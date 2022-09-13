from .workfile import TokenParser

def loads(workfile):
    parser = TokenParser()
    return parser.parse_string(workfile)

def load(workfile):
    parser = TokenParser()
    return parser.parse_file(workfile)