import pygame
import os
import time
import random
import math

WIDTH, HEIGHT = 1000, 500
SIZE = WIDTH, HEIGHT

# Load images
player_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "fly-1.png")), (70, 70))
player_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "fly-2.png")), (70, 70))

t_rex_img_1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "t-rex-1.png")), (100, 100))
t_rex_img_2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "t-rex-2.png")), (100, 100))


road_img = pygame.transform.scale(pygame.image.load(os.path.join("images", "road.png")), (2*WIDTH, int(HEIGHT/2)))

class Object:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = []
        self.animation = True # flag for swap image to create animation effect
        self.velocity = 0

    def render(self, screen):
        if self.animation:
            screen.blit(self.img[0], (self.x, self.y))
            self.animation = not self.animation
        else:
            screen.blit(self.img[1], (self.x, self.y))
            self.animation = not self.animation

class Player(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = [player_img_1, player_img_2]

    def jump(self):
        self.y -= 10
    
    def drown(self):
        self.y += 3

class Trex(Object):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.img = [t_rex_img_1, t_rex_img_2]
        self.velocity = 5

    def move(self):
        self.x -= self.velocity

class Road:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = road_img
        self.velocity = 5

    def render(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x -= self.velocity


def main():
    run = True
    fps = 120
    score = 0
    clock = pygame.time.Clock()

    player = Player(50, 360)
    t_rexs = [Trex(WIDTH - t_rex_img_1.get_width() - 20, 340)]
    roads = [Road(0, 240)]

    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Jumping T-Rex")

    # Initialize font
    pygame.font.init()
    score_font = pygame.font.SysFont("pixel", 40)

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

    def on_render():
        # render background
        screen.blit(background, (0, 0))

        # render label
        score_label = score_font.render("Score: {}".format(math.floor(score)), 1, (0, 0, 0))
        screen.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        # render player
        player.render(screen)

        # render t-rex
        for t_rex in t_rexs:
            t_rex.render(screen)

        # render infinity road
        for road in roads:
            road.render(screen)

        pygame.display.update()

    # Event loop
    while run:
        clock.tick(fps)
        on_render()

        score += 0.2

        for t_rex in t_rexs:
            t_rex.move()
            if t_rex.x < -10:
                t_rex.x = WIDTH*random.randrange(1, 3)

        for road in roads:
            road.move()
            if road.x == -WIDTH:
                roads.append(Road(WIDTH, 240))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys =  pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and player.y < 360:
            player.y += 8
        if keys[pygame.K_SPACE] and player.y > 0:
            player.jump()

        if (not keys[pygame.K_SPACE]) and (not keys[pygame.K_DOWN]) and player.y < 360:
            player.drown()    

if __name__ == '__main__':
    main()