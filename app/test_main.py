import pytest
import pygame
import sys
import os
from unittest.mock import patch

# Добавление пути к папке app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Character, Coin, Wall, GameStats, ConfirmExit, ShowStartScreen

# Фикстура для инициализации Pygame
@pytest.fixture(scope="module")
def init_pygame():
    pygame.init()
    yield
    pygame.quit()

# Фикстура для создания экрана и шрифта
@pytest.fixture
def setup_pygame(init_pygame):
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 36)
    yield screen, font  # Используем yield вместо return, чтобы удерживать контекст Pygame активным
    pygame.display.quit()  # Закрываем дисплей после завершения тестов

# Тест для проверки перемещения персонажа
def test_character_movement(setup_pygame):
    screen, font = setup_pygame
    walls = [Wall((50, 50))]  # Создание стены на позиции (50, 50)
    player = Character()  # Создание персонажа

    # Проверка начальной позиции персонажа
    assert player.rect.topleft == (32, 32)

    # Перемещение вправо
    player.move(10, 0, walls)
    assert player.rect.topleft == (42, 32)

    # Перемещение вниз и столкновение со стеной
    player.move(0, 20, walls)
    assert player.rect.bottom == 50  # Позиция должна быть ограничена стеной

# Тест для проверки взаимодействия персонажа с монетой
def test_coin_interaction():
    player = Character()
    coin = Coin((50, 50))  # Создание монеты на позиции (50, 50)

    # Проверка, что изначально персонаж не сталкивается с монетой
    assert not player.rect.colliderect(coin.rect)

    # Перемещение персонажа на позицию монеты
    player.rect.topleft = (50, 50)
    assert player.rect.colliderect(coin.rect)  # Проверка столкновения

# Тест для проверки создания стены
def test_wall_creation():
    wall = Wall((100, 100))  # Создание стены на позиции (100, 100)
    assert wall.rect.topleft == (100, 100)  # Проверка позиции стены
    assert wall.rect.size == (16, 16)  # Проверка размера стены

# Тест для проверки отображения статистики игры
def test_game_stats(setup_pygame):
    screen, font = setup_pygame
    message = "Test Message"  # Сообщение для отображения
    coin_count = 5  # Количество монет для отображения
    screen_width, screen_height = screen.get_size()
    GameStats(screen, font, message, coin_count, screen_width, screen_height)
    assert pygame.display.get_surface() is not None  # Проверка, что экран обновлен

###############
@pytest.fixture
def pygame_init():
    pygame.init()
    screen_width, screen_height = 740, 580
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 36)
    yield screen, font, screen_width, screen_height
    pygame.quit()

def test_confirm_exit_yes(monkeypatch, pygame_init):
    screen, font, screen_width, screen_height = pygame_init

    # Simulate pressing the 'Y' key
    monkeypatch.setattr(pygame.event, 'get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_y)])

    with pytest.raises(SystemExit):  # Expecting a system exit when 'Y' is pressed
        ConfirmExit(screen, font, screen_width, screen_height)

def test_confirm_exit_no(monkeypatch, pygame_init):
    screen, font, screen_width, screen_height = pygame_init

    # Simulate pressing the 'N' key
    monkeypatch.setattr(pygame.event, 'get', lambda: [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_n)])

    # Run ConfirmExit and expect it to return without exiting
    ConfirmExit(screen, font, screen_width, screen_height)

def test_confirm_exit_quit(monkeypatch, pygame_init):
    screen, font, screen_width, screen_height = pygame_init

    # Simulate pressing the window close button
    monkeypatch.setattr(pygame.event, 'get', lambda: [pygame.event.Event(pygame.QUIT)])

    with pytest.raises(SystemExit):  # Expecting a system exit when QUIT event is detected
        ConfirmExit(screen, font, screen_width, screen_height)
###############

# Задаем размеры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

@pytest.fixture
def screen():
    # Создаем фиктивный экран для тестирования
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

@pytest.fixture
def font():
    # Инициализируем модуль шрифтов pygame
    pygame.font.init()
    # Создаем фиктивный шрифт для тестирования
    return pygame.font.SysFont(None, 36)

def test_show_start_screen(screen, font, mocker):
    # Мокаем экран и шрифт
    screen_mock = mocker.Mock()
    font_mock = mocker.Mock()

    # Мокаем метод render, чтобы он возвращал Surface
    font_mock.render.return_value = pygame.Surface((100, 50))

    # Мокаем очередь событий pygame, чтобы симулировать нажатие Enter
    mocker.patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})])
    mocker.patch('pygame.display.flip')

    # Вызываем тестируемую функцию
    ShowStartScreen(screen_mock, font_mock, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Проверяем, что метод render был вызван
    font_mock.render.assert_called_with("Нажмите Enter для начала игры", True, (255, 255, 255))

    # Проверяем, что дисплей обновился
    pygame.display.flip.assert_called()

# Фикстура для завершения работы pygame после всех тестов
@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    pygame.quit()

if __name__ == "__main__":
    pytest.main()
