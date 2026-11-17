# Tutaj pisz swój kod, młody padawanie ;-)
import pygame
import random
import sys

# ================== INICJALIZACJA ==================
pygame.init()
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("STEAL A BRAINROT 2D")

FONT = pygame.font.SysFont("arial", 24)
CLOCK = pygame.time.Clock()

# ================== KOLORY ==================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (180, 0, 255)

# ================== KLASY ==================

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 40, 40)
        self.speed = 5
        self.brainrots = 0

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.clamp_ip(WIN.get_rect())

    def draw(self):
        pygame.draw.rect(WIN, BLUE, self.rect)


class Brainrot:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT - 50),
            25,
            25
        )

    def draw(self):
        pygame.draw.rect(WIN, YELLOW, self.rect)


class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            40,
            40
        )
        self.speed = 2
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if random.randint(0, 100) < 2:
            self.direction = random.choice(["up", "down", "left", "right"])

        self.rect.clamp_ip(WIN.get_rect())

    def draw(self):
        pygame.draw.rect(WIN, RED, self.rect)


class Base:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - 120, HEIGHT - 120, 100, 100)

    def draw(self):
        pygame.draw.rect(WIN, GREEN, self.rect)


# ================== FUNKCJE ==================

def draw_ui(player):
    text = FONT.render(f"Brainroty: {player.brainrots}", True, WHITE)
    WIN.blit(text, (10, 10))


def draw_window(player, brainrots, enemies, base):
    WIN.fill(BLACK)

    base.draw()

    for b in brainrots:
        b.draw()

    for e in enemies:
        e.draw()

    player.draw()
    draw_ui(player)

    pygame.display.update()


# ================== GŁÓWNA PĘTLA ==================

def main():
    player = Player()
    base = Base()

    brainrots = [Brainrot() for _ in range(5)]
    enemies = [Enemy() for _ in range(3)]

    run = True
    while run:
        CLOCK.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        player.move(keys)

        # RUCH WROGÓW
        for enemy in enemies:
            enemy.move()

            if enemy.rect.colliderect(player.rect):
                if player.brainrots > 0:
                    player.brainrots -= 1

        # ZBIERANIE BRAINROTÓW
        for b in brainrots[:]:
            if player.rect.colliderect(b.rect):
                player.brainrots += 1
                brainrots.remove(b)
                brainrots.append(Brainrot())

        # ODDANIE DO BAZY
        if player.rect.colliderect(base.rect):
            if player.brainrots > 0:
                player.brainrots += 0  # miejsce na przyszły system monet

        draw_window(player, brainrots, enemies, base)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
