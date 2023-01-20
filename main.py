import pygame, sys
from random import randint, uniform

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)   # 1. we have to init the parent class
        # 2. We need a surface -> image
        self.image = pygame.image.load("./graphics/ship.png").convert_alpha()
        # 3. We need a rect
        self.rect = self.image.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        # timer
        self.can_shoot = True
        self.shoot_time = None
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 200:
                self.can_shoot = True

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print("shoot laser")
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

            Laser(self.rect.midtop, laser_group)

    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()

# exercise
# Create a laser sprite
# create a new class + new group
# when the laser object is created, you should be able to set the position via the arguments
class Laser(pygame.sprite.Sprite): 
    def __init__(self, pos, groups):
        super().__init__(groups) 
        self.image = pygame.image.load("./graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)

        # float based position
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 600

    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        # self.rect.y -= 1

class Meteor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        # basic setup
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/meteor.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)

        # float based positioning
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 600)
    
    def update(self):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

class Score:
    def __init__(self):
        self.font = pygame.font.Font("./graphics/subatomic.ttf", 50)
    
    def display(self):
        # exercise: recreate the original display_score function inside of a class
        #actually call it in the game loop
        score_text = f"Score: {pygame.time.get_ticks() // 1000}"
        text_surf = self.font.render(score_text, True,(255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            display_surface, 
            (255,255,255), 
            text_rect.inflate(30, 30), 
            width = 8, 
            border_radius=5
        )







# exercise
# 1 create a timer
# 2 when the timer triggers create a meteor sprite
# 3 you need to create a meteor sprite class like the laser + meteor sprite group
# 4 the meteor movement should be a bit more random at the start pos is at the top of the window



# basic setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# bakcground
background_surf = pygame.image.load("./graphics/background.png").convert()

# sprite groups
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

# Sprite Creation
ship = Ship(spaceship_group)
spaceship_group.add(ship)
# timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,400)

# score
score = Score()


# main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteor_y_pos = randint(-150, -50)
            meteor_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Meteor((meteor_x_pos, meteor_y_pos), groups = meteor_group)
        
    # delta time
    dt = clock.tick() / 1000
    
    # background
    display_surface.blit(background_surf,(0, 0))

    # update
    spaceship_group.update()
    laser_group.update()
    meteor_group.update()
    
    # score
    score.display()

    # graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    pygame.display.update()