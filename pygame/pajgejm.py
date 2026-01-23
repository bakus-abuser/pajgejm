import pygame
from sys import exit
from random import randint

# ================== KLASY ==================

class Obstacle:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = image.get_rect(midbottom=(x, y))
        self.scored = False

    def update(self):
        self.rect.x -= 5

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ================== FUNKCJE ==================

def draw_score():
    score_surface = font.render(str(score), False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(score_surface, score_rect)
    return score


# ================== INIT ==================

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("blyblybly")

clock = pygame.time.Clock()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

# ================== GRAFIKA ==================

sky = pygame.image.load("zdjecia/Sky.png").convert_alpha()
ground = pygame.image.load("zdjecia/ground.png").convert_alpha()

snail = pygame.image.load("zdjecia/slimak/snail1.png").convert_alpha()
fly = pygame.image.load("zdjecia/mucha/Fly1.png").convert_alpha()

player = pygame.image.load("zdjecia/gracz/player_walk_1.png").convert_alpha()
player_rect = player.get_rect(midbottom=(80, 280))

player_stand = pygame.image.load("zdjecia/gracz/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

title = font.render("kliknij mnie zeby zaczac", False, "black")
title_rect = title.get_rect(center=(400, 80))

zdjencie = pygame.image.load('zdjecia/gracz/player_stand.png').convert_alpha()





# ================== ZMIENNE ==================

obstacles = []
score = 0
gravity = 0
game_active = False


SPAWN_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_OBSTACLE, 1400)
pygame.display.set_icon(zdjencie)
# ================== LOOP ==================

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # START GRY
        if not game_active and event.type == pygame.MOUSEBUTTONDOWN:
            if player_stand_rect.collidepoint(event.pos):
                game_active = True
                obstacles.clear()
                score = 0
                gravity = 0
                player_rect.midbottom = (80, 280)

        # SKOK
        if game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 280:
                gravity = -20

        # SPAWN PRZESZKÓD
        if event.type == SPAWN_OBSTACLE and game_active:
            if randint(0, 2):
                obstacles.append(Obstacle(snail, randint(900, 1100), 280))
            else:
                obstacles.append(Obstacle(fly, randint(900, 1100), 180))

    # ================== GRA ==================

    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 280))

        # GRACZ
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= 280:
            player_rect.bottom = 280
        screen.blit(player, player_rect)

        # PRZESZKODY
        for obs in obstacles:
            obs.update()
            obs.draw(screen)

            # KOLIZJA = KONIEC GRY
            if player_rect.colliderect(obs.rect):
                game_active = False

            # LICZENIE WYNIKU (RAZ!)
            if obs.rect.right < player_rect.left and not obs.scored:
                score += 1
                obs.scored = True

        obstacles = [obs for obs in obstacles if obs.rect.right > -100]

        draw_score()

    # ================== MENU ==================

    else:
        screen.fill((94, 129, 162))
        screen.blit(title, title_rect)
        screen.blit(player_stand, player_stand_rect)

        if score:
            twoj_wynik = font.render(f'Twoj Wynik: {score}' , False, (111,196,169))
            twoj_wynik_rect = twoj_wynik.get_rect(center=(400,320))
            screen.blit(twoj_wynik,twoj_wynik_rect)


    pygame.display.update()
    clock.tick(60)