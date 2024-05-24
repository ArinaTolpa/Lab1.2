import os
import sys
import random
import pygame
import time

# Класс для игрока (оранжевого персонажа)
class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (32, 32)

    def move(self, dx, dy, walls):
        self.rect.x += dx
        self.rect.y += dy
        print(f"Переместился в: {self.rect.topleft}")

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                print(f"Столкновение: {self.rect} с {wall.rect}")
                if dx > 0:  # Движение вправо
                    self.rect.right = wall.rect.left
                if dx < 0:  # Движение влево
                    self.rect.left = wall.rect.right
                if dy > 0:  # Движение вниз
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Движение вверх
                    self.rect.top = wall.rect.bottom
                print(f"Скорректировано до: {self.rect.topleft}")

class Coin(object):
    def __init__(self, pos, negative=False):
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.negative = negative

class Wall(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

def LevelGenerator(width, height):
    maze = [[1] * width for _ in range(height)]
    
    def carve_passages_from(cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[cy + direction[1]][cx + direction[0]] = 0
                maze[ny][nx] = 0
                carve_passages_from(nx, ny)
    
    maze[1][1] = 0
    carve_passages_from(1, 1)
    return maze

def GameStats(screen, font, message, coin_count, screen_width, screen_height):
    screen.fill((0, 0, 0))
    stats_text = font.render(f"Всего собрано монет: {coin_count}", True, (255, 255, 255))
    message_text = font.render(message, True, (255, 255, 255))
    screen.blit(stats_text, (screen_width // 2 - stats_text.get_width() // 2, screen_height // 2 - stats_text.get_height() // 2 - 20))
    screen.blit(message_text, (screen_width // 2 - message_text.get_width() // 2, screen_height // 2 - message_text.get_height() // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)

def ConfirmExit(screen, font, screen_width, screen_height):
    screen.fill((0, 0, 0))
    confirm_text = font.render("Вы уверены, что хотите выйти? (Y/N)", True, (255, 255, 255))
    screen.blit(confirm_text, (screen_width // 2 - confirm_text.get_width() // 2, screen_height // 2 - confirm_text.get_height() // 2))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_y:
                    pygame.quit()
                    sys.exit()
                if e.key == pygame.K_n:
                    return
                
def ShowStartScreen(screen, font, screen_width, screen_height):
    screen.fill((0, 0, 0))
    start_text = font.render("Нажмите Enter для начала игры", True, (255, 255, 255))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 - start_text.get_height() // 2))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return

def initialize_game():
    # Инициализация pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Настройка экрана
    screen_width, screen_height = 740, 580
    # Смещение лабиринта для создания пространства для счетчика
    maze_offset_x, maze_offset_y = 0, 50
    pygame.display.set_caption("Достигните красного квадрата!")
    screen = pygame.display.set_mode((screen_width, screen_height))

    clock = pygame.time.Clock()
    walls = []  # Список для хранения стен
    player = Character()  # Создание игрока
    coins = []  # Список для хранения монет

    return screen, clock, walls, player, coins, screen_width, screen_height, maze_offset_x, maze_offset_y

def generate_maze_and_elements(maze_width, maze_height, maze_offset_x, maze_offset_y):
    maze = LevelGenerator(maze_width, maze_height)

    # Обеспечение проходимости стартовых и конечных позиций
    player_start = (1, 1)
    maze[1][1] = 0
    end_position = (maze_width - 2, maze_height - 2)
    maze[maze_height - 2][maze_width - 2] = 0

    walls = []
    coins = []
    positive_coin_count = 0
    negative_coin_count = 0

    # Парсинг сетки лабиринта и создание стен и монет
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x] == 1:
                # Создание стены
                walls.append(Wall((x * 16 + maze_offset_x, y * 16 + maze_offset_y)))
            elif (x, y) == player_start:
                # Установка начальной позиции игрока
                player.rect.topleft = (x * 16 + maze_offset_x, y * 16 + maze_offset_y)
            elif (x, y) == end_position:
                # Установка конечной позиции
                end_rect = pygame.Rect(x * 16 + maze_offset_x, y * 16 + maze_offset_y, 16, 16)
            elif random.random() < 0.1:  # Случайное размещение монет
                # Обеспечение меньшего количества отрицательных монет
                if negative_coin_count < positive_coin_count / 2:
                    is_negative = random.random() < 0.33
                else:
                    is_negative = False
                
                if is_negative:
                    negative_coin_count += 1
                else:
                    positive_coin_count += 1
                
                # Создание монеты
                coins.append(Coin((x * 16 + maze_offset_x, y * 16 + maze_offset_y), negative=is_negative))

    # Создание границ справа и снизу
    for x in range(maze_width):
        walls.append(Wall((x * 16 + maze_offset_x, maze_height * 16 + maze_offset_y)))
    for y in range(maze_height):
        walls.append(Wall((maze_width * 16 + maze_offset_x, y * 16 + maze_offset_y)))

    return maze, player_start, end_rect, walls, coins

def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            ConfirmExit(screen, font, screen_width, screen_height)

def move_player(player, walls):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0, walls)
    if key[pygame.K_RIGHT]:
        player.move(2, 0, walls)
    if key[pygame.K_UP]:
        player.move(0, -2, walls)
    if key[pygame.K_DOWN]:
        player.move(0, 2, walls)

def check_coin_collection(player, coins, coin_count):
    for coin in coins[:]:
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)  # Удаление монеты, если игрок ее собирает
            if coin.negative:
                if coin_count > 0:  # Уменьшение счетчика монет только если он больше нуля
                    coin_count -= 1
            else:
                coin_count += 1  # Увеличение счетчика монет, если это положительная монета
    return coin_count

def check_game_end(player, end_rect, coin_count, start_time, screen, font, screen_width, screen_height):
    elapsed_time = time.time() - start_time
    if coin_count >= 20:
        GameStats(screen, font, f"Вы победили! Время: {elapsed_time:.2f} секунд", coin_count, screen_width, screen_height)
        pygame.quit()
        sys.exit()

    if player.rect.colliderect(end_rect):
        GameStats(screen, font, f"Время: {elapsed_time:.2f} секунд", coin_count, screen_width, screen_height)
        pygame.quit()
        sys.exit()

    if elapsed_time > max_time:
        GameStats(screen, font, f"Время истекло", coin_count, screen_width, screen_height)
        pygame.quit()
        sys.exit()

def draw_scene(screen, walls, coins, player, end_rect, coin_count, elapsed_time, screen_width):
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for coin in coins:
        color = (255, 0, 0) if coin.negative else (255, 255, 0)  # Красные для отрицательных монет, желтые для положительных
        pygame.draw.ellipse(screen, color, coin.rect)  # Отрисовка монет
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)

    # Отображение счетчика монет и таймера вне области лабиринта
    coin_text = font.render(f"Монеты: {coin_count}", True, (255, 255, 255))
    screen.blit(coin_text, (10, 10))
    
    timer_text = font.render(f"Время: {elapsed_time:.2f} с", True, (255, 255, 255))
    screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, 10))

    pygame.display.flip()

if __name__ == "__main__":
    screen, clock, walls, player, coins, screen_width, screen_height, maze_offset_x, maze_offset_y = initialize_game()
    maze_width, maze_height = 40, 30
    maze, player_start, end_rect, walls, coins = generate_maze_and_elements(maze_width, maze_height, maze_offset_x, maze_offset_y)

    # Инициализация счетчика монет и таймера
    coin_count = 0
    font = pygame.font.SysFont(None, 36)
    start_time = time.time()
    max_time = 120  # Максимальное время в секундах

    # Показ начального экрана
    ShowStartScreen(screen, font, screen_width, screen_height)

    # Начало игры
    running = True
    start_time = time.time()
    while running:
        clock.tick(60)
        handle_events()
        move_player(player, walls)
        coin_count = check_coin_collection(player, coins, coin_count)
        check_game_end(player, end_rect, coin_count, start_time, screen, font, screen_width, screen_height)
        
        elapsed_time = time.time() - start_time
        draw_scene(screen, walls, coins, player, end_rect, coin_count, elapsed_time, screen_width)

    pygame.quit()
