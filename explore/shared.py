
class Object:
    description = ''

    def __init__(self, name, char, weight=1):
        self.name = name
        self.char = char
        self.weight = weight

    def __str__(self):
        return self.char

    def descr(self):
        return "You see %s\n\n%s" % (self.name, self.description or "nothing is known about this object")
        # return self.description or "nothing is known about this object"
