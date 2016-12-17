(function(){

if (window.addEventListener){
	document.addEventListener('DOMContentLoaded', attachEvents);
}

function attachEvents(){
	var pageExpression = new RegExp('^(?:' + document.location.protocol + '//' + document.location.hostname.replace('.', '\\.') + '|)(?:/[^.]+|\\.html?)$'),
		currentRequest = null;

	function handlePopState(event){
		var url = document.location.href;
		if (url.match(pageExpression)){
			loadPage(url, true);
		} else {
			window.location = url;
		}
	}

	function handleClick(event){
		var target = (event.target || event.srcElement);
		while (target && (target.nodeType == 3 || target.tagName == null || target.tagName.toLowerCase() != 'a')){
			target = target.parentNode;
		}

		if (event.button == 0 && target) {
			var url = target.href;

			if (url.match(pageExpression)){
				if (document.location.href == url) {
					target.blur();
				} else {
					loadPage(target.href);
				}

				if (event.preventDefault){
					event.preventDefault();
				}
				event.returnValue = false;
				return false;
			}
		}
	}

	window.onpopstate = handlePopState;
	document.body.addEventListener('click', handleClick);
}

function loadPage(url, fromHistory){
	insertLoadingElement();

	abortRequest(currentRequest);

	if (!fromHistory) {
		window.history.pushState(null, '', url);
	}

	currentRequest = sendRequest(url, function(response){
		removeLoadingElement();

		var title = getTitleFromHTML(response);
		if (title){
			document.title = title;
			if (!fromHistory) {
				window.history.replaceState(null, title, url);
			}
		}

		var body = getBodyFromHTML(response);
		if (body) {
			for (var attribute in body.attributes){
				document.body.setAttribute(attribute, body.attributes[attribute]);
			}
			document.body.innerHTML = body.content;
		}

		currentRequest = null;
	});
}

function getRequestObject(){
	function getXMLHttpRequestObject(){
		return new XMLHttpRequest();
	}
	function getMSXML2Object(){
		return new ActiveXObject('MSXML2.XMLHTTP');
	}
	function getMSXMLObject(){
		return new ActiveXObject('Microsoft.XMLHTTP');
	}

	var request = null;

	try {
		request = getXMLHttpRequestObject();
		getRequestObject = getXMLHttpRequestObject;
	} catch (error){}
	try {
		request = getMSXML2Object();
		getRequestObject = getMSXML2Object;
	} catch (error){}
	try {
		request = getMSXMLObject();
		getRequestObject = getMSXMLObject;
	} catch (error){}

	return request;
}

function sendRequest(url, callback){
	var request = getRequestObject();

	request.open('GET', url, true);
	request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

	request.onreadystatechange = function(){
		if (request.readyState == 4) {
			request.onreadystatechange = function(){};
			if (callback){
				callback(request.responseText);
			}
		}
	}

	request.send();

	return request;
}

function abortRequest(request){
	if (request){
		request.abort();
		request.onreadystatechange = function(){};
	}
}

function getLoadingElement(){
	function getExistingLoadingElement(){
		return element;
	}

	var element = document.createElement('div');
	element.className = 'loading';
	element.appendChild(document.createElement('span'));

	getLoadingElement = getExistingLoadingElement;

	return element;
}

function insertLoadingElement(){
	var element = getLoadingElement();

	if (!element.parentNode){
		var parent = document.getElementById('top');
		if (parent){
			parent = parent.getElementsByTagName('*')[0];
			if (parent){
				if (parent.childNodes.length){
					parent.insertBefore(element, parent.childNodes[0]);
				} else {
					parent.appendChild(element);
				}
			}
		}
	}

	return element;
}

function removeLoadingElement(){
	var element = getLoadingElement();

	if (element.parentNode){
		element.parentNode.removeChild(element);
	}
}

function getTitleFromHTML(html){
	var title = null;

	var titleMatch = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
	if (titleMatch){
		title = titleMatch[1];
	}

	return title;
}

function getBodyFromHTML(html){
	var body = null;

	var bodyMatch = html.match(/<body([^>]*)>([\s\S]*?)<\/body>/i);
	if (bodyMatch){
		body = {
			attributes: {},
			content: bodyMatch[2].replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
		};

		var attributeString = bodyMatch[1].trim();
		if (attributeString) {	
			var attributeExpression = /([^\s=]+)(?:="([^"]+)")?(?:\s|$)/g,
				attributeMatch;

			while (attributeMatch = attributeExpression.exec(attributeString)) {
				body.attributes[attributeMatch[1]] = attributeMatch[2];
			}
		}
	}

	return body;
}

})();
