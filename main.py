import pygame, random, math
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
pygame.init()

#======
#CONFIG
#======

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

background_color = (0, 0, 0)

color_offset = [random.random() * 2 * math.pi for x in range(3)]
color_change_speed = [0.25 + random.random()/2 for x in range(3)]
current_time = 0
running = True

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
clock = pygame.time.Clock()
delta_time = 0
print("Hello Christus!")
#======
#Sprites
#======

class GameObject(pygame.sprite.Sprite):
    def __init__(self, height = 50, width = 50, color = (255, 255, 255)):
        super(GameObject, self).__init__()
        self.move_dir = pygame.math.Vector2()
        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()

    def reset(self):
        self.rect.left = 0
        self.rect.top = 0

    def update(self, pressed_keys, time_passed, max_speed = 1000):
        input_dir = pygame.math.Vector2()
        speed = max_speed * time_passed
        b = False
        for key_pressed in [K_DOWN, K_LEFT, K_RIGHT, K_UP]: b = b or pressed_keys[key_pressed]
        if b: 
            global current_time
            current_time += delta_time
    
        input_dir.y = int(pressed_keys[K_DOWN]) - int(pressed_keys[K_UP])
        input_dir.x = int(pressed_keys[K_RIGHT]) - int(pressed_keys[K_LEFT])
        input_dir *= speed
        self.rect.centerx += input_dir.x
        self.rect.centery += input_dir.y

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.posY = random.randint(0, SCREEN_HEIGHT)
        self.rand = random.random() * 2 * math.pi
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                self.posY,
            )
        )
        self.speed = random.randint(1000, 2000)

    def update(self):
        self.rect.move_ip(-self.speed * delta_time, 0)
        self.rect.y = self.posY + math.sin(self.rand + pygame.time.get_ticks()/200) * 50
        if self.rect.right < 0:
            self.kill()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)


player = GameObject()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

new_enemy = Enemy()
enemies.add(new_enemy)
all_sprites.add(new_enemy)

all_sprites.add(player)

def update_sprites():
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

def update_enemies():
    for enemy in enemies: enemy.update()

def kill_enemies():
    for enemy in enemies: enemy.kill()

def update_color():
    global background_color
    background_color = (
        int((1 + math.sin(color_offset[0] + current_time * color_change_speed[0]))*255/6),
        int((1 + math.sin(color_offset[1] + current_time * color_change_speed[1]))*255/6),
        int((1 + math.sin(color_offset[2] + current_time * color_change_speed[2]))*255/6),
        )


while running:

    delta_time = clock.tick() / 1000
    
    update_color()

    for event in pygame.event.get():
        if (event.type == QUIT):
            running = False
        if(event.type == ADDENEMY):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys, delta_time)
    screen.fill(background_color)
    update_enemies()
    update_sprites()
    if pygame.sprite.spritecollideany(player, enemies):
        player.reset()
        kill_enemies()
    
    #render all to the screen
    pygame.display.flip()

pygame.quit()