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
GRAY = (180, 180, 180)

# Fonts
font_large = pygame.font.SysFont("arial", 48)
font_medium = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 24)

# Game assets
def create_game_assets():
    # Player ship
    player_img = pygame.image.load('./assets/images/spaceship.png')
    pygame.draw.polygon(player_img, BLUE, [(25, 0), (0, 80), (50, 80)])
    pygame.draw.polygon(player_img, PURPLE, [(25, 10), (10, 70), (40, 70)])

    # Laser
    laser_img = pygame.Surface((4, 20), pygame.SRCALPHA)
    for i in range(20):
        alpha = 255 - (i * 10)
        if alpha < 0: alpha = 0
        pygame.draw.rect(laser_img, (*PURPLE, alpha), (0, i, 4, 1))

    # Asteroids
    asteroid_large = pygame.Surface((120, 120), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_large, BLUE, (60, 60), 50)
    pygame.draw.circle(asteroid_large, PURPLE, (60, 60), 45, 2)

    asteroid_medium = pygame.Surface((70, 70), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_medium, BLUE, (35, 35), 30)
    pygame.draw.circle(asteroid_medium, PURPLE, (35, 35), 25, 2)

    asteroid_small = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(asteroid_small, BLUE, (20, 20), 15)
    pygame.draw.circle(asteroid_small, PURPLE, (20, 20), 12, 2)

    # Power-ups
    powerup_shield = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(powerup_shield, BLUE, (15, 15), 15, 2)
    pygame.draw.circle(powerup_shield, BLUE, (15, 15), 10, 2)

    powerup_rapid = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.rect(powerup_rapid, PURPLE, (10, 5, 10, 20))
    pygame.draw.rect(powerup_rapid, PURPLE, (5, 10, 20, 10))

    powerup_health = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.polygon(powerup_health, WHITE, [(15, 5), (5, 25), (25, 25)])

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
        'powerup_shield': powerup_shield,
        'powerup_rapid': powerup_rapid,
        'powerup_health': powerup_health,
        'star_bg': star_bg
    }

assets = create_game_assets()

# Sound setup
try:
    mixer.music.load('background.wav')
    mixer.music.set_volume(0.5)
    shoot_sound = mixer.Sound('shoot.wav')
    explosion_sound = mixer.Sound('explosion.wav')
    powerup_sound = mixer.Sound('powerup.wav')
    mixer.music.play(-1)
    sounds_available = True
except:
    sounds_available = False

# Game variables
playerX = 370
playerY = 480
playerX_change = 0
player_speed = 8
player_cooldown = 0
player_health = 100
player_shield = 50
player_max_shield = 50
player_shield_regen = 0.1
player_last_hit = 0

lasers = []
laser_speed = 15

asteroids = []
asteroid_spawn_timer = 0
spawn_interval = 60

powerups = []

score = 0
high_score = 0
level = 1
difficulty_timer = 0
game_time = 0

# Menu functions
def draw_text(message, font, color, surface, x, y):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(x, y))
    surface.blit(text, text_rect)

def show_main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Spaceship vs Asteroids", font_large, WHITE, screen, 400, 120)
        draw_text("1 - Start Game", font_medium, GRAY, screen, 400, 250)
        draw_text("2 - Instructions", font_medium, GRAY, screen, 400, 300)
        draw_text("3 - Quit Game", font_medium, GRAY, screen, 400, 350)
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
        draw_text("Avoid getting hit by asteroids", font_small, WHITE, screen, 400, 280)
        draw_text("Collect power-ups for bonuses", font_small, WHITE, screen, 400, 320)
        draw_text("Press ESC to return to main menu", font_small, GRAY, screen, 400, 400)
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
        draw_text("1 - Return to Main Menu", font_medium, GRAY, screen, 400, 400)
        draw_text("2 - Quit Game", font_medium, GRAY, screen, 400, 450)
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
playerImg = pygame.image.load('./assets/images/spaceship.png')
def player(x, y):
    screen.blit(playerImg, (x, y))
    if player_shield > 0:
        shield_surface = pygame.Surface((playerImg.get_width() + 20, 
                                       playerImg.get_height() + 20), pygame.SRCALPHA)
        pygame.draw.polygon(shield_surface, (*BLUE, 50), 
                          [(25, 0), (0, 80), (50, 80)])
        screen.blit(shield_surface, (x - 10, y - 10))

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
        'rotation': 0,
        'rotation_speed': random.uniform(-1, 1),
        'rect': image.get_rect(center=(x, y))
    })

