import pygame

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 231, 190)

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
        self.load_animations()


        self.attack_animation_finished = False


    def move(self, screen_width, ground_y, surface, target):
        current_time = pygame.time.get_ticks()
        gravity = 2.5
        jump_force = -20
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()

        if not self.is_attacking or self.attack_animation_finished:
            if keys[pygame.K_a]:
                dx = -self.speed
                self.flipFace = False
            elif keys[pygame.K_d]:
                dx = self.speed
                self.flipFace = True


            if keys[pygame.K_w] and self.rect.bottom >= ground_y:
                self.vel_y = jump_force


        if (keys[pygame.K_x] or keys[pygame.K_z]) and \
           (current_time - self.last_attack_time > self.attack_cooldown) and \
           not self.is_attacking:
            self.start_attack()
            self.last_attack_time = current_time


        # Gravity
        self.vel_y += gravity
        dy += self.vel_y

        # Boundaries
        if self.rect.left + dx < -50:
            dx = -50 - self.rect.left
        if self.rect.right + dx > screen_width + 50:
            dx = (screen_width + 50) - self.rect.right

        # Ground Collision
        if self.rect.bottom + dy >= ground_y:
            self.rect.bottom = ground_y
            dy = 0
            self.vel_y = 0

        self.rect.x += dx
        self.rect.y += dy

        # Hitbox Logic
        if self.is_attacking:
            self.perform_attack(surface, target)

    def start_attack(self):
        self.is_attacking = True
        self.attack_direction = self.flipFace
        self.hitAttack = False # Resets attack state
        self.current_action = 'attack' # Animations witch
        self.current_frame_index = 0
        self.frame_timer = pygame.time.get_ticks() # Resets timer for smothness
        self.attack_animation_finished = False # Resets the attack animation state


    def perform_attack(self, surface, target):
        attack_width = 300 # Width of the attack hitbox
        attack_y_offset = 0 # Adjust

        if self.attack_direction: # Facing right
            attack_rect = pygame.Rect(self.rect.right, self.rect.y + attack_y_offset, attack_width, self.rect.height)
        else: # Facing left
            attack_rect = pygame.Rect(self.rect.left - attack_width, self.rect.y + attack_y_offset, attack_width, self.rect.height)

        if attack_rect.colliderect(target.rect):
            # Only apply damage once per attack animation
            if not self.hitAttack:
                print("Hit!")
                target.health -= 5
                self.hitAttack = True


    def load_animations(self):
        self.animations = {
            'idle': load_frames_from_spritesheet("assets/Wizard Pack/Idle.png", 6, 231, 190),
            'attack': load_frames_from_spritesheet("assets/Wizard Pack/Attack2.png", 8, 231, 190) # corrected check size
        }

        self.current_action = 'idle'
        self.current_frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 100 # General Speed for Frame:


    def update_animation(self):
        now = pygame.time.get_ticks()
        # time check
        if now - self.frame_timer > self.frame_speed:
            self.frame_timer = now
            self.current_frame_index += 1

            # Check if enough frames have been played
            if self.current_frame_index >= len(self.animations[self.current_action]):
                if self.current_action == 'attack':
                    self.is_attacking = False 
                    self.current_action = 'idle' # Reverts to idle animation
                    self.attack_animation_finished = True 
                    self.current_frame_index = 0
                else: 
                    self.current_frame_index = 0 

    def draw(self, surface):
        self.update_animation() # Updates animation
        frame = self.animations[self.current_action][self.current_frame_index]
        flipped = pygame.transform.flip(frame, not self.flipFace, False)

        # Alligns image
        frame_rect = flipped.get_rect(midbottom=self.rect.midbottom)
        surface.blit(flipped, frame_rect)


# Loading frames
def load_frames_from_spritesheet(path, num_frames, width, height):
    sheet = pygame.image.load(path).convert_alpha()
    frames = []
    for i in range(num_frames):
        
        frame = sheet.subsurface(pygame.Rect(i * width, 0, width, height))
        frames.append(frame)
    return frames