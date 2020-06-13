from pathlib import Path


class Window:
    def __init__(self):
        print("WIndow init")
        self.cust = Custom(self)
        self.fruit_list = ["Apple"]

    def add_item(self, name):
        self.fruit_list.append(name)
        print("Item added:", self.fruit_list)

    def run_foo(self):
        self.cust.foo()

    def display_list(self):
        print(self.fruit_list)


class Custom:
    def __init__(self, parent):
        print("Custom init")
        self.parent = parent

    def foo(self):
        name = input("Enter name:")
        self.parent.add_item(name)


path_1 = "L:/SCRIPT/Colour/OCIO_converter/design/output_design//icon_idt_v2\icon_idt_acescc.png"
path_2 = "L:/SCRIPT/Colour/OCIO_converter/design/output_design/icon_idt_v2/icon_idt_acescc.png "


def foopath():
    var1 = Path(path_1)
    var2 = Path(path_2)
    print(str(var1), type(str(var1)))
    print(var2, type(var2))


if __name__ == '__main__':
    foopath()
