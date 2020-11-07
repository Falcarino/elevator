import pygame as pg
import os
import text
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]
########################################

def load_image(file):
    ''' loads an image, prepares it for play
    '''
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert_alpha()

########################################

class SceneBase:

    def __init__(self, scr):
        self.next = self
        self.screen = scr


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

    def __init__(self, scr):
        SceneBase.__init__(self, scr)
        self.inputBoxes = []

        txt = "How many floors will it be?"
        self.floor_box_txt = text.Text(txt, 20, 20)
        self.floorInput = text.TextBox('', 20, 50)
        self.floorInput.active = True
        self.inputBoxes.append(self.floorInput)
        
        txt = "Alternatively, enter a seed here:"
        self.seed_box_txt = text.Text(txt, 800, 670)
        self.seedInput = text.TextBox('', 800, 700)
        self.inputBoxes.append(self.seedInput)

        self.render()

    def generate_seed(self, floors):
        seed = ''
        for i in range(9): seed += str(random.randint(0, 9))
        seed += str(floors)
        print(seed)
        return seed
    
    def process_event(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:

                if self.floorInput.active:
                    usrStr = self.floorInput.box.text
                    if usrStr.isdigit() and int(usrStr) > 2 and int(usrStr) < 10:
                        seed = self.generate_seed(int(usrStr))
                        self.SwitchToScene(ElevatorScene(self.screen, seed))
                if self.seedInput.active:
                    seed = self.seedInput.box.text
                    self.SwitchToScene(ElevatorScene(self.screen, seed))

        else:
            for box in self.inputBoxes: box.handle_event(event)
            
        self.update()
        self.render()
            
    def update(self):
        self.floorInput.update()

    def render(self):
        self.screen.fill((255, 255, 255))

        self.seed_box_txt.draw(self.screen)
        self.floor_box_txt.draw(self.screen)
        text.Text("Just write in something between 2 and 10 and press 'enter'", 20, 80).draw(self.screen)

        self.floorInput.draw(self.screen)
        self.seedInput.draw(self.screen)

########################################

MAX_PEOPLE_ON_FLOOR = 7
BUILDING_X = 400
GROUND_FLOOR_Y = 650

class Person(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = load_image("person.png")
        self.rect = self.image.get_rect()
        self.target = self

    def make_them_disappear(self):
        self.kill()

class Floor(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = load_image("floor.png")
        self.rect = self.image.get_rect()

    def spawn_people(self, current_floor, number_of_floors, people_count):
        people_on_the_floor = []
        last_person_in_queue_x = BUILDING_X

        # spawning individual people
        for i in range(people_count):
            person = Person()

            while True:
                person.target = random.randrange(number_of_floors)
                if person.target != current_floor: break

            person.rect.x = last_person_in_queue_x
            person.rect.y = self.rect.y

            people_on_the_floor.append(person)
            last_person_in_queue_x += 50

        return people_on_the_floor

class Elevator(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.image = load_image("elevator.png")
        self.rect = self.image.get_rect()
        self.rect.x = BUILDING_X - 64
        self.rect.y = GROUND_FLOOR_Y

        self.capacity = 1
        self.speed = 64
        self.targets = []

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def add_target(self, person):
        self.targets.append(person.target)
        person.make_them_disappear()
    
    def remove_target(self, floor):
        self.targets.remove(floor)
        
    def display_targets(self, scr):
        ''' For now it'll be displaying only the last person who entered
        '''
        if self.targets:    # check of the list is not empty
            targets_txt = text.Text(str(self.targets[-1] + 1), self.rect.x + 5, self.rect.y + 5)
            targets_txt.draw(scr)

class ElevatorScene(SceneBase):

    def __init__(self, scr, seed):
        SceneBase.__init__(self, scr)
        self.seed = seed

        self.all_sprites = pg.sprite.Group()

        #spawning the building and people instide it
        self.building = []
        self.people = []
        floors_amount = int(self.seed[-1])
        self.construct_building(floors_amount)

        #spawning the elevator
        self.elevator = Elevator()
        self.all_sprites.add(self.elevator)

        # setting a winning condition flag
        self.building_is_cleared = False

    def construct_building(self, number_of_floors):
        current_floor_y = GROUND_FLOOR_Y

        for floor in range(number_of_floors):

            # spawning the floor
            self.building.append(Floor())
            self.building[floor].rect.x = BUILDING_X
            self.building[floor].rect.y = current_floor_y
            current_floor_y -= 64

            # creating a list of people on the floor
            self.seed = self.seed[:-1]
            people_count = int(self.seed[-1]) % (MAX_PEOPLE_ON_FLOOR + 1)
            people_on_the_floor = self.building[floor].spawn_people(floor, number_of_floors, people_count)
            self.people.append(people_on_the_floor)
        
        # adding all created sprites to the list
        self.all_sprites.add(self.building)
        self.all_sprites.add(self.people)
            
    def draw_captions(self):
        for floor in range(len(self.building)):
            for person in self.people[floor]:
                floor_text = text.Text(str(person.target + 1), \
                            person.rect.x + 10, person.rect.y + 10)
                floor_text.draw(self.screen)
    
    def process_event(self, event):

        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            # restart when 'r' is pressed
            if keys[pg.K_r]:
                self.SwitchToScene(MainMenu(self.screen))

            else:
                # moving one floor up
                if keys[pg.K_UP] and self.elevator.rect.y > self.building[-1].rect.y:
                    self.elevator.move_up()
                
                # moving one floor down
                elif keys[pg.K_DOWN] and self.elevator.rect.y < self.building[0].rect.y:
                    self.elevator.move_down()

                # letting in the first person in the queue, if there is any
                elif keys[pg.K_SPACE]:
                    floor = (GROUND_FLOOR_Y - self.elevator.rect.y) // 64
                    
                    # first see if there are people who want to get out
                    if floor in self.elevator.targets:
                        self.elevator.remove_target(floor)
                        # if that was the last person in the building, throw a winning text
                        if not any(self.people): self.building_is_cleared = True

                    # check if someone can be picked up, unless the elevator is not full
                    elif self.people[floor] and len(self.elevator.targets) < self.elevator.capacity:
                        self.elevator.add_target(self.people[floor][0]) # removing the sprite
                        del self.people[floor][0]

        self.update()
        self.render()
        
    def update(self):
        self.all_sprites.update()

    def render(self):
        self.screen.fill((255, 255, 255))

        # drawing destination floor caption for every person in the building
        self.draw_captions()
        self.elevator.display_targets(self.screen)

        text.Text("use up and down arrow keys to move, space to load and unload people and have fun :D", 160, 30).draw(self.screen)
        text.Text("press 'r' to restart and spawn a new building", 350, 60).draw(self.screen)
        text.Text("oh, and you can press 'escape' to cease the experience", 300, 90).draw(self.screen)
        if self.building_is_cleared:
            text.Text("You've done it! Everyone got to the floors they wanted!", 300, 730).draw(self.screen)

        self.all_sprites.draw(self.screen)