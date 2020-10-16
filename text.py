import pygame as pg

class Text:

    def __init__(self, text, x, y):
        self.text = text
        self.pos = (x, y)

        self.fontname = None
        self.fontsize = 36
        self.fontcolor = (0, 0, 0)
        self.set_font()
        self.render()
    
    def set_font(self):
        self.font = pg.font.Font(self.fontname, self.fontsize)

    def render(self):
        self.surface = self.font.render(self.text, True, self.fontcolor)

    def draw(self, screen):
        self.render()
        screen.blit(self.surface, self.pos)

    def get_surface_width(self): return self.surface.get_width()

class TextBox:

    def __init__(self, text, x, y):
        #setting up the rectangle for the text
        self.x, self.y = x, y
        w, h = 50, 25
        self.rect = pg.Rect(self.x, self.y, w, h)
        self.box = Text(text, self.x, self.y)

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.box.text = self.box.text[:-1]
            else:
                self.box.text += event.unicode
            self.box.render()

    def update(self):
        # Resize the box if the text is too long
        width = max(self.rect.w, self.box.get_surface_width()+10)
        self.rect.w = width

    def draw(self, screen):
        #remove old text and blit a new one
        pg.draw.rect(screen, (255, 255, 255), self.rect)
        screen.blit(self.box.surface, (self.x, self.y))
