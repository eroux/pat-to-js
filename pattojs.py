#!/usr/bin/env python3

import argparse
import sys
import re
import json

parser = argparse.ArgumentParser(
    				description='A script to jsify pat hyphenation patterns.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-r', '--right-hyphenmin',
                    help='right hyphen min',
                    default=2, dest='right')
parser.add_argument('-l', '--left-hyphenmin',
                    help='left hyphen min',
                    default=2, dest='left')
parser.add_argument('-i', '--input', nargs='?', type = argparse.FileType('r'),
					default=sys.stdin, dest='inputfile')
parser.add_argument('-e', '--exception-list', nargs='?', type = argparse.FileType('r'),
					default=None, dest='exceptionlist')
parser.add_argument('-o', '--output-file', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, dest='outputfile')
parser.add_argument('-n', '--lang-name',
                    default='en_US', dest='name')

args = parser.parse_args()

res_obj = {}
res_obj['leftmin'] = args.left
res_obj['rightmin'] = args.right
res_obj['specialChars'] = ''
res_obj['patterns'] = {}
res_obj['patternChars'] = ''

patternChars = {}
specialChars = {}
patterns = {}

def add_pattern(pat):
	patlen = 0
	for c in pat:
		if not c.isdigit() and not c == '-' and not c == '.':
			patlen += 1
			if ord(c) < 128:
				patternChars[c] = True
			else:
				specialChars[c] = True
	if patlen not in patterns:
		patterns[patlen] = []
	patterns[patlen].append(pat)


for line in args.inputfile:
	line = line.strip()
	add_pattern(line)

def compute_object():
	patternCharsKeys = list(patternChars.keys())
	patternCharsKeys.sort()
	res_obj['patternChars'] = ''.join(patternCharsKeys)
	specialCharsKeys = list(specialChars.keys())
	specialCharsKeys.sort()
	res_obj['specialChars'] = ''.join(specialCharsKeys)
	for patlen,patternArray in patterns.items():
		res_obj['patterns'][patlen] = ''.join(patternArray)

compute_object()

print('Hyphenator.languages[\''+args.name+'\'] = '+json.dumps(res_obj)+';')

