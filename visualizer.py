import pygame
import pygame.draw


def vizualizer():
    pygame.init()
    pygame.display.set_caption('Waveform Visualizer')

    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 900

    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    middle = pygame.Rect(0,SCREEN_HEIGHT/2,SCREEN_WIDTH,1)
    top = pygame.Rect(0,SCREEN_HEIGHT*1/5,SCREEN_WIDTH,1)
    bottom = pygame.Rect(0,SCREEN_HEIGHT*5/6,SCREEN_WIDTH,1)

    reading = []
    draw_loc = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('grey')

        pygame.draw.rect(screen, 'red', middle)
        pygame.draw.rect(screen, 'black', top)
        pygame.draw.rect(screen, 'black',bottom)

        if len(reading) >= SCREEN_WIDTH:
            draw_loc = +1
            reading.pop(0)

        reading.append(draw_loc)

        for i, x in enumerate(reading):
            pygame.draw.rect(screen,'blue', pygame.Rect(i,x+SCREEN_HEIGHT/2,1,1))

        pygame.display.flip()

        clock.tick(60)


if __name__=="__main__":
    vizualizer()