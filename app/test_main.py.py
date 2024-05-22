import pytest
import pygame
import time
from main import Character, Coin, Wall, LevelGenerator, GameStats, ConfirmExit, ShowStartScreen

# Инициализация pygame для тестов
pygame.init()

@pytest.fixture
def setup_walls():
    return []

@pytest.fixture
def setup_coins():
    return []

def test_character_initialization():
    player = Character()
    assert player.rect.x == 32
    assert player.rect.y == 32
    assert player.rect.width == 16
    assert player.rect.height == 16

def test_character_move():
    player = Character()
    walls = []
    player.move(10, 0)
    assert player.rect.x == 42
    player.move(0, 10)
    assert player.rect.y == 42
    player.move(-10, -10)
    assert player.rect.x == 32
    assert player.rect.y == 32

def test_coin_initialization():
    coin = Coin((100, 100))
    assert coin.rect.x == 100
    assert coin.rect.y == 100
    assert coin.rect.width == 10
    assert coin.rect.height == 10
    assert not coin.negative

    negative_coin = Coin((150, 150), negative=True)
    assert negative_coin.rect.x == 150
    assert negative_coin.rect.y == 150
    assert negative_coin.rect.width == 10
    assert negative_coin.rect.height == 10
    assert negative_coin.negative

def test_wall_initialization():
    walls = []
    wall = Wall((200, 200))
    walls.append(wall)
    assert wall.rect.x == 200
    assert wall.rect.y == 200
    assert wall.rect.width == 16
    assert wall.rect.height == 16

def test_level_generator():
    width, height = 10, 10
    maze = LevelGenerator(width, height)
    assert len(maze) == height
    assert len(maze[0]) == width
    assert maze[1][1] == 0  # Start position should be open

def test_game_stats():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 36)
    coin_count = 10
    message = "Test message"
    screen.fill((0, 0, 0))
    stats_text = font.render(f"Всего собрано монет: {coin_count}", True, (255, 255, 255))
    message_text = font.render(message, True, (255, 255, 255))
    screen.blit(stats_text, (400 - stats_text.get_width() // 2, 300 - stats_text.get_height() // 2 - 20))
    screen.blit(message_text, (400 - message_text.get_width() // 2, 300 - message_text.get_height() // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)
    assert stats_text is not None
    assert message_text is not None

def test_confirm_exit(monkeypatch):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 36)
    screen.fill((0, 0, 0))
    confirm_text = font.render("Вы уверены, что хотите выйти? (Y/N)", True, (255, 255, 255))
    screen.blit(confirm_text, (400 - confirm_text.get_width() // 2, 300 - confirm_text.get_height() // 2))
    pygame.display.flip()

    def mock_pygame_event_get():
        return [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_y})]

    monkeypatch.setattr(pygame.event, 'get', mock_pygame_event_get)
    with pytest.raises(SystemExit):
        ConfirmExit()

def test_show_start_screen(monkeypatch):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 36)
    screen.fill((0, 0, 0))
    start_text = font.render("Нажмите Enter для начала игры", True, (255, 255, 255))
    screen.blit(start_text, (400 - start_text.get_width() // 2, 300 - start_text.get_height() // 2))
    pygame.display.flip()

    def mock_pygame_event_get():
        return [pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN})]

    monkeypatch.setattr(pygame.event, 'get', mock_pygame_event_get)
    ShowStartScreen()
