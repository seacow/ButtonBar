import sys, pygame
from pygame.locals import *

class Bar:

    EVENTS = (MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP)

    def __init__(self, screen):
        bar_width = screen.get_width()
        bar_height = screen.get_height() / 4

        self.bar = Rect(0, 3 * bar_height, bar_width, bar_height)
        self.button = Rect(0, 0, 50, 25)

        self.across = self.down = 0

        self.width = bar_width / self.button.width
        self.height = bar_height / self.button.height

        self.buttons = []

    def __iter__(self):
        for button in self.buttons:
            yield button

    def configure(self, button):
        if self.across == self.width:
            self.across = 0
            self.down += 1

        if self.down == self.height:
            assert False, "The button bar needs to be made larger."

        self.across += 1

        x = 50 * self.across + self.bar.x
        y = 25 * self.down + self.bar.y

        button.shape = self.button.move(x, y)
        self.buttons.append(button)

    def update(self, event):
        clicked = []

        for button in self.buttons:
            if event.pos not in button:
                button.reset()
            else:
                clicked.append(button)
                button.update(event.type)

        return clicked if event.type == MOUSEBUTTONUP else []

    def draw(self, screen):
        for button in self:
            button.draw(screen)

class Button:

    NORMAL = Color(255, 0, 0)   # Red
    OVER = Color(0, 255, 0)     # Green
    DOWN = Color(0, 0, 255)     # Blue
    TEXT = Color(0, 0, 0)       # Black

    def __init__(self, bar, name):
        self.bar = bar
        self.name = name

        self.shape = None
        self.color = Button.NORMAL
        self.font = pygame.font.Font(None, 12)
        
        bar.configure(self)
        assert self.shape

    def __contains__(self, point):
        shape = self.shape
        return shape.collidepoint(point)

    def reset(self):
        self.color = Button.NORMAL

    def update(self, event):
        if event == MOUSEMOTION:
            self.color = Button.OVER
        if event == MOUSEBUTTONDOWN:
            self.color = Button.DOWN
        if event == MOUSEBUTTONUP:
            self.color = Button.OVER

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.shape)

        text = self.font.render(self.name, True, Button.TEXT)
        screen.blit(text, self.shape)

if __name__ == "__main__":
    pygame.init()

    size = 320, 240
    screen = pygame.display.set_mode(size)

    bar = Bar(screen)
    hello = Button(bar, "Hello")
    world = Button(bar, "World")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type in bar.EVENTS:
                clicked = bar.update(event)

                if hello in clicked:
                    print "Hello"
                if world in clicked:
                    print "World"

        bar.draw(screen)

        pygame.display.flip()
        pygame.time.wait(50)
