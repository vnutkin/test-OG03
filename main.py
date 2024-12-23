
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

class Orbit_point:
    def __init__(self,r_planet,h_orbit,g_planet,width_screen,height_screen,frac_y,mash_k_times,time_acceleration_factor):
        self.r_planet = r_planet
        self.h_orbit = h_orbit
        self.g_planet = g_planet
        self.width_screen = width_screen
        self.height_screen = height_screen
        self.frac_y = frac_y
        self.mash_k_times = mash_k_times
        self.time_acceleration_factor = time_acceleration_factor
        self.mash_x = float(width_screen/h_orbit)
        self.mash_y = float(height_screen/h_orbit)
        self.x_0 = 0
        self.y_0 = self.h_orbit

    def polar_to_abs(self,r,phi):
        __x = float(r) * math.cos(phi)
        __y = float(r) * math.sin(phi)
        return __x, __y

    def abs_to_scr(self,x, y):
        __x = int((x - self.x_0)* self.mash_x)
        __y = int((y - self.y_0) / self.mash_y)
        if __y >= int(self.heigth_screen * self.frac_y) :
            self.mash_y = float(self.mash_y / self.mash_k_times)
            self.mash_x = float(self.mash_x / self.mash_k_times)
            self.y_0 = y
            if __x <= self.width_screen // 2:
                self.x_0 = x + (self.width_screen // 2) * self.mash_x
        if __x >= self.width_screen :
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
    def dif_eqv(self,time,param,vector_x,vector_dx):
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
        if vr == 0:
            alpha = math.pi / 2
        else:
            alpha = math.atan(math.fabs(vt / vr))
        engine_power = fuel_cons * self.gas_flow_rate
        engine_power_n = engine_power * math.cos(alpha)
        engine_power_t = engine_power * math.sin(alpha)
        dvr = vt * vt / r_h - g_planet - engine_power_n / (self.massa + fuel)
        dphi = vphi
        dvphi = - engine_power_t / (r_h * (self.massa + fuel))
        #    dr, dvr, dphi, dvphi, dfuel
        vector_dx = [dr,dvr,dphi,dvphi,dfuel]
orbit_point = Orbit_point(1737400,100000,1.625,int(WIDTH * 0.7 ),HEIGHT,0.7,5,5)
lunnik = Dinamic_object(9200,6000,3500)
param = [0,orbit_point.r_planet + orbit_point.h_orbit,orbit_point.g_planet]
vt = math.sqrt(orbit_point.g_planet * (orbit_point.r_planet + orbit_point.h_orbit))

vector_x = [orbit_point.r_planet + orbit_point.h_orbit,0,0,vt / (orbit_point.r_planet + orbit_point.h_orbit), lunnik.fuel ]
vector_dx = [0,0,0,0,0]

# Цикл игры
running = True
current_time =0
delta_time = 0.01
n_times = int(float(1 / FPS) / delta_time) * orbit_point.time_acceleration_factor
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
        lunnik.dif_eqv(current_time,param,vector_x,vector_dx )
        for j in range(0,len(vector_x)):
            vector_x
            vector_x[j] = vector_x[j] + vector_dx[j] * delta_time
        current_time += delta_time
    print(current_time,vector_x, vector_dx)
pygame.quit()
sys.exit()


