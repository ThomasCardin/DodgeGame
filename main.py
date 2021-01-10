import pygame
import random
import time

WIDTH = 1200
HEIGHT = 800
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15

BLOCK_WIDTH = 15
BLOCK_HEIGHT = 15

class Blocks(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BLOCK_WIDTH, BLOCK_HEIGHT))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

        random_x_point = random.randint(0 , WIDTH)
        self.rect.center = (random_x_point, 0)
    
    def update(self, player_y, player_x):
        global nb_score
        gravity = random.randint(1, 10)
        self.rect.y += gravity

        if self.rect.bottom > player_y:
            if self.rect.left < player_x + PLAYER_WIDTH and self.rect.right > player_x or self.rect.left + BLOCK_WIDTH < player_x + PLAYER_WIDTH and self.rect.right > player_x + PLAYER_WIDTH:
               Game_over()

        if self.rect.y >= HEIGHT - 100:
            self.rect.y = 0
            nb_score += 1

     
class Player():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        rect = pygame.draw.rect(DISPLAY, (0, 254, 0), (self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def handle_keys(self):
        key = pygame.key.get_pressed()
        distance = 5
      
        if key[pygame.K_a] or key[pygame.K_LEFT] and self.x != 0:
            self.x -= distance
        if key[pygame.K_d] or key[pygame.K_RIGHT] and self.x != WIDTH - PLAYER_WIDTH:
            self.x += distance


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def message_display(text):
    font = pygame.font.Font('freesansbold.ttf', 100)
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = ((WIDTH / 2), (HEIGHT / 2))

    font = pygame.font.Font('freesansbold.ttf', 50)
    str_nb_score = 'Score: ' + str(nb_score)
    TextSurf_score, TextRect_score = text_objects(str_nb_score, font)
    TextRect_score = ((WIDTH / 2) - 100, (HEIGHT / 2) + 100)

    DISPLAY.blit(TextSurf, TextRect)
    DISPLAY.blit(TextSurf_score, TextRect_score)

    pygame.display.update()
    time.sleep(4)


def show_score(text):
    font = pygame.font.Font('freesansbold.ttf', 18)
    TextSurf, TextRect = text_objects(text, font)
    TextSurf2, TextRect2 = text_objects('Score: ', font)
    TextRect.center = (70, 20)
    TextRect2.center = (30, 20)
    DISPLAY.blit(TextSurf2, TextRect2)
    DISPLAY.blit(TextSurf, TextRect)
    pygame.display.update()

def Game_over():
    message_display('Game Over')
    main()


def main():
    global nb_score
    blocks_group = pygame.sprite.Group()
    nb_score = 0
    nb_spawn_new_block = 0

    pygame.init()
    pygame.display.set_caption('Dodge')
    clock = pygame.time.Clock()
    
    # Creating players and blocks
    player = Player((WIDTH / 2), (HEIGHT - 100))

    blocks_group.add((Blocks()))

    while True:
        # clock tick + score
        clock.tick(60) # speed
        nb_spawn_new_block += 1

        # add block
        if nb_spawn_new_block % 10 == 0:
            blocks_group.add(Blocks())

        # show current score
        show_score(str(nb_score))

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        DISPLAY.fill((0, 0, 0))

        # handle keys - PLAYER
        player.handle_keys()
        player.draw()

        # update - BLOCKS
        blocks_group.update(player.y, player.x)
        blocks_group.draw(DISPLAY)

        pygame.display.update()

main()