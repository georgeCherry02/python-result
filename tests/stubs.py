class Foo:
    def __init__(self, a: int):
        self.a = a

    def __eq__(self, other) -> bool:
        if isinstance(other, Foo):
            return self.a == other.a
        if isinstance(other, int):
            return self.a == other
        else:
            return False
