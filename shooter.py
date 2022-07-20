from turtle import position
import pygame as pg
from random import randint
pg.font.init()
pg.mixer.init()

WIDTH = 800
HEIGHT = 640

window = pg.display.set_mode((WIDTH, HEIGHT))

clock = pg.time.Clock()

class ImageSprite(pg.sprite.Sprite):
    def __init__(self, filename, position, size, speed=(0,0)): # create the constructor (runs when a new object is created)
        super().__init__()
        self.image = pg.image.load(filename)
        self.image = pg.transform.scale(self.image, size)
        self.rect = pg.Rect(position, size)
        self.speed = pg.Vector2(speed)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Player(ImageSprite):
    def __init__(self, filename, position, size, speed=(0,0)):
        super().__init__(filename, position, size, speed)
        self.original_pos = position
    def reset(self):
        self.rect.topleft = self.original_pos
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= self.speed.x
        if keys[pg.K_d]:
            self.rect.x += self.speed.x
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def shoot(self):
        temp_bullet = Bullet(filename="laser.png", position=(0,0), size=(5, 10), speed=(0, -15))
        temp_bullet.rect.midbottom = self.rect.midtop
        bullets.add(temp_bullet)

class Enemy(ImageSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top >= HEIGHT-90:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)


class Bullet(ImageSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.bottom < 0:
            self.kill()


rocket = Player(filename="rocket.png", position=(WIDTH/2, HEIGHT-90), size=(50,50), speed=(12, 0))
bg = ImageSprite(filename="bg.jpeg", position=(0, 0), size=(WIDTH, HEIGHT))
enemies = pg.sprite.Group()
bullets = pg.sprite.Group()


def CreateEnemy():
    temp_enemy = Enemy(filename="enemy.png", position=(0,0), size=(50, 50), speed=(0, randint(1,5)))
    temp_enemy.rect.x = randint(0, WIDTH-temp_enemy.rect.width)
    enemies.add(temp_enemy)


for i in range(randint(6, 10)):
    CreateEnemy()


# Main loop
while not pg.event.peek(pg.QUIT):
    for ev in pg.event.get():
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_SPACE:
                rocket.shoot()

    rocket.update()
    enemies.update()
    bullets.update()

    bg.draw(window)
    rocket.draw(window)
    enemies.draw(window)
    bullets.draw(window)

    pg.display.update()
    clock.tick(60)