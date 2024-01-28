from pygame import *
init()
font.init()
black = (0, 0, 0)
font = font.SysFont('Timws New Roman', 70)
finish = False
run = True
W = 700
H = 500
back = (200, 255, 255) 
Screen_size = (W, H)
window = display.set_mode(Screen_size)
FPS = 60
window.fill(back)
display.set_caption('Нутипавот')
clock = time.Clock()
GREEN = (20, 255, 50)


class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        self.rect.x += self.x_speed
        pl_td = sprite.spritecollide(self, brs, False)
        if self.x_speed > 0:
            for p in pl_td:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in pl_td:
                self.rect.left = max(self.rect.left, p.rect.right)
        self.rect.y += self.y_speed
        pl_td = sprite.spritecollide(self, brs, False)
        if self.y_speed > 0:
            for p in pl_td:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in pl_td:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('weapon.png', 30, 10, self.rect.right, self.rect.centery, 20)
        bullet.reset()
        bul.add(bullet)


class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.speed = speed
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= 400:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= W + 10:
            self.kill()

ha = font.render('YOU WIN', True, black)
no = font.render('YOU LOSE', True, black)
sad = transform.scale(image.load('mkadm.png'), Screen_size)
win = transform.scale(image.load('win.jpg'), Screen_size)
player1 = Player('hero.png', 80, 80, 5, 400, 0, 0)
final = GameSprite('final.png', 60, 90, 500, 150)
w1 = GameSprite('wall.png', 40, 400, 250, 150)
w2 = GameSprite('wall.png', 150, 40, 100, 250)
w3 = GameSprite('wall.png', 700, 5, 0, 0)
w4 = GameSprite('wall.png', 5, 500, 0, 0)
w5 = GameSprite('wall.png', 5, 500, 700, 0)
w6 = GameSprite('wall.png', 700, 5, 0, 500)
monster = Enemy('mkadm.png', 100, 100, 400, 90, 10)
mon = sprite.Group()
mon.add(monster)
bul = sprite.Group()
brs = sprite.Group()
brs.add(w1)
brs.add(w2)
brs.add(w3)
brs.add(w4)
brs.add(w5)
brs.add(w6)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                    player1.y_speed = -5
            if e.key == K_DOWN:
                    player1.y_speed = 5
            if e.key == K_RIGHT:
                    player1.x_speed = 5
            if e.key == K_LEFT:
                    player1.x_speed = -5
            if e.key == K_SPACE:
                player1.fire()
        elif e.type == KEYUP:
            if e.key == K_UP:
                player1.y_speed = 0
            if e.key == K_DOWN:
                player1.y_speed = 0
            if e.key == K_RIGHT:
                player1.x_speed = 0
            if e.key == K_LEFT:
                player1.x_speed = 0
    if finish == False:
        window.fill(GREEN)
        player1.reset()
        mon.draw(window)
        final.reset()
        w1.reset()
        w2.reset()
        w3.reset()
        w4.reset()
        w5.reset()
        w6.reset()
        player1.update()
        monster.update()
        bul.update()
        bul.draw(window)

        if sprite.collide_rect(player1, final):
            finish = True
            window.blit(win, (0, 0))
            window.blit(ha, (220, 220))
        if sprite.spritecollide(player1, mon, False):
            finish = True
            window.blit(sad, (0, 0))
            window.blit(no, (220, 220))
        sprite.groupcollide(bul, mon, True, True)
        sprite.groupcollide(bul, brs, True, False)
    time.delay(50)
    display.update()


