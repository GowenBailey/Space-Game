import pygame, sys

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
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            print("shoot laser")
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

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
# Sprite Creation
ship = Ship(spaceship_group)
spaceship_group.add(ship)
laser = Laser((100,300), laser_group)

# main game loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    # delta time
    dt = clock.tick() / 1000
    
    # background
    display_surface.blit(background_surf,(0, 0))

    # update
    spaceship_group.update()

    # graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)

    pygame.display.update()