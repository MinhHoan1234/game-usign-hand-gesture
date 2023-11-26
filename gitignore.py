import pygame
import random

# Thiết lập các biến cấu hình
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GRAVITY = 0.5

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_stand = pygame.Surface((40, 60))  # Hình ảnh khi đứng
        self.image_stand.fill((0, 128, 0))  # Màu xanh lá cây
        self.image_duck = pygame.Surface((40, 40))  # Hình ảnh khi cúi
        self.image_duck.fill((0, 128, 0))  # Màu xanh lá cây
        self.image = self.image_stand  # Hình ảnh mặc định là đứng
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.velocity = 0
        self.ducking = False

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.velocity = 0

    def jump(self):
        if self.rect.y == SCREEN_HEIGHT - self.rect.height:
            self.velocity -= 10

    def duck(self):
        self.ducking = True
        self.image = self.image_duck
        self.rect.height = self.image.get_height()

    def stand_up(self):
        self.ducking = False
        self.image = self.image_stand
        self.rect.height = self.image.get_height()

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 40))  # Tạo hình ảnh cho cây xương rồng
        self.image.fill((139, 69, 19))  # Màu nâu đậm
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - self.rect.height

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.kill()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((25, 30))  # Tạo hình ảnh cho con chim
        self.image.fill((255, 0, 0))  # Màu đỏ
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(250, 350)  # Vị trí ngẫu nhiên theo chiều y

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -self.rect.width:
            self.kill()

# Thiết lập màn hình và các sprite
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()
dinosaur = Dinosaur()
sprites.add(dinosaur)

score = 0
font = pygame.font.Font(None, 36)

running = True
game_over = False  # Trạng thái game over

# Hình ảnh nút chơi lại
replay_button_img = pygame.Surface((100, 50))
replay_button_img.fill((0, 0, 255))  # Màu xanh dương
replay_button_rect = replay_button_img.get_rect()
replay_button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

while running:
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button_rect.collidepoint(event.pos):  # Kiểm tra nút chơi lại đã được nhấn
                    sprites.empty()
                    dinosaur = Dinosaur()
                    sprites.add(dinosaur)
                    score = 0
                    game_over = False

        screen.fill((255, 255, 255))
        sprites.draw(screen)
        screen.blit(replay_button_img, replay_button_rect)

        pygame.display.flip()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dinosaur.jump()
                elif event.key == pygame.K_DOWN:
                    dinosaur.duck()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dinosaur.stand_up()

        sprites.update()

        if random.randint(0, 120) < 1:
            cactus = Cactus()
            sprites.add(cactus)
        if random.randint(0, 30) < 1:
            bird = Bird()
            sprites.add(bird)

        screen.fill((255, 255, 255))
        sprites.draw(screen)

        collision_list = pygame.sprite.spritecollide(dinosaur, sprites, False)
        if len(collision_list) > 1:
            game_over = True

        score += 1
        score_text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
