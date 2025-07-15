import pygame
import sys

def InitializeMenu():
    global ColorWhite, ColorBlack, ColorGray
    global FontLarge, FontMedium, FontSmall

    ColorWhite = (255, 255, 255)
    ColorBlack = (0, 0, 0)
    ColorGray = (180, 180, 180)

    FontLarge = pygame.font.SysFont("arial", 48)
    FontMedium = pygame.font.SysFont("arial", 32)
    FontSmall = pygame.font.SysFont("arial", 24)

def DrawText(Message, FontUsed, TextColor, Surface, XCenter, YCenter):
    TextImage = FontUsed.render(Message, True, TextColor)
    TextRectangle = TextImage.get_rect(center=(XCenter, YCenter))
    Surface.blit(TextImage, TextRectangle)

def ShowMainMenu(GameScreen):
    while True:
        GameScreen.fill(ColorBlack)
        DrawText("Spaceship vs Asteroids", FontLarge, ColorWhite, GameScreen, 400, 120)
        DrawText("1 - Start Game", FontMedium, ColorGray, GameScreen, 400, 250)
        DrawText("2 - Instructions", FontMedium, ColorGray, GameScreen, 400, 300)
        DrawText("3 - Quit Game", FontMedium, ColorGray, GameScreen, 400, 350)
        pygame.display.update()

        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_1:
                    return "start"
                elif Event.key == pygame.K_2:
                    ShowInstructions(GameScreen)
                elif Event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def ShowInstructions(GameScreen):
    while True:
        GameScreen.fill(ColorBlack)
        DrawText("How to Play", FontLarge, ColorWhite, GameScreen, 400, 100)
        DrawText("Use the arrow keys to move your spaceship.", FontSmall, ColorWhite, GameScreen, 400, 200)
        DrawText("Press the spacebar to shoot asteroids.", FontSmall, ColorWhite, GameScreen, 400, 240)
        DrawText("Avoid getting hit!", FontSmall, ColorWhite, GameScreen, 400, 280)
        DrawText("Press ESC to return to the main menu.", FontSmall, ColorGray, GameScreen, 400, 400)
        pygame.display.update()

        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_ESCAPE:
                    return

def ShowGameOver(GameScreen):
    while True:
        GameScreen.fill(ColorBlack)
        DrawText("Game Over", FontLarge, ColorWhite, GameScreen, 400, 200)
        DrawText("1 - Return to Main Menu", FontMedium, ColorGray, GameScreen, 400, 300)
        DrawText("2 - Quit Game", FontMedium, ColorGray, GameScreen, 400, 350)
        pygame.display.update()

        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_1:
                    return "restart"
                elif Event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()
