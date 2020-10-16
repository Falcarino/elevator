#check "cars" project to see how to deal with sprites, seems easier than the "aliens" one
import pygame as pg
import text
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
########################################

def load_image(file):
    """ loads an image, prepares it for play
    """
    file = os.path.join(main_dir, "sprites", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert_alpha()

########################################

class SceneBase:

    def __init__(self, scr):
        self.screen = scr
        self.screen.fill((255, 255, 255))
        self.next = self

    def process_event(self, event):
        print('class SceneBase not overridden')
    def update():
        print('class SceneBase not overridden')
    def render():
        print('class SceneBase not overridden')

    def SwitchToScene(self, new_scene):
        self.next = new_scene

########################################

class MainMenu(SceneBase):

    def __init__(self, scr, txt="How many floors will it be? (doesn't do anything for now)"):
        SceneBase.__init__(self, scr)
        self.txt = text.Text(txt, 20, 20)
        self.txt.draw(self.screen)

        text.Text("just write in something between 2 and 10 and press 'enter'", 20, 80).draw(self.screen)

        self.userInput = text.TextBox('0', 20, 50)
    
    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                usrStr = self.userInput.box.text
                if usrStr.isdigit() and int(usrStr) > 2 and int(usrStr) < 10:
                    self.SwitchToScene(ElevatorScene(self.screen))
            else:
                self.userInput.handle_event(event)
                self.update()
                self.render()
            
    def update(self):
        self.userInput.update()

    def render(self):
        self.userInput.draw(self.screen)

########################################

class Person(pg.sprite.Sprite):
    def __init__(self, starting_floor, destination):
        super.__init__(self)

        self.floor = starting_floor
        self.target = destination

        self.x = 100
        self.y = 100 * self.floor

class Elevator(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = load_image("elevator.png")
        self.rect = self.image.get_rect()
        self.rect.x = 334
        self.rect.y = 650

        self.speed = 32
        """
        self.floorQueues = [list(floor) for floor in queues]
        self.capacity = capacity
        self.number_of_floors = len(self.floorQueues)
        self.currentFloor, self.direction = 0, 1
        self.liftTrace, self.people_in_lift = [0], []
        """
    def move_up(self):
        self.rect.y -= self.speed
    def move_down(self):
        self.rect.y += self.speed

class Floor(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = load_image("floor.png")
        self.rect = self.image.get_rect()

class ElevatorScene(SceneBase):

    def __init__(self, scr):
        SceneBase.__init__(self, scr)

        self.all_sprites = pg.sprite.Group()
        self.elevator = Elevator()
        self.all_sprites.add(self.elevator)

        self.building = []
        self.construct_building(4)

        
        self.update()
        self.render()

    def construct_building(self, number_of_floors):
        y = 650

        for floor in range(number_of_floors):
            self.building.append(Floor())
            self.building[floor].rect.x = 400
            self.building[floor].rect.y = y

            y -= 64
        
        self.all_sprites.add(self.building)
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
            
    
    def process_event(self, event):
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_UP] and self.elevator.rect.y > self.building[-1].rect.y:
                self.elevator.move_up()
            if keys[pg.K_DOWN] and self.elevator.rect.y < self.building[0].rect.y:
                self.elevator.move_down()

        self.update()
        self.render()
            
    def update(self):
        self.all_sprites.update()

    def render(self):
        self.screen.fill((255, 255, 255))
        text.Text("use up and down arrow keys and have fun :D", 350, 80).draw(self.screen)
        text.Text("oh, and you can press 'escape' to cease the experience", 300, 120).draw(self.screen)
        self.all_sprites.draw(self.screen)