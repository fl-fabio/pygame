import pygame
import random
import sys


WIDTH = 800
HEIGHT = 600

PLAYER_SIZE = 40
ENEMY_SIZE = 40
COIN_SIZE = 20

BACKGROUND_COLOR = (30, 30, 30)
PLAYER_COLOR = (50, 150, 255)
ENEMY_COLOR = (255, 80, 80)
COIN_COLOR = (80, 255, 120)
TEXT_COLOR = (255, 255, 255)


def create_game_state():
    player = {
        "x": WIDTH // 2,
        "y": HEIGHT // 2,
        "speed": 5
    }

    enemy = {
        "x": 100,
        "y": 100,
        "speed": 2
    }

    coin = {
        "x": random.randint(0, WIDTH - COIN_SIZE),
        "y": random.randint(0, HEIGHT - COIN_SIZE)
    }

    score = 0

    return player, enemy, coin, score


def draw_text(screen, font, text, x, y):
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, (x, y))


def move_player(player, keys):
    if keys[pygame.K_LEFT]:
        player["x"] -= player["speed"]
    if keys[pygame.K_RIGHT]:
        player["x"] += player["speed"]
    if keys[pygame.K_UP]:
        player["y"] -= player["speed"]
    if keys[pygame.K_DOWN]:
        player["y"] += player["speed"]

    player["x"] = max(0, min(WIDTH - PLAYER_SIZE, player["x"]))
    player["y"] = max(0, min(HEIGHT - PLAYER_SIZE, player["y"]))


def move_enemy(enemy, player):
    if enemy["x"] < player["x"]:
        enemy["x"] += enemy["speed"]
    elif enemy["x"] > player["x"]:
        enemy["x"] -= enemy["speed"]

    if enemy["y"] < player["y"]:
        enemy["y"] += enemy["speed"]
    elif enemy["y"] > player["y"]:
        enemy["y"] -= enemy["speed"]


def respawn_coin(coin):
    coin["x"] = random.randint(0, WIDTH - COIN_SIZE)
    coin["y"] = random.randint(0, HEIGHT - COIN_SIZE)


def create_rectangles(player, enemy, coin):
    player_rect = pygame.Rect(player["x"], player["y"], PLAYER_SIZE, PLAYER_SIZE)
    enemy_rect = pygame.Rect(enemy["x"], enemy["y"], ENEMY_SIZE, ENEMY_SIZE)
    coin_rect = pygame.Rect(coin["x"], coin["y"], COIN_SIZE, COIN_SIZE)

    return player_rect, enemy_rect, coin_rect


def draw_game(screen, font, player_rect, enemy_rect, coin_rect, score):
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)
    pygame.draw.rect(screen, ENEMY_COLOR, enemy_rect)
    pygame.draw.rect(screen, COIN_COLOR, coin_rect)

    draw_text(screen, font, f"Score: {score}", 20, 20)

    pygame.display.flip()


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smart Chase")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    player, enemy, coin, score = create_game_state()

    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        move_player(player, keys)
        move_enemy(enemy, player)

        player_rect, enemy_rect, coin_rect = create_rectangles(player, enemy, coin)

        if player_rect.colliderect(coin_rect):
            score += 1
            respawn_coin(coin)

        if player_rect.colliderect(enemy_rect):
            running = False

        draw_game(screen, font, player_rect, enemy_rect, coin_rect, score)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()