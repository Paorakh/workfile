from .workfileparser import TokenParser

def loads(workfile):
    return TokenParser.parse_string(workfile)

def load(workfile):
    return TokenParser.parse_file(workfile)