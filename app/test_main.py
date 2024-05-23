import pytest
import pygame
from unittest.mock import patch, MagicMock
from main import Character, Wall, Coin, GameStats, ConfirmExit, ShowStartScreen
import sys
from pygame.locals import QUIT, KEYDOWN, K_y, K_n


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
def setup_pygame():
    screen = MagicMock()
    font = MagicMock()
    return screen, font

@patch('pygame.display.flip')
@patch('pygame.time.wait')
def test_GameStats(mock_wait, mock_flip, setup_pygame):
    screen, font = setup_pygame
    message = "Тестовое сообщение"
    coin_count = 5
    screen_width = 740
    screen_height = 580

    # Мок объектов pygame для тестирования
    stats_text = MagicMock()
    message_text = MagicMock()
    
    # Настройка mock для методов render и get_width
    font.render.side_effect = [stats_text, message_text]
    stats_text.get_width.return_value = 200
    stats_text.get_height.return_value = 50
    message_text.get_width.return_value = 200
    message_text.get_height.return_value = 50

    GameStats(screen, font, message, coin_count, screen_width, screen_height)

    # Проверка, что render был вызван дважды
    assert font.render.call_count == 2

    # Проверка аргументов для render
    font.render.assert_any_call(f"Всего собрано монет: {coin_count}", True, (255, 255, 255))
    font.render.assert_any_call(message, True, (255, 255, 255))

    # Проверка, что flip и wait были вызваны
    mock_flip.assert_called_once()
    mock_wait.assert_called_once_with(3000)

    # Проверка вызовов blit
    screen.blit.assert_any_call(stats_text, (screen_width // 2 - 200 // 2, screen_height // 2 - 50 // 2 - 20))
    screen.blit.assert_any_call(message_text, (screen_width // 2 - 200 // 2, screen_height // 2 - 50 // 2 + 20))

######
def test_ConfirmExit_no_quit(monkeypatch):
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 36)

    # Мокирование событий для нажатия клавиши 'N'
    def mock_get():
        return [
            pygame.event.Event(KEYDOWN, {'key': K_n}),
        ]

    monkeypatch.setattr(pygame.event, 'get', mock_get)

    quit_called = []

    def mock_quit():
        quit_called.append(True)
        raise SystemExit

    monkeypatch.setattr(pygame, 'quit', mock_quit)

    try:
        ConfirmExit(screen, font, screen_width, screen_height)
    except SystemExit:
        pytest.fail("Неожиданный SystemExit при ConfirmExit с клавишей 'N'")

    assert not quit_called, "pygame.quit() был вызван при нажатии клавиши 'N'"

    # Восстановление оригинальной функции pygame.quit для предотвращения SystemExit
    monkeypatch.undo()
    pygame.quit()

def test_ConfirmExit_yes_quit(monkeypatch):
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 36)

    # Мокирование событий для нажатия клавиши 'Y'
    def mock_get_exit():
        return [
            pygame.event.Event(KEYDOWN, {'key': K_y}),
        ]

    monkeypatch.setattr(pygame.event, 'get', mock_get_exit)

    def mock_quit():
        raise SystemExit

    monkeypatch.setattr(pygame, 'quit', mock_quit)

    with pytest.raises(SystemExit):
        ConfirmExit(screen, font, screen_width, screen_height)

    # Восстановление оригинальной функции pygame.quit для предотвращения SystemExit
    monkeypatch.undo()
######

# Закрытие Pygame после тестов
@pytest.fixture(scope="module", autouse=True)
def teardown_pygame():
    yield
    pygame.quit()