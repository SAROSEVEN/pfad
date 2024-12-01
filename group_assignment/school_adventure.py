import pygame
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Window setup
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("School Adventure")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
SKY_BLUE = (135, 206, 250)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 60
        self.original_image = pygame.image.load('assets/player.png')
        self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH // 2
        self.rect.y = WINDOW_HEIGHT // 2
        self.speed = 5
        self.direction = "right"
        self.caught_count = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = pygame.transform.flip(self.original_image, True, False)
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            self.image = self.original_image
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed

class Target(pygame.sprite.Sprite):
    def __init__(self, target_type="normal"):
        super().__init__()
        self.target_type = target_type
        self.size = 50
        
        image_paths = {
            "normal": "assets/normal_target.png",
            "fast": "assets/fast_target.png",
            "special": "assets/special_target.png"
        }
        self.original_image = pygame.image.load(image_paths[target_type])
        self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.reset_position()
        
        self.properties = {
            "normal": {"speed": 3, "points": 1},
            "fast": {"speed": 6, "points": 2},
            "special": {"speed": 4, "points": 3}
        }[target_type]
        
        self.speed = self.properties["speed"]
        self.points = self.properties["points"]
        self.direction = random.randint(0, 360)

    def reset_position(self):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = -self.size
        elif side == 'bottom':
            self.rect.x = random.randint(0, WINDOW_WIDTH)
            self.rect.y = WINDOW_HEIGHT
        elif side == 'left':
            self.rect.x = -self.size
            self.rect.y = random.randint(0, WINDOW_HEIGHT)
        else:
            self.rect.x = WINDOW_WIDTH
            self.rect.y = random.randint(0, WINDOW_HEIGHT)

    def update(self):
        if self.target_type == "special" and random.random() < 0.02:
            self.direction = random.randint(0, 360)
        
        angle = math.radians(self.direction)
        dx = math.cos(angle) * self.speed
        self.rect.x += dx
        self.rect.y += math.sin(angle) * self.speed
        
        if dx > 0:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)

        if (self.rect.right < 0 or self.rect.left > WINDOW_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT):
            self.reset_position()

