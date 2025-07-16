import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Spaceship vs Asteroids")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
PURPLE = (150, 0, 255)

# Fonts
font_large = pygame.font.SysFont("arial", 48)
font_medium = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 24)

# Game Stuff
def create_game_assets():
    #  ship
    player_img = pygame.image.load('./assets/images/spaceship.png')

    # Laser
    laser_img = pygame.Surface((4, 20), pygame.SRCALPHA)
    for i in range(20):
        alpha = 255 - (i * 10)
        if alpha < 0: alpha = 0
        pygame.draw.rect(laser_img, (*PURPLE, alpha), (0, i, 4, 1))

    # Asteroids - different sizes worth different points
    asteroid_large = pygame.Surface((120, 120), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_large, BLUE, (60, 60), 50)
    pygame.draw.circle(asteroid_large, PURPLE, (60, 60), 45, 2)

    asteroid_medium = pygame.Surface((70, 70), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_medium, BLUE, (35, 35), 30)
    pygame.draw.circle(asteroid_medium, PURPLE, (35, 35), 25, 2)

    asteroid_small = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_small, BLUE, (20, 20), 15)
    pygame.draw.circle(asteroid_small, PURPLE, (20, 20), 12, 2)

    # Background
    star_bg = pygame.Surface((800, 600), pygame.SRCALPHA)
    for _ in range(200):
        x = random.randint(0, 800)
        y = random.randint(0, 600)
        size = random.randint(1, 3)
        pygame.draw.circle(star_bg, WHITE, (x, y), size)

    return {
        'player_img': player_img,
        'laser_img': laser_img,
        'asteroid_large': asteroid_large,
        'asteroid_medium': asteroid_medium,
        'asteroid_small': asteroid_small,
        'star_bg': star_bg
    }

assets = create_game_assets()

# Sound setup
try:
    mixer.music.load('./assets/music/background.wav')
    mixer.music.set_volume(0.5)
    shoot_sound = mixer.Sound('./assets/music/shoot.wav')
    explosion_sound = mixer.Sound('./assets/music/explosion.wav')
    mixer.music.play(-1)
    sounds_available = True
except:
    sounds_available = False

# Game variables
playerX = 370
playerY = 480
player_speed = 8
player_cooldown = 0
player_health = 100

lasers = []
laser_speed = 15

asteroids = []
asteroid_spawn_timer = 0
spawn_interval = 60

score = 0
high_score = 0

# Asteroid point values
ASTEROID_POINTS = {
    'large': 30,
    'medium': 20,
    'small': 10
}

# Menu functions
def draw_text(message, font, color, surface, x, y):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)

def show_main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Spaceship vs Asteroids", font_large, WHITE, screen, 400, 120)
        draw_text("1 - Start Game", font_medium, WHITE, screen, 400, 250)
        draw_text("2 - Instructions", font_medium, WHITE, screen, 400, 300)
        draw_text("3 - Quit Game", font_medium, WHITE, screen, 400, 350)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    show_instructions()
                elif event.key == pygame.K_3:
                    pygame.quit()
                    return "quit"

def show_instructions():
    while True:
        screen.fill(BLACK)
        draw_text("How to Play", font_large, WHITE, screen, 400, 100)
        draw_text("Use arrow keys to move your spaceship", font_small, WHITE, screen, 400, 200)
        draw_text("Press SPACE to shoot asteroids", font_small, WHITE, screen, 400, 240)
        draw_text("Large asteroids: 30 pts", font_small, BLUE, screen, 400, 280)
        draw_text("Medium asteroids: 20 pts", font_small, BLUE, screen, 400, 320)
        draw_text("Small asteroids: 10 pts", font_small, BLUE, screen, 400, 360)
        draw_text("Press ESC to return to main menu", font_small, WHITE, screen, 400, 440)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

def show_game_over():
    while True:
        screen.fill(BLACK)
        draw_text("Game Over", font_large, WHITE, screen, 400, 200)
        draw_text(f"Score: {score}", font_medium, WHITE, screen, 400, 280)
        draw_text(f"High Score: {high_score}", font_medium, BLUE, screen, 400, 320)
        draw_text("1 - Return to Main Menu", font_medium, WHITE, screen, 400, 400)
        draw_text("2 - Quit Game", font_medium, WHITE, screen, 400, 450)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "menu"
                elif event.key == pygame.K_2:
                    pygame.quit()
                    return "quit"

# Game functions
def player(x, y):
    screen.blit(assets['player_img'], (x, y))

def fire_laser(x, y):
    lasers.append({
        'x': x,
        'y': y,
        'rect': assets['laser_img'].get_rect(midbottom=(x, y))
    })

