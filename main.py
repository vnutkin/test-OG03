import math
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
        if __y > int(elf.heigth_screen * frac_y) :
            self.mash_y = float(self.mash_y / self.mash_k_times)
            self.mash_x = float(self.mash_x / self.mash_k_times)

