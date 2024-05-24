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

# Тест для проверки отображения экрана подтверждения выхода
#@patch('sys.exit')  # Мок для перехвата вызова sys.exit
#def test_confirm_exit(mock_exit, setup_pygame):
#    screen, font = setup_pygame
#    screen_width, screen_height = screen.get_size()

    # Использование pygame.event.post для имитации нажатия клавиши
#    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_y))

    # Запуск цикла событий для обработки события
#    pygame.event.pump()

#    ConfirmExit(screen, font, screen_width, screen_height)

    # Проверка, что sys.exit был вызван
#    mock_exit.assert_called_once()

# Тест для проверки отображения начального экрана
#def test_show_start_screen(setup_pygame):
#    screen, font = setup_pygame
#    screen_width, screen_height = screen.get_size()
#    ShowStartScreen(screen, font, screen_width, screen_height)
#    assert pygame.display.get_surface() is not None  # Проверка, что экран обновлен


# Точка входа для запуска тестов
if __name__ == "__main__":
    pytest.main()
