
class Button():
    def __init__(self, name) -> None:
        self.name = name
        self.holds = 0
        self.presses = 0
    def track(self, info):
        if len(info) > 2:
            self.presses+=1
        else:
            self.holds+=1
    def getState(self):
        return {
            'holds':self.holds,
            'presses':self.presses,
        }

class Select(Button):
    def __init__(self, name="Select") -> None:
        super().__init__(name)
class Start(Button):
    def __init__(self, name="Start") -> None:
        super().__init__(name)
class Up(Button):
    def __init__(self, name="Up") -> None:
        super().__init__(name)
class Down(Button):
    def __init__(self, name="Down") -> None:
        super().__init__(name)
class Right(Button):
    def __init__(self, name="Right") -> None:
        super().__init__(name)
class Left(Button):
    def __init__(self, name="Left") -> None:
        super().__init__(name)
class L2(Button):
    def __init__(self, name="L2") -> None:
        super().__init__(name)
class R2(Button):
    def __init__(self, name="R2") -> None:
        super().__init__(name)
class L1(Button):
    def __init__(self, name="L1") -> None:
        super().__init__(name)
class R1(Button):
    def __init__(self, name="R1") -> None:
        super().__init__(name)
class Triangle(Button):
    def __init__(self, name="Triangle") -> None:
        super().__init__(name)
class Circle(Button):
    def __init__(self, name="Circle") -> None:
        super().__init__(name)
class X(Button):
    def __init__(self, name="X") -> None:
        super().__init__(name)
class Square(Button):
    def __init__(self, name="Square") -> None:
        super().__init__(name)


class Controller():
    def __init__(self, player) -> None:
        self.player = player
        self.select = Select()
        self.start = Start()
        self.up = Up()
        self.right = Right()
        self.down = Down()
        self.left = Left()
        self.l2 = L2()
        self.l1 = L1()
        self.r2 = R2()
        self.r1 = R1()
        self.triangle = Triangle()
        self.circle = Circle()
        self.x = X()
        self.square = Square()
    def track(self, event):
        '''event is 0209['button'] which is a 2 or 4 digit string'''
        button = event[0]
        if button == '0':
            self.select.track(event)
        elif button == '3':
            self.start.track(event)
        elif button == '4':
            self.up.track(event)
        elif button == '5':
            self.right.track(event)
        elif button == '6':
            self.down.track(event)
        elif button == '7':
            self.left.track(event)
        elif button == '8':
            self.l2.track(event)
        elif button == '9':
            self.r2.track(event)
        elif button == 'A':
            self.l1.track(event)
        elif button == 'B':
            self.r1.track(event)
        elif button == 'C':
            self.triangle.track(event)
        elif button == 'D':
            self.circle.track(event)
        elif button == 'E':
            self.x.track(event)
        elif button == 'F':
            self.square.track(event)
    def getState(self):
        return{
            self.select.name:self.select.getState(),
            self.start.name:self.start.getState(),
            self.up.name:self.up.getState(),
            self.right.name:self.right.getState(),
            self.down.name:self.down.getState(),
            self.left.name:self.left.getState(),
            self.r2.name:self.r2.getState(),
            self.l1.name:self.l1.getState(),
            self.l2.name:self.l2.getState(),
            self.r1.name:self.r1.getState(),
            self.triangle.name:self.triangle.getState(),
            self.circle.name:self.circle.getState(),
            self.x.name:self.x.getState(),
            self.square.name:self.square.getState(),
        }