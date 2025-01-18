
import math
import pygame
import random
import sys
WIDTH = 1200
HEIGHT = 800
FPS = 30
# Создаем игру и окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Игра Посадка лунника')
clock = pygame.time.Clock()
lun_orig = pygame.image.load('img/lunnic_without_flames.jpg')
lun_width = 80
lun_height = 80
lun_img = pygame.transform.scale(lun_orig, (lun_width, lun_height))

class Orbit_point:
    def __init__(self,r_planet,h_orbit,g_planet,width_screen,height_screen,frac_x,frac_y,mash_k_times,time_acceleration_factor):

        
        self.r_planet = r_planet
        self.h_orbit = h_orbit
        self.g_planet = g_planet
        self.width_screen = width_screen
        self.height_screen = height_screen
        self.frac_x = frac_x
        self.frac_y = frac_y
        self.mash_k_times = mash_k_times
        self.time_acceleration_factor = time_acceleration_factor
        self.mash_x = float(width_screen / (self.g_planet+h_orbit) * self.frac_x)
        self.mash_y = float(height_screen/(self.g_planet+h_orbit))
        self.x_0 = 0.0
        self.y_0 = self.r_planet + self.h_orbit
        self.width_x = int(self.width_screen * self.frac_x)
        self.beg_x = self.width_screen-self.width_x
    def polar_to_scr(self,r,phi):
        __xa = float(r) * math.sin(phi)
        __ya = float(r) * math.cos(phi)
        __x = int((__xa - self.x_0)* self.mash_x)
        __y = - int((__ya - self.y_0) / self.mash_y)
        if __y >= int(self.height_screen * self.frac_y) :
            self.mash_y = float(self.mash_y / self.mash_k_times)
            self.mash_x = float(self.mash_x / self.mash_k_times)
            self.x_0 = 0.0
            self.y_0 = r
            if __x <= self.width_x // 2:
                self.x_0 =  (self.width_x // 2) * self.mash_x
        if __x >= int(self.width_screen * self.frac_x):
            self.x_0 = 0.0
            self.y_0 = r
        return __x + self.beg_x, __y

    def abs_to_scr(self,x, y):
        __x = int((x - self.x_0)* self.mash_x)
        __y = - int((y - self.y_0) / self.mash_y)
        if __y >= int(self.height_screen * self.frac_y) :
            self.mash_y = float(self.mash_y / self.mash_k_times)
            self.mash_x = float(self.mash_x / self.mash_k_times)
            self.y_0 = y
            if __x <= self.width_screen // 2:
                self.x_0 = x + (self.width_screen // 2) * self.mash_x
        if __x >= int(self.width_screen * self.frac_x):
            self.x_0 = x
        return __x, __y
    def set_init_point(self):
        self.x_0 = 0
        self.y_0 = self.h_orbit

class Dinamic_object:
    def __init__(self,massa,fuel,gas_flow_rate):
        self.massa = massa
        self.fuel = fuel
        self.gas_flow_rate = gas_flow_rate
    def dif_eqv(self,time,param,vector_x):
        fuel_cons = param[0]
        r_h = param[1]
        g_planet = param[2]
    #     r, vr, phi, vphi, fuel
        r = vector_x[0]
        vr = vector_x[1]
        phi = vector_x[2]
        vphi = vector_x[3]
        fuel = vector_x[4]
        dfuel = -fuel_cons
        dr = vr
        vt = float(vphi * r_h)
        alpha = math.atan2(vr , vt)
        engine_power = fuel_cons * self.gas_flow_rate
        engine_power_n = engine_power * math.sin(alpha)
        engine_power_t = engine_power * math.cos(alpha)
        dvr = vt * vt / r_h - g_planet + engine_power_n / (self.massa + fuel)
        dphi = vphi
        dvphi =  engine_power_t / (r_h * (self.massa + fuel))
        #    dr, dvr, dphi, dvphi, dfuel
        return [dr,dvr,dphi,dvphi,dfuel]
orbit_point = Orbit_point(1737400.0,100000.0,1.625,WIDTH,HEIGHT,0.8,0.7,5,1)
lunnik = Dinamic_object(9200.0,6000.0,3500.0)
param = [0.0,orbit_point.r_planet + orbit_point.h_orbit,orbit_point.g_planet]
vt = math.sqrt(orbit_point.g_planet * (orbit_point.r_planet + orbit_point.h_orbit))

vector_x = [orbit_point.r_planet + orbit_point.h_orbit,0.0,0.0,vt / (orbit_point.r_planet + orbit_point.h_orbit), lunnik.fuel ]
vector_dx = [0.0,0.0,0.0,0.0,0.0]

# Цикл игры
running = True
current_time =0
delta_time = 0.01
n_times = int(float(1.0 / FPS) / delta_time) * orbit_point.time_acceleration_factor
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка мыши
                mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(0,n_times):
        vector_dx = lunnik.dif_eqv(current_time,param,vector_x )
        for j in range(0,len(vector_x)):
            vector_x[j] = vector_x[j] + vector_dx[j] * delta_time
        current_time += delta_time
    print(current_time,vector_x, vector_dx)
    x_scr, y_scr = orbit_point.polar_to_scr(vector_x[0],vector_x[2])
    if y_scr >int(HEIGHT * orbit_point.frac_y):
        vector_x[2] = 0.0
    if y_scr > WIDTH:
        running = False
    else:
        screen.blit(lun_img, (x_scr, y_scr))
    print(x_scr, y_scr)
# Обновление экрана
    pygame.display.flip()

pygame.quit()
sys.exit()


