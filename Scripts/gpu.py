import cpu
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random

class gpu:
    def __init__(self, sizeX = 300, sizeY = 200):
        self.width, self.height = sizeX, sizeY
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()
        name = "$gpu.name $gpu.intsize $gpu.hertz GPU".replace("$gpu.name", cpu.SPECS["GPU"]["Name"]).replace("$version", cpu.VERSION).replace("$gpu.intsize", cpu.SPECS["GPU"]["IntSize"]).replace("$gpu.hertz", cpu.SPECS["GPU"]["Hertz"])
        pygame.display.set_caption(name)
        print(f"\033[32;1mSuccesfully started {name}\033[0m")

    def tick(self, screen : list[cpu.x8]):
        i = -1
        for y in range(100):
            for x in range(150):
                i += 1
                
                Color = (cpu.x8ToNum(screen[i][0]),cpu.x8ToNum(screen[i][1]),cpu.x8ToNum(screen[i][2]))
                
                if (Color[0] + Color[1] + Color[2]) > 3:
                    pygame.draw.circle(self.screen, Color, ((x*2), (y*2)), 1, 150)
                    #pygame.draw.circle(self.screen, Color, ((x*2), (y*2)+1), 2, 150)
                    #pygame.draw.circle(self.screen, Color, ((x*2)+1, (y*2)), 2, 150)
                    #pygame.draw.circle(self.screen, Color, ((x*2)+1, (y*2)+1), 2, 150)
        pygame.display.flip() 

def randomCol():
    return (cpu.x8(random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)),cpu.x8(random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)),cpu.x8(random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)))
