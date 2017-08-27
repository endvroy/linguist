class LALRTableBuildError(Exception):
    def __init__(self, cc, ccid):
        self.cc = cc
        self.ccid = ccid
        # self.conflict = conflict


class ReversedRangeError(Exception):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return f'Character Range Reversed in {self.start}-{self.end}'


class LangBuildError(Exception):
    pass


class ScanError(Exception):
    def __init__(self, char, loc):
        self.char = char
        self.loc = loc

    def __str__(self):
        return f"illegal character '{self.char}' near position {self.loc}"


class ParseError(Exception):
    def __init__(self, expected, got):
        self.expected = expected
        self.got = got

    def __str__(self):
        return f'Unexpected token {self.got}, expect {self.expected}'
