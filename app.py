from pygame import *
from random import randint, choice
import time
import pygame


pygame.init()
win_width = 800
win_height = 700
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load('road.png'), (win_width, win_height))
window.blit(back, (0, 0))

car_speed = 10
speed_road = 25


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
        if pressed_keys[K_UP] :
            self.rect.y -= car_speed
        if pressed_keys[K_DOWN]:
            self.rect.y += car_speed



class TrafficCars(Car):
    def __init__(self, img, width, height, x, y, tm):
        super().__init__(img, width, height, x, y)
        self.tm = tm

    def update(self):
        self.rect.y += 15
        if self.rect.y > win_height:
            self.kill()
        



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


n_cars = ['bluecar.png', 'oceancar.png', 'yellowcar.png']
# создание машин
tr_cars = sprite.Group()
car = CarDrive('maslcar.png', 55, 130, 440, 560)
for i in range(1):
    traffic_car = TrafficCars('yellowcar.png',50, 100, randint(170, 580), -100, randint(1, 10))
    tr_cars.add(traffic_car)
    


shift = 0
run = True
start = time.time()
finish = False

while run:
    if not finish:
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
        tr_cars.update()

        # надпись таймера
        timer = time.time() - start
        text = pygame.font.SysFont('verdana', 26).render('ВРЕМЯ:' + str(int(timer)), True, (255, 255, 0))
        window.blit(text, (30, 20))

        
       
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
                print(tr_cars_list[j].collidelist(tr_cars_list[j+1]))
                if tr_cars_list[j].collidelist(tr_cars_list[j+1]):
                    tr_cars.remove(tr_cars.sprites()[j])
                    print('*DEL*')
            print(tr_cars_list)

                
        #     print(sprite.spritecollide(tr_cars.sprites()[i]), tr_cars.sprites()[i+1])

        # увеличение скорости
        # if timer > 15:
        #     speed_traffic_and_road = 25
        #     car_speed = 15

        # завершение игры при столкновении
        if sprite.spritecollide(car, tr_cars, False):
            finish = True
    
            window.blit(transform.scale(image.load('gameover.png'), (win_width, win_height)), (0, 0))

        
            
    
    # обработка события - выключить
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    display.update()
    pygame.time.delay(30)