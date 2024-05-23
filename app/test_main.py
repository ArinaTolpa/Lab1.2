import pytest
import pygame
from main import Character, Wall, Coin

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

# Закрытие Pygame после тестов
@pytest.fixture(scope="module", autouse=True)
def teardown_pygame():
    yield
    pygame.quit()