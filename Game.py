# Created by Sujal Jain

import pygame              # Importing pygame module
from sys import exit       # Importing exit() from sys module
import random
pygame.init()              # Initialising pygame

# Creating Display surface, which must be unique
WIDTH,HEIGHT=800,400
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Title of our game
pygame.display.set_caption('Mario')  

# Clock object
clock = pygame.time.Clock() 

# Importing images and creating background
sky_surface = pygame.image.load('Sky.png').convert()
ground_surface = pygame.image.load('Ground.png').convert()

# Creating enemy
# Turtle
turtle_1= pygame.image.load('turtle1.png').convert_alpha()
turtle_2= pygame.image.load('turtle2.png').convert_alpha()
turtle_frame = [turtle_1,turtle_2]
turtle_frame_index = 0
turtle_surface = turtle_frame[turtle_frame_index]

# Fly
fly_1 = pygame.image.load('Fly1.png').convert_alpha()
fly_2 = pygame.image.load('Fly2.png').convert_alpha()
fly_frame = [fly_1,fly_2]
fly_frame_index = 0
fly_surface = fly_frame[fly_frame_index]

obstacle_rect_list = []

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 317:
               screen.blit(turtle_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collision(player,obstacles):
    if obstacles:
        for turtle_rect in obstacles:
            if player.colliderect(turtle_rect):return False
    return True
 
def player_animation():
    # Running animation if player is on floor
    global player_surface, player_index
    
    if player_rect.bottom < 300:
        player_surface = player_jump
        
    else:
        player_index += 0.2
        if player_index >len(player_run):player_index = 0
        player_surface = player_run[int(player_index)]


# Creating the player

# At the time of playing
player_run_1 = pygame.image.load('run1.png').convert_alpha()
player_run_2 = pygame.image.load('run2.png').convert_alpha()
player_run_3 = pygame.image.load('run3.png').convert_alpha()
player_run = [player_run_1,player_run_2,player_run_3]
player_index = 0
player_surface = player_run[player_index]
player_rect = player_surface.get_rect(midbottom = (80,310))
player_jump = pygame.image.load('jump.png').convert_alpha()



# Exit Surface
player_exit_surface = pygame.image.load('player.png').convert_alpha()
player_exit_scale = pygame.transform.rotozoom(player_exit_surface,0,2)
player_exit_rect = player_exit_scale.get_rect(midbottom = (400,250))

# Creating the exit screen
name = pygame.font.Font('Pixeltype.ttf',50)
game_name = name.render('Mario',False,'White')
game_name_rect = game_name.get_rect(center = (400,130))
game_message = pygame.font.Font('Pixeltype.ttf',50)
game_message_surface = game_message.render('Press "s" to run again',False,'White')
game_message_rect = game_message_surface.get_rect(midbottom = (400,300))

# Create a Custom color
# Using the rgb or hexadecimal method

# Gravity
player_gravity = 0

# State management
game_active = True

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2000)

turtle_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(turtle_animation_timer,200)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    # draw all our elements 
    # update everything
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit()
        
        if game_active:
            if (event.type == obstacle_timer):
                if random.randint(0,2):
                    obstacle_rect_list.append(turtle_surface.get_rect(bottomright = (random.randint(900,1100),317)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (random.randint(900,1100),217)))
            
            if event.type == turtle_animation_timer:
                if turtle_frame_index == 0: turtle_frame_index = 1
                else: turtle_frame_index = 0
                turtle_surface = turtle_frame[turtle_frame_index]
                
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface = fly_frame[fly_frame_index]
            
    if game_active:
            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >=300:
                    player_gravity = -20
            
            screen.blit(sky_surface,(0,0)) 
            screen.blit(ground_surface,(0,300))  
            
            
            # Keyboard input, player and gravity
            keys = (pygame.key.get_pressed())         
            # Creating a dictionary
            if keys[pygame.K_SPACE] and player_rect.bottom >=300:
                player_gravity = -20
            
            
            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >=300:
                player_rect.bottom = 300
            
            player_animation()
            screen.blit(player_surface,player_rect)
            
            
            obstacle_rect_list = obstacle_movement(obstacle_rect_list)
            
            # Collision 
            game_active = collision(player_rect,obstacle_rect_list)
    
    else:
        screen.fill('Black')
        screen.blit(player_exit_scale,player_exit_rect)
        screen.blit(game_name,game_name_rect)
        screen.blit(game_message_surface,game_message_rect)
        keys = (pygame.key.get_pressed()) 
        if keys[pygame.K_s]:
            game_active = True
            obstacle_rect_list.clear()      
            
    pygame.display.update()
            
    # Setting the Frame rate
    # Basically telling the while loop to run at 60 frames per second
    clock.tick(60)                    