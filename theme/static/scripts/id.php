<?php

# Very simple script that generates an ID that looks random, based on
# the client's IP address. In cases where a more precise determination
# is not required, this "unique" ID can be used to identify clients
# without the use of cookies, e.g. for client side analytics scripts.

header('Content-Type: text/plain; charset=UTF-8', true);
header('X-Robots-Tag: noindex', true);

$ip_address = null;

if (!empty($_SERVER['REMOTE_ADDR'])) {
	$ip_address = $_SERVER['REMOTE_ADDR'];
} else {
	$ip_address = '127.0.0.1';
}

$base = [
	252345678,
	263456789,
	264242424,
	255123123
];
$ipv4_multiplier = 18;

$id = '';

if (strpos($ip_address, '.') === false) {
	$parts = explode(':', $ip_address);
	$part_count = count($parts);
	if ($part_count < 8) {
		array_splice($parts, array_search('', $parts), 0, array_pad([], 8 - $part_count, ''));
	}
	foreach ($parts as $index => $part) {
		$part = substr($base[$index % 4], 0, 5) - hexdec($part);
		if ($part < 0) {
			$part += 65535;
		}
		$part = dechex($part);
		if ($index % 2) {
			$part = strrev($part);
		}
		$id .= str_pad($part, 4, '0', STR_PAD_LEFT);
	}
} else {
	$ipv6_prefix_position = strrpos($ip_address, ':');
	if ($ipv6_prefix_position !== false) {
		$ip_address = substr($ip_address, $ipv6_prefix_position + 1);
	}
	$id = '6292';
	foreach (explode('.', $ip_address) as $index => $part) {
		$part = dechex($base[$index] - $ipv4_multiplier * intval(decbin($part), 10));
		if ($index % 2) {
			$part = strrev($part);
		}
		$id .= $part;
	}
}

$id = preg_replace('/^(.{8})(.{4})(.{4})(.{4})(.{12})$/', '$1-$2-$3-$4-$5', $id);

echo $id, "\n";
