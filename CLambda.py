#!/usr/bin/python3
"""Archivo principal de lambda."""
from lambda_calculus import parse, lex
from sys import argv

if len(argv) > 1:
    if argv[1] == '--debug':
        string = argv[2]
        print(lex(string))
        print(parse(string))
    else:
        print(parse(argv[1]))

