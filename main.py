import pygame
import sys
import random
import time

# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("✈️ Plane Flight Simulation")

# --- Load Assets ---
jet = pygame.image.load("jet.png").convert_alpha()
plane = pygame.image.load("plane.png").convert_alpha()

# Scale planes
jet = pygame.transform.scale(jet, (200, 100))
plane = pygame.transform.scale(plane, (200, 100))

# Obstacles
obstacle_bird = pygame.image.load("bird.png").convert_alpha()
obstacle_mountain = pygame.image.load("mountain.png").convert_alpha()
obstacle_storm = pygame.image.load("storm.png").convert_alpha()

obstacle_bird = pygame.transform.scale(obstacle_bird, (100, 100))
obstacle_mountain = pygame.transform.scale(obstacle_mountain, (200, 200))
obstacle_storm = pygame.transform.scale(obstacle_storm, (150, 150))

obstacles = {
    "bird": obstacle_bird,
    "mountain": obstacle_mountain,
    "storm": obstacle_storm
}

# --- Colors & Fonts ---
SKY = (135, 206, 250)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (80, 200, 120)
BROWN = (120, 80, 40)
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()


# --- Helper Functions ---
def choose_plane():
    """Menu to pick plane (waits for key input)."""
    selecting = True
    while selecting:
        screen.fill(SKY)
        title = font.render("Choose your aircraft:", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 180, 100))

        # Draw planes
        screen.blit(jet, (WIDTH // 4 - 100, 250))
        screen.blit(plane, (3 * WIDTH // 4 - 100, 250))

        # Labels
        screen.blit(font.render("Press 1 for Jet (Strong)", True, WHITE), (WIDTH // 4 - 120, 370))
        screen.blit(font.render("Press 2 for Plane (Weaker)", True, WHITE), (3 * WIDTH // 4 - 130, 370))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "jet", jet
                elif event.key == pygame.K_2:
                    return "plane", plane

        pygame.display.flip()
        clock.tick(30)


def reset_game(plane_type):
    """Reset plane and state after crash or restart."""
    if plane_type == "jet":
        speed = 7
        stability = 1  # less shaking
        crash_limit = HEIGHT - 90
    else:  # weaker plane
        speed = 4
        stability = 2  # more shaking
        crash_limit = HEIGHT - 130

    return {
        "plane_x": 50,
        "plane_y": HEIGHT // 2,
        "speed": speed,
        "stability": stability,
        "crash_limit": crash_limit,
        "flying": True,
        "crashing": False,
        "obstacle_chosen": None,
        "obstacle_x": WIDTH + 200,
        "start_time": time.time(),
        "landing": False,
    }


# --- Setup ---
plane_type, current_plane = choose_plane()
game = reset_game(plane_type)

# --- Main Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Choose obstacle (for testing)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game["obstacle_chosen"] = "bird"
                game["crashing"] = True
            elif event.key == pygame.K_2:
                game["obstacle_chosen"] = "mountain"
                game["crashing"] = True
            elif event.key == pygame.K_3:
                game["obstacle_chosen"] = "storm"
                game["crashing"] = True
            elif event.key == pygame.K_r and not game["flying"]:
                game = reset_game(plane_type)

    screen.fill(SKY)

    # --- Draw ground ---
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - 40, WIDTH, 40))

    # --- Timer & Landing Logic ---
    elapsed = time.time() - game["start_time"]
    remaining_time = max(0, 60 - int(elapsed))  # 1-minute flight

    # Start landing after 60 seconds
    if elapsed >= 60 and not game["landing"] and game["flying"]:
        game["landing"] = True

    # Plane movement
    if game["flying"]:
        game["plane_x"] += game["speed"]

        # ✅ Keep plane on screen (loop around)
        if game["plane_x"] > WIDTH:
            game["plane_x"] = -200

        # Normal flight shaking (depends on strength)
        if not game["landing"] and not game["crashing"]:
            game["plane_y"] += random.choice([-game["stability"], 0, game["stability"]])

        # If obstacle chosen, simulate crash
        if game["crashing"]:
            game["plane_y"] += random.choice([-4, 4])
            game["plane_x"] += 2

        # Landing motion
        if game["landing"]:
            if game["plane_y"] < HEIGHT - 120:
                game["plane_y"] += 1.5  # descend slowly
            else:
                game["flying"] = False  # finished landing
                game["landing"] = False

        # Crash if hit ground (depends on strength)
        if not game["landing"] and game["plane_y"] > game["crash_limit"]:
            game["flying"] = False

    # --- Obstacle Movement ---
    if game["obstacle_chosen"] and game["flying"] and not game["landing"]:
        obs = obstacles[game["obstacle_chosen"]]
        game["obstacle_x"] -= 6
        obs_y = HEIGHT // 2 if game["obstacle_chosen"] != "mountain" else HEIGHT - 240
        screen.blit(obs, (game["obstacle_x"], obs_y))
        if game["obstacle_x"] < -200:
            game["obstacle_chosen"] = None
            game["obstacle_x"] = WIDTH + random.randint(200, 600)

    # --- Draw Plane ---
    screen.blit(current_plane, (game["plane_x"], game["plane_y"]))

    # --- Draw Timer ---
    timer_text = font.render(f"Time Left: {remaining_time}s", True, WHITE)
    screen.blit(timer_text, (20, 20))

    # --- Landing / Crash Messages ---
    if not game["flying"]:
        if elapsed >= 60:
            msg = "✅ Successful Landing your family still died because of murder."
            color = GREEN
        else:
            msg = " plane Crashed you have lost your family in the crash X_X"
            color = RED
        text = font.render(msg, True, color)
        screen.blit(text, (WIDTH // 2 - 300, HEIGHT // 2))

    pygame.display.update()
    clock.tick(60)
