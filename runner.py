import pygame
import sys
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Art/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Art/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Art/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.grav = 0

        self.jump_sound = pygame.mixer.Sound('Audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.1)

# Key imput

    def player_imput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.grav = -20
            self.jump_sound.play()

# Gravity
    def apply_grav(self):
        self.grav += 1
        self.rect.y += self.grav
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

# Animation and jump mechanic
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

# Player imputs, gravity and animation update
    def update(self):
        self.player_imput()
        self.apply_grav()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

    # Enemies imports
        if type == 'fly':
            fly_1 = pygame.image.load('Art/Enemies/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Art/Enemies/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('Art/Enemies/Snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Art/Enemies/Snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

    # Where to spawn and animation index
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

# Defines animation, going through images 1 and 2
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        else:
            self.image = self.frames[int(self.animation_index)]

# Updates the animation and frames, giving movement
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

# Destroys sprites that are not anymore on screen
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


# Displaying "Score"
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# Old obstacle movement
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


# Old collision code
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# How to create sprite colision using groups
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# How to define a player aimation and jump mechanic
def player_animation():
    # play walking animation if the player is on the floor
    # display the jump animation if the players isn't on the floor
    global player_surf, player_index
# Jump
    if player_rect.bottom < 300:
        player_surf = player_jump
# Walk
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


# Creating window and defining the basics
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Audio/music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.2)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# For importing images into surface
# test_surface = pygame.image.load('folder/file.extension')
# convert() and convert_alpha() to make processing less stressing to ur pc

# For plain collor fill into surface
# test_surface = pygame.Surface((100,200))
# test_surface.fill('Red')

# Background and floor imports
sky_surf = pygame.image.load('Art/Background/Sky.png').convert()
ground_surf = pygame.image.load('Art/Background/Ground.png').convert()

# Old text and rect that turned into "Score"
# score_surf = test_font.render('My Game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))

# Snail imports
snail_frame_1 = pygame.image.load('Art/Enemies/Snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Art/Enemies/Snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_index = 0
snail_surf = snail_frames[int(snail_index)]

# Fly imports
fly_frame_1 = pygame.image.load('Art/Enemies/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Art/Enemies/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surf = fly_frames[int(fly_index)]

obstacle_rect_list = []

# Player imports
player_walk_1 = pygame.image.load('Art/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Art/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('Art/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_grav = 0

# Intro screen imports and image scale
player_stand = pygame.image.load('Art/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render(f'PIXEL RUNNER', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 70))

start_game = test_font.render(f'Press SPACE to start', False, (111, 196, 169))
start_game_rect = start_game.get_rect(center=(400, 330))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    # Imputs and Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_grav = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            # New spawn rate
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

            # Old spawn rate outside the Class
                # if randint(0, 2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 210)))

        # Snail animation, unlike the player animation it is defined in a different way
            if event.type == snail_animation_timer:
                snail_surf = snail_frames[snail_index]
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0

        # Fly animation, unlike the player animation it is defined in a different way
            if event.type == fly_animation_timer:
                fly_surf = fly_frames[fly_index]
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0

# Blits the sky and ground surface at their respective x & y position, blits the score too
    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()

        # Old score text, where it would appear, his collors in hexadecimal, his rect and screen blit
        # pygame.draw.rect(screen, '#c0e8ec', score_rect)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, 10)
        # screen.blit(score_surf, score_rect)

        # Old snail movement
        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)

        # Old player movement, animation, gravity and screen blit
        # player_grav += 1
        # player_rect.y += player_grav
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf, player_rect)

    # PLayer Group Sprites and Updates through frames
        player.draw(screen)
        player.update()

    # Obstacles Group Sprites and Updates through frames
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Old obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    # collision
        game_active = collision_sprite()

        # Old collision code
        # game_active = collisions(player_rect, obstacle_rect_list)

# Intro and Game Over Screen are the same.
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_grav = 0

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
    # Here the screen can alternate into the "Start Game" and "Press Start" to "Your Score: ...".
        if score == 0:
            screen.blit(start_game, start_game_rect)
        else:
            screen.blit(score_message, score_message_rect)

# Defines the update and "FPS".
    pygame.display.update()
    clock.tick(60)
