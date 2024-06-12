from random import randint
from pygame import *
from time import time as get_time
SCREEN_SIZE = (1200, 800)
SPRITE_SIZE = 60

def show_text(text, x, y, text_color = (255, 255, 255), text_size = 40, font_name = 'Verdana'):
        f = font.SysFont(font_name, text_size)
        image = f.render(text, True, text_color)
        window.blit(image,(x, y))  

class GameSprite(sprite.Sprite):
    def __init__ (self, image_name, x, y, speed, image_scale = 1):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (SPRITE_SIZE//image_scale, SPRITE_SIZE//image_scale))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
font.init()
class Counter:
    def __init__(self, x, y, text):
        self.pos = (x, y)
        self.text = text
        self.count = 0 
    def render_text(self, text_color = (255, 255, 255), text_size = 40, font_name = 'Verdana'):
        f = font.SysFont(font_name, text_size)
        self.image = f.render(self.text + str(self.count), True, text_color)
    def reset(self):
        window.blit(self.image, self.pos)  




class enemy(GameSprite):
    def __init__(self, image_name, x, y,  speed):
        if speed > 1:
            super().__init__(image_name, x, y, speed, 2)
        else:
            super().__init__(image_name, x, y, speed)   
        self.set_hp()

    def set_hp(self):
        if self.speed == 3 or self.speed == 2:
            self.hp = 1
        else:
            self.hp = 3    

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE) 
            missed_counter.count += 1
            missed_counter.render_text() 
               
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE) 
class Bullet(GameSprite):
        def update(self):
            self.rect.y -= self.speed
            if self.direction == 1:
                self.rect.x -= self.speed
            elif self.direction == 2:
                self.rect.x += self.speed

        def __init__ (self, image_name, x, y, speed, direction = 0):
            super().__init__(image_name, x, y, speed)
            self.direction = direction     

class Player(GameSprite):
    def __init__ (self, image_name, x, y, speed, lives = 3, image_live = 'heart.png'):
        super().__init__(image_name, x, y, speed)
        self.last_shoot_time = 0
        self.last_shoot_time_for_new_weapon = 0 
        self.lives = lives
        self.image_live = transform.scale(image.load(image_live), (SPRITE_SIZE, SPRITE_SIZE))
    def draw_lives(self):
        for i in range(self.lives):
            window.blit(self.image_live, (SCREEN_SIZE[0]-i*70-80, 20))   
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < SCREEN_SIZE[0] - SPRITE_SIZE:
            self.rect.x += self.speed
        if keys_pressed[K_q]:
            if get_time() - self.last_shoot_time_for_new_weapon > .8:
                self.new_weapon_shoot()
                self.last_shoot_time_for_new_weapon = get_time()  
        if keys_pressed[K_SPACE]: 
            if get_time() - self.last_shoot_time > .5:
                self.shoot()
                self.last_shoot_time = get_time()
        self.reset()        
    def new_weapon_shoot(self):
        for i in range(3):
            new_bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 7, i)
            new_bullet.image = transform.scale(new_bullet.image, (SPRITE_SIZE//4, SPRITE_SIZE//4))
            new_bullet.rect = new_bullet.image.get_rect()
            new_bullet.rect.x = self.rect.centerx - 8
            new_bullet.rect.y = self.rect.y
            bullets.add(new_bullet)


        
    def shoot(self):
        new_bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 7)
        new_bullet.image = transform.scale(new_bullet.image, (SPRITE_SIZE//4, SPRITE_SIZE//4))
        new_bullet.rect = new_bullet.image.get_rect()
        new_bullet.rect.x = self.rect.centerx - 8
        new_bullet.rect.y = self.rect.y
        s = mixer.Sound('awp1.mp3')
        s.set_volume(0.1)
        s.play()
        bullets .add(new_bullet)
missed_counter = Counter(10, 10, 'Количество пропущенных:')
missed_counter.render_text()
killed_counter = Counter(10, 40, 'Количество уничтожегнных')
killed_counter.render_text()
bullets =  sprite.Group()
enemies = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    new_enemy = enemy('ufo.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, randint(1,3))
    enemies.add(new_enemy)    
asteroids.add(Asteroid('asteroid.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 1))
asteroids.add(Asteroid('asteroid.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 1))
player = Player('rocket.png',SCREEN_SIZE[0]/2, SCREEN_SIZE[-1]- SPRITE_SIZE, 10, image_live = 'heart.png')       

window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')
background = transform.scale(
        image.load('galaxy.jpg'),
        SCREEN_SIZE
)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()            
game = True
clock = time.Clock()
FPS = 60
finish = False
while game:
    clock.tick(FPS)
    if finish == False:
        window.blit(background, (0,0))
        player.update()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        killed_counter.reset()
        missed_counter.reset()
        monsters_list = sprite.groupcollide(enemies, bullets, False, True)
        for m in monsters_list:
            m.hp -= 1
            if m.hp <= 0:
                m.set_hp()
                m.hp = 2    
                m.rect.y = 0
                m.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
                killed_counter.count += 1
                killed_counter.render_text() 
        for m in sprite.spritecollide(player, enemies, False)  or sprite.spritecollide(player, asteroids, False):
            m.rect.y = 0
            m.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            player.lives -= 1
        if missed_counter.count >= 3:
            player.lives -= 1
            missed_counter.count = 0
        if player.lives <= 0:
            show_text('Поражение', SCREEN_SIZE[0]//2 -  50, SCREEN_SIZE[1]//2- 50)
            mixer.music.stop()
            finish = True  

            
        if killed_counter.count >= 10:
            show_text('Победа', SCREEN_SIZE[0]//2 -  50, SCREEN_SIZE[1]//2- 50)
            mixer.music.stop()
            finish = True 
        #show_text(str(player.lives), SCREEN_SIZE[0]-40, 10)
        player.draw_lives()        
        display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False

