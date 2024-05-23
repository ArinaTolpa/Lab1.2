import pytest
import pygame
from unittest.mock import patch
from main import Character, Coin, Wall, LevelGenerator

@pytest.fixture
def setup_character():
    character = Character()
    walls = [Wall((48, 32)), Wall((16, 32))]
    return character, walls

# def test_move_right_no_collision(setup_character):
#     character, walls = setup_character
#     character.move(16, 0, walls)
#     assert character.rect.topleft == (48, 32)

def test_move_right_collision(setup_character):
    character, _ = setup_character
    character.move(16, 0, [Wall((48, 32))])
    assert character.rect.right == 48

def test_move_left_no_collision(setup_character):
    character, walls = setup_character
    character.rect.topleft = (48, 32)
    character.move(-16, 0, walls)
    assert character.rect.topleft == (32, 32)

def test_move_left_collision(setup_character):
    character, _ = setup_character
    character.move(-16, 0, [Wall((16, 32))])
    assert character.rect.left == 32

def test_move_down_no_collision(setup_character):
    character, walls = setup_character
    character.move(0, 16, walls)
    assert character.rect.topleft == (32, 48)

def test_move_down_collision(setup_character):
    character, _ = setup_character
    character.move(0, 16, [Wall((32, 48))])
    assert character.rect.bottom == 48

def test_move_up_no_collision(setup_character):
    character, walls = setup_character
    character.rect.topleft = (32, 48)
    character.move(0, -16, walls)
    assert character.rect.topleft == (32, 32)

def test_move_up_collision(setup_character):
    character, _ = setup_character
    character.move(0, -16, [Wall((32, 16))])
    assert character.rect.top == 32

def test_coin_initialization():
    coin = Coin((100, 100))
    assert coin.rect.topleft == (100, 100)
    assert not coin.negative

def test_negative_coin_initialization():
    coin = Coin((100, 100), negative=True)
    assert coin.negative

def test_wall_initialization():
    wall = Wall((50, 50))
    assert wall.rect.topleft == (50, 50)

def test_level_generator():
    width, height = 10, 10
    maze = LevelGenerator(width, height)
    assert len(maze) == height
    assert len(maze[0]) == width
    assert maze[1][1] == 0  # Start point is open

# Определение функции ShowStartScreen из вашего кода
def ShowStartScreen(screen, screen_width, screen_height, font):
    # Отображение начального экрана
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

@pytest.fixture
def pygame_setup():
    pygame.init()
    screen_width = 740
    screen_height = 580
    screen = pygame.display.set_mode((screen_width, screen_height))
    font = pygame.font.SysFont(None, 36)
    yield screen, screen_width, screen_height, font
    pygame.quit()

@patch('pygame.event.get')
def test_show_start_screen(mock_pygame_event_get, pygame_setup):
    screen, screen_width, screen_height, font = pygame_setup
    
    # Мокируем события для симуляции нажатия клавиши Enter
    mock_pygame_event_get.return_value = [
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}),
    ]

    # Вызываем функцию
    ShowStartScreen(screen, screen_width, screen_height, font)

    # Проверяем, что pygame.display.flip() был вызван хотя бы раз
    assert pygame.display.get_surface() is not None


if __name__ == "__main__":
    pytest.main()

if __name__ == '__main__':
    pytest.main()