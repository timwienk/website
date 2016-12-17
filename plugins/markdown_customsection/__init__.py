'''
Custom section extension for Python-Markdown
============================================

Wraps the document in logical sections, as implied by h1-h6 headings.

Downgrades h1-h5 headings to h2-h6, and adds a span inside the heading
elements containing the heading text, for styling purposes.

The section logic is based on:
https://github.com/jessedhillon/mdx_sections
'''

import re
from markdown.util import etree
from markdown import Extension
from markdown.treeprocessors import Treeprocessor


class CustomSectionProcessor(Treeprocessor):
	def process_headings(self, node):
		pattern = re.compile('^h(\d)')

		for child in list(node):
			match = pattern.match(child.tag.lower())

			if match:
				new_level = min(6, int(match.group(1)) + 1)
				child.tag = 'h' + str(new_level)

				span = etree.SubElement(child, 'span')
				span.text = child.text
				child.text = ''

			else:
				self.process_headings(child)

	def process_sections(self, node):
		s = []
		pattern = re.compile('^h(\d)')

		for child in list(node):
			match = pattern.match(child.tag.lower())

			if match:
				section = etree.SubElement(node, 'section')

				section.append(child)
				node.remove(child)

				for key, value in list(child.attrib.items()):
					section.set(key, value)
					del child.attrib[key]

				depth = int(match.group(1))
				contained = False

				while s:
					container, container_depth = s[-1]
					if depth <= container_depth:
						s.pop()
					else:
						contained = True
						break

				if contained:
					container.append(section)
					node.remove(section)

				s.append((section, depth))

			else:
				if s:
					container, container_depth = s[-1]
					container.append(child)
					node.remove(child)
				else:
					self.process_sections(child)

		if len(node) > 1 or len(node) == 1 and len(node[0]) > 0:
			extra_section = None

			for child in list(node):
				if child.tag.lower() == 'p':
					if extra_section is None:
						extra_section = etree.Element('section')
						node.insert(0, extra_section)

					node.remove(child)
					extra_section.append(child)

				else:
					break
			
	def run(self, root):
		self.process_headings(root)
		self.process_sections(root)
		return root


class CustomSectionExtension(Extension):
	def extendMarkdown(self, md, md_globals):
		ext = CustomSectionProcessor(md)
		md.treeprocessors.add('customsection', ext, '_end')


def makeExtension(*args, **kwargs):
	return CustomSectionExtension(*args, **kwargs)
