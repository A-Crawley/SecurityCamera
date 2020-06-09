
class MyClass():
    def __init__(self, first, second):
        self.f = first
        self.s = second

    def total(self):
        calc = self.f + self.s
        return ("Claculation: ", calc)


if __name__ == "__main__":
    c = MyClass(1, 2)
    string, calc = c.total()
    print(string + str(calc))
