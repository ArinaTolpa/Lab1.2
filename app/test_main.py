import pytest
import pygame
from main import Character, Wall, Coin, GameStats
import numpy as np

# Фикстура для инициализации Pygame и создания персонажа
@pytest.fixture
def setup_character():
    pygame.init()
    character = Character()
    walls = [
        Wall((100, 100)),  # Создаем стену для проверки столкновения
    ]
    return character, walls

# Тест для проверки начальной позиции персонажа
def test_initial_position(setup_character):
    character, _ = setup_character
    assert character.rect.x == 32
    assert character.rect.y == 32

# Тест для проверки движения персонажа вправо без столкновений
def test_move_right_no_collision(setup_character):
    character, walls = setup_character
    initial_x = character.rect.x
    character.move(10, 0, walls)
    assert character.rect.x == initial_x + 10
    assert character.rect.y == 32

# Тест для проверки движения персонажа влево без столкновений
def test_move_left_no_collision(setup_character):
    character, walls = setup_character
    initial_x = character.rect.x
    character.move(-10, 0, walls)
    assert character.rect.x == initial_x - 10
    assert character.rect.y == 32

# Тест для проверки движения персонажа вверх без столкновений
def test_move_up_no_collision(setup_character):
    character, walls = setup_character
    initial_y = character.rect.y
    character.move(0, -10, walls)
    assert character.rect.x == 32
    assert character.rect.y == initial_y - 10

# Тест для проверки движения персонажа вниз без столкновений
def test_move_down_no_collision(setup_character):
    character, walls = setup_character
    initial_y = character.rect.y
    character.move(0, 10, walls)
    assert character.rect.x == 32
    assert character.rect.y == initial_y + 10

# Тест для проверки столкновения со стеной справа
def test_collision_right(setup_character):
    character, walls = setup_character
    character.rect.topleft = (90, 100)  # Устанавливаем персонажа рядом со стеной
    character.move(20, 0, walls)
    assert character.rect.right == walls[0].rect.left

# Тест для проверки столкновения со стеной слева
def test_collision_left(setup_character):
    character, walls = setup_character
    character.rect.topleft = (110, 100)  # Устанавливаем персонажа рядом со стеной
    character.move(-20, 0, walls)
    assert character.rect.left == walls[0].rect.right

# Тест для проверки столкновения со стеной сверху
def test_collision_top(setup_character):
    character, walls = setup_character
    character.rect.topleft = (100, 90)  # Устанавливаем персонажа рядом со стеной
    character.move(0, 20, walls)
    assert character.rect.bottom == walls[0].rect.top

# Тест для проверки столкновения со стеной снизу
def test_collision_bottom(setup_character):
    character, walls = setup_character
    character.rect.topleft = (100, 110)  # Устанавливаем персонажа рядом со стеной
    character.move(0, -20, walls)
    assert character.rect.top == walls[0].rect.bottom

# Фикстура для создания монет
@pytest.fixture
def setup_coin():
    pos = (50, 50)
    positive_coin = Coin(pos)
    negative_coin = Coin(pos, negative=True)
    return positive_coin, negative_coin

# Тест для проверки начальной позиции монеты
def test_coin_position(setup_coin):
    positive_coin, _ = setup_coin
    assert positive_coin.rect.x == 50
    assert positive_coin.rect.y == 50

# Тест для проверки начальной позиции отрицательной монеты
def test_negative_coin_position(setup_coin):
    _, negative_coin = setup_coin
    assert negative_coin.rect.x == 50
    assert negative_coin.rect.y == 50

# Тест для проверки, что монета не отрицательная по умолчанию
def test_positive_coin_default(setup_coin):
    positive_coin, _ = setup_coin
    assert not positive_coin.negative

# Тест для проверки, что монета может быть отрицательной
def test_negative_coin_flag(setup_coin):
    _, negative_coin = setup_coin
    assert negative_coin.negative

@pytest.fixture
def setup_screen():
    pygame.init()
    screen_width, screen_height = 740, 580
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 36)
    return screen, font, screen_width, screen_height

# Тест для проверки отображения статистики игры
def test_gamestats_display(setup_screen):
    screen, font, screen_width, screen_height = setup_screen
    message = "Тестовое сообщение"
    coin_count = 5

    # Вызов функции для отображения статистики
    GameStats(screen, font, message, coin_count, screen_width, screen_height)

    # Сохранение содержимого экрана в изображение
    pygame.image.save(screen, "screenshot.png")

    # Проверка, что изображение не пустое
    image = pygame.image.load("screenshot.png")
    image_array = pygame.surfarray.array3d(image)
    
    # Проверка, что экран не пуст (на нем что-то отрисовано)
    assert np.any(image_array != 0), "Screen is empty"

    # Проверка, что сообщение отобразилось правильно
    text_surface = font.render(message, True, (255, 255, 255))
    text_x = screen_width // 2 - text_surface.get_width() // 2
    text_y = screen_height // 2 - text_surface.get_height() // 2 + 20

    text_rendered_correctly = True
    for y in range(text_surface.get_height()):
        for x in range(text_surface.get_width()):
            if text_surface.get_at((x, y))[:3] != (0, 0, 0):  # Проверка только RGB значений
                if screen.get_at((text_x + x, text_y + y))[:3] != (255, 255, 255):
                    text_rendered_correctly = False
                    break
        if not text_rendered_correctly:
            break

    assert text_rendered_correctly, "Text is not rendered correctly on the screen"


# Закрытие Pygame после тестов
@pytest.fixture(scope="module", autouse=True)
def teardown_pygame():
    yield
    pygame.quit()