def create_powerup(x, y):
    power_type = random.choice(["shield", "rapid", "health"])
    
    if power_type == "shield":
        image = assets['powerup_shield']
    elif power_type == "rapid":
        image = assets['powerup_rapid']
    else:
        image = assets['powerup_health']
    
    powerups.append({
        'x': x,
        'y': y,
        'image': image,
        'speed': 2,
        'type': power_type,
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
    
    # power-ups
    for powerup in powerups:
        screen.blit(powerup['image'], powerup['rect'])
    
    # player
    player(playerX, playerY)
    
    # Health line
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (20, 20, 200 * (player_health / 100), 20))
    
    # Shield line
    pygame.draw.rect(screen, (100, 100, 255), (20, 50, 200, 15))
    pygame.draw.rect(screen, BLUE, (20, 50, 200 * (player_shield / player_max_shield), 15))
    
    # Score and level
    draw_text(f"Score: {score}", font_small, WHITE, screen, 700, 30)
    draw_text(f"Level: {level}", font_small, WHITE, screen, 700, 70)

def update_game():
    global playerX, playerX_change, player_cooldown, player_shield, player_health, player_last_hit
    global score, high_score, level, difficulty_timer, game_time, asteroid_spawn_timer, spawn_interval
    
    # Update player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and playerX > 0:
        playerX -= player_speed
    if keys[pygame.K_RIGHT] and playerX < 800 - playerImg.get_width():
        playerX += player_speed
    
    if player_cooldown > 0:
        player_cooldown -= 1
    
    # Shield come back
    if pygame.time.get_ticks() - player_last_hit > 3000:
        player_shield = min(player_max_shield, player_shield + player_shield_regen)
    
    # difficulty
    game_time += 1
    difficulty_timer += 1
    
    if difficulty_timer >= 600:  # 10 seconds
        difficulty_timer = 0
        level += 1
        spawn_interval = max(15, spawn_interval - 5)
    
    # Spawn asteroids
    asteroid_spawn_timer += 1
    if asteroid_spawn_timer >= spawn_interval:
        asteroid_spawn_timer = 0
        create_asteroid()
        if random.random() < 0.3 * level:
            create_asteroid()
    
    # Update lasers
    for laser in lasers[:]:
        laser['rect'].y -= laser_speed
        if laser['rect'].bottom < 0:
            lasers.remove(laser)
    
    # Update asteroids
    player_rect = playerImg.get_rect(topleft=(playerX, playerY))
    for asteroid in asteroids[:]:
        asteroid['y'] += asteroid['speed']
        asteroid['rotation'] += asteroid['rotation_speed']
        asteroid['rect'].center = (asteroid['x'], asteroid['y'])
        
        if asteroid['rect'].top > 600:
            asteroids.remove(asteroid)
        elif (pygame.time.get_ticks() - player_last_hit > 1000 and 
              check_collision(asteroid['rect'], player_rect)):
            if player_shield > 0:
                player_shield -= 20
                if player_shield < 0:
                    player_health += player_shield
                    player_shield = 0
            else:
                player_health -= 20
            
            player_last_hit = pygame.time.get_ticks()
            asteroids.remove(asteroid)
            
            if player_health <= 0:
                return "game_over"
    
    # Collisions
    for laser in lasers[:]:
        for asteroid in asteroids[:]:
            if check_collision(laser['rect'], asteroid['rect']):
                asteroid['health'] -= 1
                if asteroid['health'] <= 0:
                    if sounds_available:
                        explosion_sound.play()
                    score += 10 * (4 - (asteroid['image'].get_width() // 20))
                    asteroids.remove(asteroid)
                    
                    # Chance to spawn power-up
                    if random.random() < 0.2:
                        create_powerup(asteroid['x'], asteroid['y'])
                lasers.remove(laser)
                break
    
    # Update power-ups
    for powerup in powerups[:]:
        powerup['y'] += powerup['speed']
        powerup['rect'].center = (powerup['x'], powerup['y'])
        
        if powerup['rect'].top > 600:
            powerups.remove(powerup)
        elif check_collision(powerup['rect'], player_rect):
            if powerup['type'] == "shield":
                player_shield = min(player_max_shield, player_shield + 30)
            elif powerup['type'] == "rapid":
                player_cooldown = max(0, player_cooldown - 5)
            else:  # health
                player_health = min(100, player_health + 20)
            
            powerups.remove(powerup)
            if sounds_available:
                powerup_sound.play()
    
    return "playing"

def reset_game():
    global playerX, playerY, player_health, player_shield, player_last_hit, player_cooldown
    global lasers, asteroids, powerups
    global score, level, difficulty_timer, game_time, asteroid_spawn_timer, spawn_interval
    
    playerX = 370
    playerY = 480
    player_health = 100
    player_shield = 50
    player_last_hit = 0
    player_cooldown = 0
    
    lasers = []
    asteroids = []
    powerups = []
    
    score = 0
    level = 1
    difficulty_timer = 0
    game_time = 0
    asteroid_spawn_timer = 0
    spawn_interval = 60

    # Score
    try:
        with open('highscore.txt', 'r') as f:
            high_score = int(f.read())
    except (FileNotFoundError, ValueError):
        high_score = 0

# Game loop
def main():
    global high_score
    global player_cooldown
    
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
                            fire_laser(playerX + playerImg.get_width() // 2, playerY)
                
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