import pygame
import random
from sys import exit

WIDTH = 400
HEIGHT = 600

pygame.init()
pygame.display.set_caption('Rush Hour Rider')

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game_active = True

# Background Road Image
background = pygame.image.load('learning pygame/rush_hour_rider/images/background.png').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
bg_y1 = 0
bg_y2 = HEIGHT

# Player Car
user_car = pygame.image.load('learning pygame/rush_hour_rider/images/car.png').convert_alpha()
user_car = pygame.transform.scale(user_car, (75, 125))
user_car_rect = user_car.get_rect(midbottom = (WIDTH/2, HEIGHT - 100))

# Text display
score = 0
high_score = 0
font = pygame.font.Font("learning pygame/rush_hour_rider/font/score.ttf", 36)
text_surface = font.render('Score: 0', True, 'white')
text_surface_rect = text_surface.get_rect(midbottom = (70, 50))

# Traffic cars
traffic_car = pygame.image.load('learning pygame/rush_hour_rider/images/obstacle.png').convert_alpha()
traffic_car = pygame.transform.scale(traffic_car, (75, 125))
traffic_car_rect = traffic_car.get_rect(midbottom = (85, 0))

traffic_car2 = pygame.image.load('learning pygame/rush_hour_rider/images/obstacle.png').convert_alpha()
traffic_car2 = pygame.transform.scale(traffic_car2, (75, 125))
traffic_car_rect2 = traffic_car2.get_rect(midbottom = (315, HEIGHT - 200))
relative_speed = 0

# End Screen
end_screen = pygame.Surface((300, 150)).convert_alpha()
end_screen_rect = end_screen.get_rect(center = (WIDTH / 2, HEIGHT / 2))

bg_y1 = 0
bg_y2 = -HEIGHT

while True:
    bg_scroll_speed = 10 + relative_speed  # Background scroll speed increases with relative speed
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    user_car_rect.midbottom = (WIDTH / 2, HEIGHT - 100)
                    traffic_car_rect.midbottom = (85, 0)
                    traffic_car_rect2.midbottom = (315, HEIGHT - 200)
                    score = 0
                    relative_speed = 0
                    bg_y1 = 0
                    bg_y2 = HEIGHT
    
    if game_active:
        key_pressed = pygame.key.get_pressed()
        if (key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]) and user_car_rect.right < 370:
            user_car_rect.x += 7   # Car Movement speed
        if (key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]) and user_car_rect.left > 30:
            user_car_rect.x -= 7   # Car Movement speed

        bg_y1 += bg_scroll_speed
        bg_y2 += bg_scroll_speed
        if bg_y1 >= HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 >= HEIGHT:
            bg_y2 = -HEIGHT

        display.blit(background, (0, bg_y1))
        display.blit(background, (0, bg_y2))

        # User car movement
        display.blit(user_car, user_car_rect)

        # Traffic car movement
        traffic_car_rect.top += 5 + relative_speed  # Traffic car speed
        display.blit(traffic_car, traffic_car_rect)
        if traffic_car_rect.top > 600:
            score += 1
            traffic_car_rect.bottom = 0
            traffic_car_lane_coords = [50, 165, 280, 50, 165, 280, 50, 165, 280]
            random_index = traffic_car_lane_coords[random.randint(0, 8)]
            traffic_car_rect.x = random_index
        
        # Traffic car 2 movement
        traffic_car_rect2.top += 5 + relative_speed
        display.blit(traffic_car2, traffic_car_rect2)
        if traffic_car_rect2.top > 600:
            score += 1
            traffic_car_rect2.bottom = 0
            traffic_car_lane_coords = [50, 165, 280, 50, 165, 280, 50, 165, 280]
            random_index = traffic_car_lane_coords[random.randint(0, 8)]
            traffic_car_rect2.x = random_index
        # relative speed
        relative_speed += 0.001  # Increase relative speed overtime
        
        # Text display
        display.blit(text_surface, text_surface_rect)
        text_surface = font.render(f'Score: {score}', True, 'white')
        text_surface_rect = text_surface.get_rect(midbottom = (70, 50))

        if user_car_rect.colliderect(traffic_car_rect) or user_car_rect.colliderect(traffic_car_rect2):
            game_active = False
    else:
        if score > high_score:
            high_score = score
        pygame.draw.rect(display, "#CDB18F", end_screen_rect, 0, 20)
        pygame.draw.rect(display, "#755A5A", end_screen_rect, 5, 20)
        end_text = font.render('Game Over', True, 'white')
        end_text_rect = end_text.get_rect(center = (200, 250))
        display.blit(end_text, end_text_rect)
        end_score_text = font.render(f'Your Score: {score}', True, 'white')
        end_score_text_rect = end_score_text.get_rect(center = (175, 285))
        display.blit(end_score_text, end_score_text_rect)
        end_high_score_text = font.render(f'Your High Score: {high_score}', True, 'white')
        end_high_score_text_rect = end_score_text.get_rect(center = (175, 310))
        display.blit(end_high_score_text, end_high_score_text_rect)
        restart_text = font.render('Press Enter to Restart', True, 'white')
        restart_text_rect = restart_text.get_rect(center = (200, 350))
        display.blit(restart_text, restart_text_rect)
        
            
    pygame.display.update()
    clock.tick(60)