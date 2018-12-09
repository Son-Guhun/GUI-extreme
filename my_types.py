

class IntBool(int):
    """
     A boolean type whose __str__ method returns either "1" or "0".

    It's __repr__ type returns either "True(1)" or "False(0)"

    IntBool(x) is logically equivalent to bool(int(x)). Therefore, types which cannot be converted to an integer with
    int() cannot be used as arguments to IntBool().

    Only two instances of this class exist: IntTrue and IntFalse.
    """

    def __new__(cls, arg):
        return IntTrue if int(arg) else IntFalse

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return "{}({})".format(bool.__str__(bool(self)), str(self))


IntTrue = int.__new__(IntBool,1)
IntFalse = int.__new__(IntBool,0)


class WC3Version(int):

    names = {0:  "Reign of Chaos",
             1:  "The Frozen Throne"
             }

    tracker = {}

    def __new__(cls, arg):
        if arg not in cls.tracker:
            cls.tracker[arg] = int.__new__(WC3Version, arg)
        return cls.tracker[arg]

    def __repr__(self):
        return "WC3Version('{}')".format(self.names[self]) if self in self.names else "WC3Version('Unknown')"

    @property
    def title(self):
        return self.names[self]


REIGN_OF_CHAOS = WC3Version(0)
FROZEN_THRONE = WC3Version(1)