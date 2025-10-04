import pygame
import random
import sys

# --- Initialize Pygame ---
pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World-Class Plane Crash Simulation")
clock = pygame.time.Clock()

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# --- Fonts ---
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 26)

# --- Plane options (add more if you want) ---
plane_options = {
    "Jet Plane": "plane1.png",
    "Propeller Plane": "plane2.png"
}

plane_width = 100
plane_height = 100


# --- Plane Selection Menu ---
def choose_plane():
    """Display plane selection menu and return selected plane image."""
    selecting = True
    plane_img = None

    while selecting:
        screen.fill(SKY_BLUE)
        y_offset = 150
        title = font.render("✈️ Select Your Plane!", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Draw clickable plane names
        button_rects = {}
        for name, path in plane_options.items():
            text_surf = small_font.render(name, True, WHITE)
            rect = text_surf.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(text_surf, rect)
            button_rects[name] = (rect, path)
            y_offset += 60

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, (rect, path) in button_rects.items():
                    if rect.collidepoint(event.pos):
                        plane_img = pygame.image.load(path)
                        plane_img = pygame.transform.scale(plane_img, (plane_width, plane_height))
                        selecting = False
                        break

        pygame.display.update()
        clock.tick(30)

    return plane_img


# --- Simulation Function ---
def run_simulation(plane_img):
    plane_x = 50
    plane_y = 200
    plane_speed = 6
    stability = 100
    stability_max = 100
    gravity = 0.8

    obstacles = ["Turbulence", "Bird Strike", "Engine Failure", "Storm"]
    damage = {"Turbulence": 10, "Bird Strike": 20, "Engine Failure": 30, "Storm": 15}

    running = True
    while running:
        screen.fill(SKY_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Random event ---
        if random.random() < 0.02:
            event = random.choice(obstacles)
            stability -= damage[event]
            stability = max(0, stability)
            print(f"{event}! Stability drops to {stability}")
            plane_y += damage[event] // 2

        # --- Gravity ---
        plane_y += gravity
        plane_y = max(0, min(plane_y, HEIGHT - plane_height))

        # --- Move forward ---
        plane_x += plane_speed
        if plane_x > WIDTH - 100:
            plane_x = 50  # wrap around

        # --- Draw plane ---
        screen.blit(plane_img, (plane_x, plane_y))

        # --- Stability bar ---
        pygame.draw.rect(screen, RED, (50, 50, 200, 25))
        green_width = 200 * (stability / stability_max)
        pygame.draw.rect(screen, GREEN, (50, 50, green_width, 25))
        text = small_font.render(f"Stability: {stability}", True, BLACK)
        screen.blit(text, (50, 20))

        # --- Check for crash ---
        if stability <= 0 or plane_y >= HEIGHT - plane_height:
            crash_text = font.render("💥 PLANE CRASHED! Simulation Over 💥", True, RED)
            screen.blit(crash_text, (WIDTH//2 - 300, HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(3000)
            running = False

        pygame.display.update()
        clock.tick(30)


# --- Main program ---
plane_img = choose_plane()
run_simulation(plane_img)

pygame.quit()
sys.exit()