def create_asteroid():
    size = random.choice(["large", "medium", "small"])
    
    if size == "large":
        image = assets['asteroid_large']
        speed = random.uniform(1.5, 2.5)
        health = 3
    elif size == "medium":
        image = assets['asteroid_medium']
        speed = random.uniform(2.5, 3.5)
        health = 2
    else:
        image = assets['asteroid_small']
        speed = random.uniform(3.5, 5)
        health = 1

    x = random.randint(image.get_width() // 2, 800 - image.get_width() // 2)
    y = -image.get_height() // 2
    
    asteroids.append({
        'x': x,
        'y': y,
        'image': image,
        'speed': speed,
        'health': health,
        'size': size,  # Track asteroid size for scoring
        'rotation': 0,
        'rotation_speed': random.uniform(-1, 1),
        'rect': image.get_rect(center=(x, y))
    })

def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

def draw_game():
    screen.fill(BLACK)
    screen.blit(assets['star_bg'], (0, 0))
    
    # lasers
    for laser in lasers:
        screen.blit(assets['laser_img'], laser['rect'])
    
    # asteroids
    for asteroid in asteroids:
        rotated = pygame.transform.rotate(asteroid['image'], asteroid['rotation'])
        screen.blit(rotated, rotated.get_rect(center=(asteroid['x'], asteroid['y'])))
    
    # player
    player(playerX, playerY)
    
    # Health bar
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (20, 20, 200 * (player_health / 100), 20))
    
    # Score display
    draw_text(f"Score: {score}", font_small, WHITE, screen, 700, 30)

def update_game():
    global playerX, playerY, player_cooldown, player_health
    global score, high_score, asteroid_spawn_timer, spawn_interval
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > 0:
        playerX -= player_speed
    if keys[pygame.K_RIGHT] and playerX < 800 - assets['player_img'].get_width():
        playerX += player_speed
    
    if player_cooldown > 0:
        player_cooldown -= 1
    
    # Spawn asteroids
    asteroid_spawn_timer += 1
    if asteroid_spawn_timer >= spawn_interval:
        asteroid_spawn_timer = 0
        create_asteroid()
        if random.random() < 0.3:  # 30% chance for an extra asteroid
            create_asteroid()
    
    # Update lasers
    for laser in lasers[:]:
        laser['rect'].y -= laser_speed
        if laser['rect'].bottom < 0:
            lasers.remove(laser)
    
    # Update asteroids and check collisions
    player_rect = assets['player_img'].get_rect(topleft=(playerX, playerY))
    for asteroid in asteroids[:]:
        asteroid['y'] += asteroid['speed']
        asteroid['rotation'] += asteroid['rotation_speed']
        asteroid['rect'].center = (asteroid['x'], asteroid['y'])
        
        if asteroid['rect'].top > 600:
            asteroids.remove(asteroid)
        elif check_collision(asteroid['rect'], player_rect):
            player_health -= 20
            asteroids.remove(asteroid)
            
            if player_health <= 0:
                return "game_over"
    
    # Check laser-asteroid collisions
    for laser in lasers[:]:
        for asteroid in asteroids[:]:
            if check_collision(laser['rect'], asteroid['rect']):
                asteroid['health'] -= 1
                if asteroid['health'] <= 0:
                    if sounds_available:
                        explosion_sound.play()
                    # Award points based on asteroid size
                    score += ASTEROID_POINTS[asteroid['size']]
                    asteroids.remove(asteroid)
                lasers.remove(laser)
                break
    
    return "playing"

def reset_game():
    global playerX, playerY, player_health, player_cooldown
    global lasers, asteroids
    global score, asteroid_spawn_timer, spawn_interval
    
    playerX = 370
    playerY = 480
    player_health = 100
    player_cooldown = 0
    
    lasers = []
    asteroids = []
    
    score = 0
    asteroid_spawn_timer = 0
    spawn_interval = 60

    # Load high score
    try:
        with open('highscore.txt', 'r') as f:
            high_score = int(f.read())
    except (FileNotFoundError, ValueError):
        high_score = 0

# Game loop
def main():
    global high_score, player_cooldown
    
    running = True
    while running:
        # Show main menu
        menu_choice = show_main_menu()
        
        if menu_choice == "start":
            reset_game()
            game_active = True
            
            while game_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        game_active = False
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_active = False
                        elif event.key == pygame.K_SPACE and player_cooldown == 0:
                            player_cooldown = 15
                            if sounds_available:
                                shoot_sound.play()
                            fire_laser(playerX + assets['player_img'].get_width() // 2, playerY)
                
                if not running:
                    break
                
                game_state = update_game()
                draw_game()
                
                if game_state == "game_over":
                    high_score = max(high_score, score)
                    with open('highscore.txt', 'w') as f:
                        f.write(str(high_score))
                    
                    game_over_choice = show_game_over()
                    if game_over_choice == "menu":
                        break
                    elif game_over_choice == "quit":
                        running = False
                        break
                
                pygame.display.update()
                clock.tick(60)
        
        elif menu_choice == "quit":
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()