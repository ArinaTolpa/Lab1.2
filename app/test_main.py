import pytest
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

if __name__ == '__main__':
    pytest.main()