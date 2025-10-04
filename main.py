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
    "Jet Plane": "plane1.jpg",
    "Propeller Plane": "plane2.jpg"
}

plane_width = 100
plane_height = 100

# --- Initialize Pygame ---
pygame.init()

# --- Display Constants ---
WIDTH = 800
HEIGHT = 600
FPS = 30

# --- Plane Constants ---
PLANE_WIDTH = 80
PLANE_HEIGHT = 50
PLANE_INITIAL_X = 50
PLANE_INITIAL_Y = 200
PLANE_SPEED = 6
PLANE_WRAP_THRESHOLD = 100

# --- Physics Constants ---
GRAVITY = 0.8

# --- Stability Constants ---
STABILITY_INITIAL = 100
STABILITY_MAX = 100
STABILITY_BAR_X = 50
STABILITY_BAR_Y = 50
STABILITY_BAR_WIDTH = 200
STABILITY_BAR_HEIGHT = 25
STABILITY_TEXT_Y = 20

# --- Menu Constants ---
MENU_TITLE_Y = 50
MENU_START_Y = 150
MENU_BUTTON_SPACING = 60

# --- Event Constants ---
EVENT_PROBABILITY = 0.02
TURBULENCE_DAMAGE = 10
BIRD_STRIKE_DAMAGE = 20
ENGINE_FAILURE_DAMAGE = 30
STORM_DAMAGE = 15

# --- Game Over Constants ---
CRASH_MESSAGE_DELAY = 3000
CRASH_MESSAGE_X_OFFSET = 300

# --- Obstacles and Damage ---
OBSTACLES = ["Turbulence", "Bird Strike", "Engine Failure", "Storm"]
# --- Obstacle Images ---
OBSTACLE_IMAGES = {
    "Turbulence": "turbulence.png",
    "Bird Strike": "bird.png",
    "Engine Failure": "fire.png",
    "Storm": "storm.png"
}
DAMAGE = {
    "Turbulence": TURBULENCE_DAMAGE,
    "Bird Strike": BIRD_STRIKE_DAMAGE,
    "Engine Failure": ENGINE_FAILURE_DAMAGE,
    "Storm": STORM_DAMAGE
}
# --- Event Display Constants ---
EVENT_DISPLAY_DURATION = 90  # frames (3 seconds at 30 FPS)
EVENT_IMAGE_WIDTH = 100
EVENT_IMAGE_HEIGHT = 100
EVENT_IMAGE_X = 350
EVENT_IMAGE_Y = 250
EVENT_TEXT_Y_OFFSET = 120

# --- Plane Selection Menu ---
def choose_plane():
    """Display plane selection menu and return selected plane image."""
    selecting = True
    choosen_plane_img = None

    while selecting:
        screen.fill(SKY_BLUE)
        y_offset = MENU_START_Y
        title = font.render("Select Your Plane!", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, MENU_TITLE_Y))

        # Draw clickable plane names
        button_rects = {}
        for name, path in plane_options.items():
            text_surf = small_font.render(name, True, WHITE)
            rect = text_surf.get_rect(center=(WIDTH // 2, y_offset))
            screen.blit(text_surf, rect)
            button_rects[name] = (rect, path)
            y_offset += MENU_BUTTON_SPACING

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for name, (rect, path) in button_rects.items():
                    if rect.collidepoint(event.pos):
                        choosen_plane_img = pygame.image.load(path)
                        choosen_plane_img = pygame.transform.scale(choosen_plane_img, (PLANE_WIDTH, PLANE_HEIGHT))
                        selecting = False
                        break

        pygame.display.update()
        clock.tick(FPS)

    return choosen_plane_img


# --- Simulation Function ---
def run_simulation(plane_img):
    plane_x = PLANE_INITIAL_X
    plane_y = PLANE_INITIAL_Y
    plane_speed = PLANE_SPEED
    stability = STABILITY_INITIAL
    stability_max = STABILITY_MAX
    gravity = GRAVITY

    # Event display tracking
    current_event = None
    event_image = None
    event_timer = 0

    running = True
    while running:
        screen.fill(SKY_BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Random event ---
        if random.random() < EVENT_PROBABILITY:
            event_name = random.choice(OBSTACLES)
            stability -= DAMAGE[event_name]
            stability = max(0, stability)
            print(f"{event_name}! Stability drops to {stability}")
            plane_y += DAMAGE[event_name] // 2

            # Load and scale event image
            current_event = event_name
            event_image = pygame.image.load(OBSTACLE_IMAGES[event_name])
            event_image = pygame.transform.scale(event_image, (EVENT_IMAGE_WIDTH, EVENT_IMAGE_HEIGHT))
            event_timer = EVENT_DISPLAY_DURATION

        # --- Gravity ---
        plane_y += gravity
        plane_y = max(0, min(plane_y, HEIGHT - PLANE_HEIGHT))

        # --- Move forward ---
        plane_x += plane_speed
        if plane_x > WIDTH - PLANE_WRAP_THRESHOLD:
            plane_x = PLANE_INITIAL_X  # wrap around

        # --- Draw plane ---
        screen.blit(plane_img, (plane_x, plane_y))

        # --- Display event image and text ---
        if event_timer > 0:
            # Draw semi-transparent background for better visibility
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(100)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

            # Draw event image
            screen.blit(event_image, (EVENT_IMAGE_X, EVENT_IMAGE_Y))

            # Draw event text
            event_text = font.render(f"{current_event}!", True, RED)
            screen.blit(event_text, (WIDTH // 2 - event_text.get_width() // 2, EVENT_IMAGE_Y + EVENT_TEXT_Y_OFFSET))

            event_timer -= 1

        # --- Stability bar ---
        pygame.draw.rect(screen, RED, (STABILITY_BAR_X, STABILITY_BAR_Y, STABILITY_BAR_WIDTH, STABILITY_BAR_HEIGHT))
        green_width = STABILITY_BAR_WIDTH * (stability / stability_max)
        pygame.draw.rect(screen, GREEN, (STABILITY_BAR_X, STABILITY_BAR_Y, green_width, STABILITY_BAR_HEIGHT))
        text = small_font.render(f"Stability: {stability}", True, BLACK)
        screen.blit(text, (STABILITY_BAR_X, STABILITY_TEXT_Y))

        # --- Check for crash ---
        if stability <= 0 or plane_y >= HEIGHT - PLANE_HEIGHT:
            crash_text = font.render("PLANE CRASHED! Simulation Over", True, RED)
            screen.blit(crash_text, (WIDTH // 2 - CRASH_MESSAGE_X_OFFSET, HEIGHT // 2))
            pygame.display.update()
            pygame.time.delay(CRASH_MESSAGE_DELAY)
            running = False

        pygame.display.update()
        clock.tick(FPS)


# --- Main program ---
plane_img = choose_plane()
run_simulation(plane_img)

pygame.quit()
sys.exit()