from pygame import *
from random import randint, choice
import time
import pygame

back_img = 'road.png'
pygame.init()
win_width = 800
win_height = 700
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load(back_img), (win_width, win_height))
window.blit(back, (0, 0))


car_speed = 15
speed_road = 20
bot_car_speed = 15

class Car(sprite.Sprite):
    def __init__(self, img, width, height, x, y):
        super().__init__()

        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


    def collidelist(self, spr):
        return self.rect.colliderect(spr.rect)


        
    
class CarDrive(Car):
    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys[K_RIGHT] and not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
            self.rect.x += car_speed
        if pressed_keys[K_LEFT] and not pressed_keys[K_UP] and not pressed_keys[K_DOWN]:
            self.rect.x -= car_speed
        if pressed_keys[K_UP] and self.rect.y > 0:
            self.rect.y -= car_speed
        if pressed_keys[K_DOWN] and self.rect.y <= 555:
            self.rect.y += car_speed



class TrafficCars(Car):
    def __init__(self, img, width, height, x, y, tm):
        super().__init__(img, width, height, x, y)
        self.tm = tm

    def update(self):
        self.rect.y += bot_car_speed
        if self.rect.y > win_height:
            self.kill()
        


class Wall(pygame.sprite.Sprite):
    def __init__(self, x=20, y=0, width=120, height=120):
        pygame.sprite.Sprite.__init__(self)
        # картинка - новый прямоугольник нужных размеров:
        self.image = pygame.Surface([width, height], SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        # self.image.fill(color)

        # создаем свойство rect 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y




# class Label():
#     def __init__(self, text, fsize=12, color=(0,0,0)) -> None:
#         self.text = text
#         self.fsize = fsize
#         self.color = color

#     def set_text(self):
#         # self.text = font.render(self.text, self.fsize, self.color)
#         self.text = pygame.font.SysFont('verdana', self.fsize).render(self.text, True, self.color)

#     def draw(self, shift_x, shift_y):
#         window.blit(self.text, (shift_x, shift_y))


# *от 170 до 580 расстояние дороги в x



# группа и объекты стен
walls = sprite.Group()
wall_right = Wall(690, 0, 10, win_height)
wall_left = Wall(110, 0, 10, win_height)
walls.add(wall_right)
walls.add(wall_left)



n_cars = ['bluecar.png', 'oceancar.png', 'yellowcar.png']
# создание машин
tr_cars = sprite.Group()
car = CarDrive('maslcar_red.png', 55, 130, 440, 560)
for i in range(1):
    traffic_car = TrafficCars('yellowcar.png',50, 100, randint(170, 580), -100, randint(1, 10))
    tr_cars.add(traffic_car)
    


shift = 0
run = True
start = time.time()
score = 0
finish = False

while run:
    # back_img = 'road.png'
    if not finish:
        # увеличение скорости пропорционально очкам
        if score >= 500: # 500
            speed_road = 25
        if score >= 1000: # 1000
            speed_road = 30
        if score >= 1500: # 1500
            speed_road = 35
            bot_car_speed = 20
        if score >= 2000: # 2000
            speed_road = 50
            bot_car_speed = 22.5
        if score >= 5000:
            speed_road = 65
            bot_car_speed = 28.5
            
        # движение дороги
        shift += speed_road
        local_shift = shift % win_height
        window.blit(back, (0, local_shift)) 
        if local_shift != 0:
            window.blit(back, (0, local_shift - win_height))

        # отрисовка и движение машин
        car.reset()
        car.update()
        tr_cars.draw(window)
        walls.draw(window)
        tr_cars.update()
        
        # надпись таймера
        timer = time.time() - start
        text = pygame.font.SysFont('verdana', 26).render('ВРЕМЯ: ' + str(int(timer)), True, (255, 255, 0))
        window.blit(text, (30, 20))

        score += 0.5
        text = pygame.font.SysFont('verdana', 26).render('СЧЕТ: ' + str(int(score)), True, (255, 255, 0))
        window.blit(text, (600, 20))


        if timer >= 60:
            back_img = 'road_night1.png'
        
        back = transform.scale(image.load(back_img), (win_width, win_height))

        # при отсутствии машин в группе благодаря kill() мы воссоздаем их заново
        if not tr_cars:
            count_cars = 5
            coor = []
            for i in range(count_cars):
                x_car = randint(170, 580)
                traffic_car = TrafficCars(choice(n_cars), 50, 100, x_car, randint(-2000, -100), randint(1, 10))
                tr_cars.add(traffic_car)
                
            # после пополнения tr_cars объектами машин, проверяем на спавн в одном и том же месте, 
            # если функция возращает нам True, то мы удаляем машину из группы
            tr_cars_list = list(tr_cars.sprites())
            for j in range(len(tr_cars_list) - 1):
                # print(tr_cars_list[j].collidelist(tr_cars_list[j+1]))
                if tr_cars_list[j].collidelist(tr_cars_list[j+1]):
                    tr_cars.remove(tr_cars.sprites()[j])
                    # print('*DEL1*')

            # for d in range(len(tr_cars_list), 1):
            #     # print(tr_cars_list[d].collidelist(tr_cars_list[d+1]))
            #     if tr_cars_list[d].collidelist(tr_cars_list[d+1]):
            #         tr_cars.remove(tr_cars.sprites()[d])
            #         # print('*DEL2*')
            # print(tr_cars_list)

                
        #     print(sprite.spritecollide(tr_cars.sprites()[i]), tr_cars.sprites()[i+1])

        # увеличение скорости
        # if timer > 15:
        #     speed_traffic_and_road = 25
        #     car_speed = 15

        # завершение игры при столкновении
        if sprite.spritecollide(car, tr_cars, False) or sprite.spritecollide(car, walls, False):
            finish = True
            window.blit(transform.scale(image.load('gameover.png'), (win_width, win_height)), (0, 0))

        
            
    
    # обработка события - выключить
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    display.update()
    pygame.time.delay(30)