class MovingStudent(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 50
        self.image = pygame.image.load('assets/student.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.reset_position()
        self.speed = random.randint(3, 6)
        self.direction = random.choice([-1, 1])

    def reset_position(self):
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.size)
        self.rect.y = random.randint(0, WINDOW_HEIGHT - self.size)

    def update(self):
        self.rect.x += self.speed * self.direction
        
        if self.rect.right > WINDOW_WIDTH or self.rect.left < 0:
            self.direction *= -1
            if self.direction > 0:
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = pygame.transform.flip(self.image, False, False)

class Game:
    def __init__(self, start_level=1):
        pygame.mixer.music.stop()
        if start_level == 1:
            pygame.mixer.music.load('assets/background_music_level1.mp3')
        else:
            pygame.mixer.music.load('assets/background_music_level2.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        
        self.catch_sound = pygame.mixer.Sound('assets/catch.wav')
        self.game_over_sound = pygame.mixer.Sound('assets/gameover.wav')
        if start_level == 1:
            self.level_complete_sound = pygame.mixer.Sound('assets/level1_complete.wav')
        else:
            self.level_complete_sound = pygame.mixer.Sound('assets/level2_complete.wav')
        self.game_over_sound.set_volume(0.2)
        
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self.cafeteria_students = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.score = 0
        self.level = start_level
        self.game_over = False
        self.level_complete = False
        self.font = pygame.font.Font(None, 36)
        self.timer = 60
        self.start_time = pygame.time.get_ticks()
        self.show_tutorial = True if start_level == 1 else False
        
        if start_level == 1:
            self.add_initial_targets()
        else:
            self.init_level_two()

    def draw_custom_background(self, surface):
        if self.level == 1:
            background = pygame.image.load('assets/background_level1.png')
        else:
            background = pygame.image.load('assets/background_level2.png')
        background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        surface.blit(background, (0, 0))

    def add_initial_targets(self):
        for _ in range(3):
            self.add_target("normal")
        for _ in range(2):
            self.add_target("fast")
        self.add_target("special")

    def add_target(self, target_type):
        target = Target(target_type)
        self.all_sprites.add(target)
        self.targets.add(target)

    def init_level_two(self):
        self.timer = 60
        self.start_time = pygame.time.get_ticks()
        self.level_complete = False
        self.game_over = False
        
        for sprite in self.targets:
            sprite.kill()
            
        for _ in range(8):
            student = MovingStudent()
            self.cafeteria_students.add(student)
            self.all_sprites.add(student)

    def draw_tutorial(self):
        tutorial_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        tutorial_surface.fill((0, 0, 0, 128))
        
        messages = [
            "Welcome to School Adventure - Catch Truant Students!",
            "Use arrow keys to move",
            "Catch different types of targets:",
            "Red: Normal (1 point)",
            "Orange: Fast (2 points)",
            "Purple: Special (3 points)",
            "Score 80 points to unlock the next level!",
            "Press SPACE to start!"
        ]
        
        y_offset = 150
        for message in messages:
            text = self.font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            tutorial_surface.blit(text, text_rect)
            y_offset += 50
        
        screen.blit(tutorial_surface, (0, 0))

    def update(self):
        if self.show_tutorial:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.show_tutorial = False
                self.start_time = pygame.time.get_ticks()
            return

        if not self.game_over and not self.level_complete:
            if self.level == 1:
                self.update_level_one()
            elif self.level == 2:
                self.update_level_two()

    def update_level_one(self):
        self.all_sprites.update()
        
        caught = pygame.sprite.spritecollide(self.player, self.targets, True)
        for target in caught:
            self.score += target.points
            self.catch_sound.play()
            self.add_target(random.choice(["normal", "fast", "special"]))

        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        self.timer = max(60 - elapsed_time, 0)
        
        if self.timer <= 0:
            if self.score >= 80:
                self.level_complete = True
                self.level_complete_sound.play()
            else:
                self.game_over = True
                self.game_over_sound.play()

    def update_level_two(self):
        self.all_sprites.update()
        
        if pygame.sprite.spritecollideany(self.player, self.cafeteria_students):
            self.game_over = True
            self.game_over_sound.play()
            return
            
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        self.timer = max(60 - elapsed_time, 0)
        
        if self.timer <= 0:
            self.level_complete = True
            self.level_complete_sound.play()

    def draw(self):
        self.draw_custom_background(screen)
        
        if self.show_tutorial:
            self.draw_tutorial()
            return

        self.all_sprites.draw(screen)
        
        score_text = self.font.render(f'Level {self.level} - Score: {self.score}', True, WHITE)
        time_text = self.font.render(f'Time: {self.timer}', True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (10, 50))

        if self.game_over:
            self.draw_game_over()
        elif self.level_complete:
            if self.level == 1:
                self.draw_level_complete()
            else:
                self.draw_final_victory()

    def draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render('Game Over!', True, WHITE)
        final_score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        restart_text = self.font.render('Press R to Restart', True, WHITE)
        
        screen.blit(game_over_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 50))
        screen.blit(final_score_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2))
        screen.blit(restart_text, (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 + 50))

    def draw_level_complete(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        messages = [
            "Level Complete!",
            "Next Level: Cafeteria Challenge",
            "Dodge students with food trays!",
            "Press SPACE to continue"
        ]
        
        y_offset = WINDOW_HEIGHT // 3
        for message in messages:
            text = self.font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 50

    def draw_final_victory(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))
        
        messages = [
            "Congratulations!",
            "You completed the School Adventure!",
            "You won a Pineapple Pizza!",
        ]
        
        y_offset = WINDOW_HEIGHT // 3
        for message in messages:
            text = self.font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 50

def main():
    clock = pygame.time.Clock()
    game = Game()
    running = True
    current_level = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game = Game(start_level=game.level)
                elif event.key == pygame.K_SPACE and game.level_complete and game.level == 1:
                    current_level = 2
                    game = Game(start_level=2)

        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()