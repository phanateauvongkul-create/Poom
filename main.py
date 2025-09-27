import pygame
import random
import sys

# --- Initialize Pygame ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✈️ World-Class Plane Crash Simulation")
clock = pygame.time.Clock()

# --- Colors ---
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# --- Load and resize plane image ---
plane_img = pygame.image.load("plane.gif")  # ensure this exists
plane_width, plane_height = 100, 100
plane_img = pygame.transform.scale(plane_img, (plane_width, plane_height))

# --- Plane setup ---
plane_x, plane_y = 100, 200
plane_speed_y = 0

# --- Stability setup ---
stability = 100
MAX_STABILITY = 100

# --- Obstacles setup ---
obstacles = ["🌪️ Turbulence", "🐦 Bird Strike", "🔥 Engine Failure", "🌧️ Storm"]
damage = {"🌪️ Turbulence": 10,
          "🐦 Bird Strike": 20,
          "🔥 Engine Failure": 30,
          "🌧️ Storm": 15}

# --- Font ---
font = pygame.font.SysFont("Arial", 24)

# --- Simulation loop ---
round_num = 1
running = True
event_timer = 0  # timer to trigger events every 2 seconds

while running:
    screen.fill(SKY_BLUE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Trigger obstacle every 2 seconds
    event_timer += clock.get_time()
    if event_timer > 2000:  # milliseconds
        event_timer = 0
        if random.random() < 0.5:
            obstacle = random.choice(obstacles)
            stability -= damage[obstacle]
            stability = max(stability, 0)
            print(f"Round {round_num}: {obstacle}! Stability drops to {stability}%")
            plane_speed_y += damage[obstacle] * 0.2  # plane descends when hit
        else:
            print(f"Round {round_num}: Smooth flight. Stability unchanged.")
        round_num += 1

    # Update plane position (simulating gravity when stability is lost)
    plane_y += plane_speed_y
    plane_speed_y *= 0.95  # damping to smooth motion

    # Draw plane
    screen.blit(plane_img, (plane_x, int(plane_y)))

    # Draw stability bar
    bar_width = 300
    bar_height = 25
    bar_x = 50
    bar_y = 50
    pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * (stability / MAX_STABILITY)), bar_height))
    text_surf = font.render(f"Stability: {stability}%", True, WHITE)
    screen.blit(text_surf, (bar_x, bar_y - 30))

    # Check crash
    if stability <= 0 or plane_y + plane_height > HEIGHT:
        print("Plane has crashed!")
        crash_text = font.render("💥 Plane Crashed!", True, RED)
        screen.blit(crash_text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
