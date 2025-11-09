#создай игру "Лабиринт"!
from pygame import *

window = display.set_mode((700,500))
display.set_caption('Лабиринт')

background = transform.scale(image.load("background.jpg"), (700,500))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed ):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        
        if keys[K_d] and self.rect.x < 700 - 75:
            self.rect.x += self.speed
        
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_s] and self.rect.y < 500 - 75:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = "left"
        
    def update(self):
        if self.rect.x <= 215:
            self.direction = "right"
        if self.rect.x >= 580:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed     
        else:
            self.rect.x += self.speed      
    
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        

player = Player('hero.png', 5, 420, 4)
monster = Enemy('cyborg.png', 470 , 280, 2)
final = GameSprite('treasure.png', 580, 420, 0)

w1 = Wall(150, 200, 50, 100, 10, 550, 10)
w2 = Wall(150, 200, 50, 100, 490, 350, 10)
w3 = Wall(150, 200, 50, 100, 20, 10, 380)
w4 = Wall(150, 200, 50, 210, 100, 10, 380)
w5 = Wall(150, 200, 50, 300, 100, 345, 10)
w6 = Wall(150, 200, 50, 650, 15, 10, 500)

font.init()
font = font.Font(None, 70)

win = font.render('YOU WIN!', True, (255, 215 ,0 ))
lose = font.render('YOU LOSE!', True, (180, 0 ,0 ))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

finish =  False
while True:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0,0) )

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()

        player.reset()
        player.update()

        monster.reset()
        monster.update()

        final.reset()

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win,(200,200))
            money.play()

        if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) or sprite.collide_rect(player, w2) or sprite.collide_rect(player, w3) or sprite.collide_rect(player, w4) or sprite.collide_rect(player, w5) or sprite.collide_rect(player, w6):
            finish = True
            window.blit(lose, (200,200))
            kick.play()

    display.update()
    clock.tick(FPS)
