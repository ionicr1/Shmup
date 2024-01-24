import pygame
import random
import os
import time

WIDTH = 900
HEIGHT = 450
FPS = 60

TESTVariable = 0

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
PURPLE = (128,0,128)
YELLOW = (250,253,15)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((15,15))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.centery = (HEIGHT / 2)
        self.rect.left = 20
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.speedy = 0
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy -= 5
        if keystate[pygame.K_s]:
            self.speedy += 5
        if keystate[pygame.K_a]:
            self.speedx -= 6
        if keystate[pygame.K_d]:
            self.speedx += 6
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right > (WIDTH / 2):
            self.rect.right = (WIDTH / 2)
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet()
        bullet_sprites.add(bullet)
        bullet_sound.play()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,25))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(HEIGHT - self.rect.width)
        self.rect.x = random.randrange(WIDTH + 300, WIDTH + 400)
        self.speedx = random.randrange(-5, -2)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x < 0 - 25:
            self.rect.y = random.randrange(HEIGHT - self.rect.width)
            self.rect.x = random.randrange(WIDTH + 300, WIDTH + 400)
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centery = player.rect.centery
        self.rect.left = player.rect.right
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > WIDTH:
            self.kill()

class Stars(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(HEIGHT - self.rect.width)
        self.rect.x = random.randrange(WIDTH + 10, WIDTH + 15)
        self.speedx = random.randrange(-40, -15)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.x < 0 + 10:
            self.rect.y = random.randrange(HEIGHT - self.rect.width)
            self.rect.x = random.randrange(WIDTH + 10, WIDTH + 15)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shmup')
clock = pygame.time.Clock()

dir_name = os.path.dirname(__file__)
bullet_sound = pygame.mixer.Sound(os.path.join(dir_name, 'bullet.wav'))
bullet_sound.set_volume(0.2)
pygame.mixer.music.load(os.path.join(dir_name, 'bg.wav'))
pygame.mixer.music.play(loops=-1)

good_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
mob_sprites = pygame.sprite.Group()
star_sprites = pygame.sprite.Group()
player = Player()
mob = Mob()
for i in range(20):
    stars = Stars()
    star_sprites.add(stars)
for i in range(10):
    stars = Stars()
    star_sprites.add(stars)
for i in range(5):
    mob = Mob()
    mob_sprites.add(mob)
good_sprites.add(player)
mob_sprites.add(mob)

def game_loop():
    score = 0
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    player.shoot()
                    

        good_sprites.update()
        star_sprites.update()
        mob_sprites.update()
        bullet_sprites.update()

        hits = pygame.sprite.groupcollide(bullet_sprites, mob_sprites, True, True)
        if hits:
            score += 1
            print(score)
        
        screen.fill(BLACK)
        star_sprites.draw(screen)
        bullet_sprites.draw(screen)
        good_sprites.draw(screen)
        mob_sprites.draw(screen)
        pygame.display.flip()

def main():
    game_loop()

if __name__ == '__main__':
    main()