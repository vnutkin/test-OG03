
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
pygame.display.set_caption("Игра Тир")
clock = pygame.time.Clock()

class Orbit_point:
    def __init__(self,r_planet,h_orbit,phi,x_abs,y_abs,width_screen,heigth_screen,x_screen,y_screen,frac_y,mash_k_times):
        self.r_planet = r_planet
        self.h_orbit = h_orbit
        self.phi = phi
        self.x_abs = x_abs
        self.y_abs = y_abs
        self.width_screen = width_screen
        self.heigth_screen = heigth_screen
        self.x_screen = x_screen
        self.y_screen = y_screen
        self.frac_y = frac_y
        self.mash_k_times = mash_k_times
        self.mash_x = float(width_screen/h_orbit)
        self.mash_y = float(heigth_screen/h_orbit)
        self.y_0 = h_orbit
        self.x_0 = 0

    def polar_to_abs(r,phi):
        __x = r * math.cos(phi)
        __y = r * math.sin()
        return __x, __y

    def abs_to_scr(self,x, y):
        __x = int((x - x_0)* self.mash_x)
        __y = int((y - y_0) / self.mash_y)
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
    def __init__(self,massa,fuel,coef_force):
        self.massa = massa
        self.fuel = fuel
        self.coef_force = coef_force
    def dif_eqv(self,time,fuel_cons,(r,vr,phi,vphi)):