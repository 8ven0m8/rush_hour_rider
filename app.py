import pygame
from sys import exit
import random


# Constants
WIDTH = 400
HEIGHT = 600
lane_coordinates = [50, 165, 280]

# Variables
score = 0
relative_speed = 0
high_score = 0

# Initialize Pygame
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Rush Hour Rider')

########### Sprite Groups ############

# Player Car
class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('learning pygame/rush_hour_rider/images/car_small.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 125))
        self.rect = self.image.get_rect(midbottom = (WIDTH / 2, HEIGHT - 100))
    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.right < WIDTH - 30:
            self.rect.x += 7
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.left > 30:
            self.rect.x -= 7

# Traffic Car
class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('learning pygame/rush_hour_rider/images/obstacle_small.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (65, 125))
        self.rect = self.image.get_rect(midbottom = (x, y))
    def update(self):
        global relative_speed, score
        self.rect.top += 5 + relative_speed
        if self.rect.top > HEIGHT:
            score += 1
            relative_speed += 0.1
            self.rect.bottom = 0
            self.rect.x = lane_coordinates[random.randint(0, len(lane_coordinates) - 1)]


########### Sprites ############
player = pygame.sprite.GroupSingle()
player_car = PlayerCar()
player.add(player_car)

traffic = pygame.sprite.Group()
traffic_car1 = TrafficCar(85, 0)
traffic_car2 = TrafficCar(315, HEIGHT - 200)
traffic.add(traffic_car1, traffic_car2)



# Boolean to control game state
game_state = 'main-menu'

# Background Road Image
background = pygame.image.load('learning pygame/rush_hour_rider/images/background.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = -HEIGHT


# Font for Texts
font = pygame.font.Font("learning pygame/rush_hour_rider/font/score.ttf", 36)

# End screen
end_screen = pygame.Surface((300, 150)).convert_alpha()
end_screen_rect = end_screen.get_rect(center=(WIDTH / 2, HEIGHT / 2))

# Buttons

# Return
return_btn = pygame.Surface((100, 30)).convert_alpha()
return_btn_rect = return_btn.get_rect(center=(120, 348))

# Restart
restart_btn = pygame.Surface((100, 30)).convert_alpha()
restart_btn_rect = restart_btn.get_rect(center=(278, 348))


while True:

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_state == 'game_over':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_state = 'playing'
                    # Reset game state
                    player_car.rect.midbottom = (WIDTH / 2, HEIGHT - 100)
                    traffic.empty()
                    traffic.add(TrafficCar(85, 0), TrafficCar(315, HEIGHT - 200))
                    score = 0
                    relative_speed = 0
                    bg_y1 = 0
                    bg_y2 = -HEIGHT
                elif event.key == pygame.K_ESCAPE:
                    game_state = 'main-menu'
                    # Reset background position
                    bg_y1 = 0
                    bg_y2 = -HEIGHT

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn_rect.collidepoint(event.pos):
                    game_state = 'playing'
                    player_car.rect.midbottom = (WIDTH / 2, HEIGHT - 100)
                    traffic.empty()
                    traffic.add(TrafficCar(85, 0), TrafficCar(315, HEIGHT - 200))
                    score = 0
                    relative_speed = 0
                    bg_y1 = 0
                    bg_y2 = -HEIGHT
                elif return_btn_rect.collidepoint(event.pos):
                    game_state = 'main-menu'
                    bg_y1 = 0
                    bg_y2 = -HEIGHT

        elif game_state == 'main-menu' and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_state = 'playing'
                player_car.rect.midbottom = (WIDTH / 2, HEIGHT - 100)
                traffic.empty()
                traffic.add(TrafficCar(85, 0), TrafficCar(315, HEIGHT - 200))
                score = 0
                relative_speed = 0
                bg_y1 = 0
                bg_y2 = -HEIGHT




    # Playing the game state
    if game_state == 'playing':



        # Background Scrolling Mechanics
        bg_scroll_speed = 10 + relative_speed
        bg_y1 += bg_scroll_speed
        bg_y2 += bg_scroll_speed
        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT
        display.blit(background, (0, bg_y1))
        display.blit(background, (0, bg_y2))

        # Player Car
        player.draw(display)
        player.update()

        # Traffic Cars
        traffic.draw(display)
        traffic.update()

        # Score Display
        score_display = font.render(f'Score: {score}', True, 'white')
        score_display_rect = score_display.get_rect(topleft = (10, 10))
        display.blit(score_display, score_display_rect)

        # Check for collisions
        if pygame.sprite.spritecollide(player_car, traffic, False):
            game_state = 'game_over'

    elif game_state == 'game_over':
        if score > high_score:
            high_score = score
        pygame.draw.rect(display, "#CDB18F", end_screen_rect, 0, 20)
        pygame.draw.rect(display, "#755A5A", end_screen_rect, 5, 20)
        pygame.draw.rect(display, "#CE7A14", return_btn_rect, 0, 20)
        pygame.draw.rect(display, "#CE7A14", restart_btn_rect, 0, 20)
        end_text = font.render('Game Over', True, 'white')
        end_text_rect = end_text.get_rect(center=(200, 250))
        display.blit(end_text, end_text_rect)
        end_score_text = font.render(f'Your Score: {score}', True, 'white')
        end_score_text_rect = end_score_text.get_rect(center=(200, 285))
        display.blit(end_score_text, end_score_text_rect)
        end_high_score_text = font.render(f'High Score: {high_score}', True, 'white')
        end_high_score_text_rect = end_high_score_text.get_rect(center=(200, 310))
        display.blit(end_high_score_text, end_high_score_text_rect)


        restart_text = font.render('Return', True, 'white')
        restart_text_rect = restart_text.get_rect(center=(120, 350))


        restart_text2 = font.render('Restart', True, 'white')
        restart_text2_rect = restart_text2.get_rect(center=(280, 350))

        display.blit(restart_text, restart_text_rect)
        display.blit(restart_text2, restart_text2_rect)

    elif game_state == 'main-menu':
        display.fill("#2D2121")
        menu_text = font.render('Rush Hour Rider', True, 'white')
        menu_text_rect = menu_text.get_rect(center=(WIDTH / 2, HEIGHT - 500))
        display.blit(menu_text, menu_text_rect)
        user_car = pygame.image.load('learning pygame/rush_hour_rider/images/car_small.png').convert_alpha()
        user_car = pygame.transform.scale(user_car, (125, 255))
        user_car_rect = user_car.get_rect(center=(WIDTH / 2, HEIGHT - 300))
        display.blit(user_car, user_car_rect)
        if high_score == 0:
            start_text = font.render('Press Enter to Start', True, 'white')
        else:
            start_text = font.render(f'Highscore: {high_score}', True, 'white')
        start_text_rect = start_text.get_rect(center=(WIDTH / 2, HEIGHT - 100))
        display.blit(start_text, start_text_rect)




        
    pygame.display.update()
    clock.tick(60)
