class Epsilon:
    def __repr__(self):
        return '<epsilon>'

    def __eq__(self, other):
        if isinstance(other, Epsilon):
            return True
        else:
            return False

    def __hash__(self):
        return 0


class EOF:
    def __repr__(self):
        return '<eof>'

    def __eq__(self, other):
        if isinstance(other, EOF):
            return True
        else:
            return False

    def __hash__(self):
        return 1


epsilon = Epsilon()
eof = EOF()
