import pygame
import random

class Player:
    def __init__(self, x, y, is_bot=False):
        self.rect = pygame.Rect(x, y, 231, 190)

        # variables for player attributes

        self.color = (255, 0, 0)
        self.speed = 15
        self.vel_y = 0
        self.attack_type = None
        self.is_attacking = False
        self.attack_direction = True
        self.health = 100
        self.flipFace = True
        self.hitAttack = False
        self.attack_cooldown = 500
        self.last_attack_time = 0

        self.is_bot = is_bot
        self.darken_bot = is_bot # Variable to darken bot's colour

        if self.is_bot:
            self.bot_move_timer = pygame.time.get_ticks()
            self.bot_move_duration = 0
            self.bot_current_dx = 0
            self.bot_next_attack_time = pygame.time.get_ticks() + random.randint(1000, 3000)
            self.bot_attack_range_threshold = 350
            self.bot_jump_chance = 0.005
        else:
            self.control_keys = { # Control keys for human player
                'left': pygame.K_a,
                'right': pygame.K_d,
                'jump': pygame.K_w,
                'attack1': pygame.K_x,
                'attack2': pygame.K_z
            }

        self.load_animations()

        self.attack_animation_finished = False

        self.is_dead = False # Death check
        self.death_animation_finished = False # Variable for death animation state


    def move(self, screen_width, ground_y, surface, target):
        # Checks if player dead, so they can't do anything
        if self.is_dead: 
            return
        
        # Movement and time variables
        current_time = pygame.time.get_ticks()
        gravity = 2.5
        jump_force = -20
        dx = 0
        dy = 0

        if not self.is_bot:
            keys = pygame.key.get_pressed()

        # Allow movement if not attacking and not dead
        if not self.is_attacking or self.attack_animation_finished:
            if self.is_bot:
                # Bot movement random logic
                if current_time - self.bot_move_timer > self.bot_move_duration:
                    self.bot_move_timer = current_time
                    self.bot_move_duration = random.randint(500, 2000)

                    distance_to_target = target.rect.centerx - self.rect.centerx

                    if abs(distance_to_target) < self.bot_attack_range_threshold - 100:
                        self.bot_current_dx = -self.speed if distance_to_target > 0 else self.speed
                        self.bot_move_duration = random.randint(300, 800)
                    elif abs(distance_to_target) > self.bot_attack_range_threshold + 50:
                        self.bot_current_dx = self.speed if distance_to_target > 0 else -self.speed
                        self.bot_move_duration = random.randint(500, 1500)
                    else:
                        self.bot_current_dx = random.choice([-self.speed, 0, self.speed])
                        self.bot_move_duration = random.randint(300, 1000)

                dx = self.bot_current_dx

                if dx < 0:
                    self.flipFace = False
                elif dx > 0:
                    self.flipFace = True

                if random.random() < self.bot_jump_chance and self.rect.bottom >= ground_y:
                    self.vel_y = jump_force

                # Bot attack logic
                if not self.is_attacking and current_time >= self.bot_next_attack_time:
                    distance_to_target_abs = abs(self.rect.centerx - target.rect.centerx)

                    if distance_to_target_abs < self.bot_attack_range_threshold:
                        self.start_attack(random.choice(['attack1', 'attack2']))
                        self.last_attack_time = current_time
                        self.bot_next_attack_time = current_time + random.randint(self.attack_cooldown, 2000)
                    else:
                        self.bot_next_attack_time = current_time + random.randint(100, 500)

            else: # Now player (human) controls
                if keys[self.control_keys['left']]: # Flips direction based on key presses
                    dx = -self.speed
                    self.flipFace = False
                elif keys[self.control_keys['right']]:
                    dx = self.speed
                    self.flipFace = True

                if keys[self.control_keys['jump']] and self.rect.bottom >= ground_y:
                    self.vel_y = jump_force

                if not self.is_attacking and (current_time - self.last_attack_time > self.attack_cooldown):
                    if keys[self.control_keys['attack2']]: # Attack types
                        self.start_attack('attack2')
                        self.last_attack_time = current_time
                    elif keys[self.control_keys['attack1']]:
                        self.start_attack('attack1')
                        self.last_attack_time = current_time

        self.vel_y += gravity # Gravity checks for jump
        dy += self.vel_y

        if self.rect.left + dx < -50: # Boundary check
            dx = -50 - self.rect.left
        if self.rect.right + dx > screen_width + 50:
            dx = (screen_width + 50) - self.rect.right

        if self.rect.bottom + dy >= ground_y:
            self.rect.bottom = ground_y
            dy = 0
            self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        if self.is_attacking:
            self.perform_attack(surface, target) # Performs to attack method

    def start_attack(self, attack_type_name): # Sets variables based on starting attack
        self.is_attacking = True
        self.attack_type = attack_type_name
        self.attack_direction = self.flipFace
        self.hitAttack = False
        self.current_action = attack_type_name
        self.current_frame_index = 0
        self.frame_timer = pygame.time.get_ticks()
        self.attack_animation_finished = False

    def perform_attack(self, surface, target):
            # Dead targets can't attack
            if target.is_dead:
                return

            attack_width = 0
            attack_y_offset = 0
            attack_height = self.rect.height

            # Attack range and damage based on attack type

            if self.attack_type == 'attack1':
                attack_width = 90
                attack_y_offset = 0
                damage = 5
            elif self.attack_type == 'attack2':
                attack_width = 2
                attack_y_offset = 0
                damage = 10
            else:
                attack_width = 150
                attack_y_offset = 0
                attack_height = self.rect.height
                damage = 0.25

            if self.attack_direction:
                attack_rect = pygame.Rect(self.rect.right, self.rect.y + attack_y_offset, attack_width, attack_height)
            else:
                attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.y + attack_y_offset, attack_width, attack_height)

            if attack_rect.colliderect(target.rect):
                if not self.hitAttack:
                    print("Hit with", self.attack_type, "!")
                    target.health -= damage
                    self.hitAttack = True
                    # If target dead from hit, sets death states to true
                    if target.health <= 0: 
                        target.is_dead = True
                        target.current_action = 'death'
                        target.current_frame_index = 0 
                        target.frame_timer = pygame.time.get_ticks()
                        print(f"Player {target.rect.topleft} has died!") # I used to debug


    # Loading animations from wizard pack
    def load_animations(self):
        self.animations = {
            'idle': load_frames_from_spritesheet("assets/Wizard Pack/Idle.png", 6, 231, 190), # Calculated based on size of files
            'attack1': load_frames_from_spritesheet("assets/Wizard Pack/Attack1.png", 8, 231, 190),
            'attack2': load_frames_from_spritesheet("assets/Wizard Pack/Attack2.png", 8, 231, 190),
            'death': load_frames_from_spritesheet("assets/Wizard Pack/Death.png", 6, 231, 190) 
        }

        self.current_action = 'idle' # Current state of player
        self.current_frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 100

    def update_animation(self):
        now = pygame.time.get_ticks()

        # If player is dead, stops updating animation
        if self.is_dead and self.death_animation_finished:
            return

        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.current_frame_index += 1

            # Handles animation frame logic
            if self.current_frame_index >= len(self.animations[self.current_action]):
                if self.current_action == 'death': 
                    self.current_frame_index = len(self.animations[self.current_action]) - 1 
                    self.death_animation_finished = True 
                elif self.current_action in ['idle', 'attack1', 'attack2']: 
                    self.is_attacking = False
                    self.attack_type = None
                    self.current_action = 'idle'
                    self.attack_animation_finished = True
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = 0

    def draw(self, surface):
        self.update_animation() # Updates frame before drawing
        frame = self.animations[self.current_action][self.current_frame_index]

        # Darkeing filter to bot for shadow effect and distiguish
        if self.darken_bot: 
            frame = self._apply_darken_filter(frame, 0.1) # Darken factor 0.1

        flipped = pygame.transform.flip(frame, not self.flipFace, False)

        frame_rect = flipped.get_rect(midbottom=self.rect.midbottom)
        surface.blit(flipped, frame_rect)

    # Darkening filter helper function
    def _apply_darken_filter(self, surface, factor):
        new_surface = surface.copy()
        new_surface = new_surface.convert_alpha() # Transparency
        
        # Creates, and blends dark overlay
        dark_overlay = pygame.Surface(new_surface.get_size(), pygame.SRCALPHA)
        dark_overlay.fill((0, 0, 0, int(255 * (1 - factor))))
        new_surface.blit(dark_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return new_surface


def load_frames_from_spritesheet(path, num_frames, width, height):
    sheet = pygame.image.load(path).convert_alpha() # Loads frames outside class
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(pygame.Rect(i * width, 0, width, height))
        frames.append(frame)
    return frames
