import cpu
import pygame
import random

class gpu:
    def __init__(self, sizeX = 300, sizeY = 200):
        self.width, self.height = sizeX, sizeY
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.flip()
        pygame.display.set_caption("PyBit x8 GPU")

    def tick(self, screen : list[cpu.x8]):
        i = -1
        for x in range(150):
            for y in range(100):
                i += 1
                
                Color = (cpu.x8ToNum(screen[i][0]),cpu.x8ToNum(screen[i][1]),cpu.x8ToNum(screen[i][2]))
                
                if Color != (0, 0, 0):
                    pygame.draw.circle(self.screen, Color, ((x*2)+1, (y*2)+1), 2, 2)
        pygame.display.flip() 

def randomCol():
    return (cpu.x8(random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)),cpu.x8(random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)),cpu.x8(random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1),random.randint(0,1)))

