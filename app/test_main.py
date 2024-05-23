import pytest
import random
from main import Character, Coin, Wall, LevelGenerator

# Test for Character class
def test_character_move():
    walls = [Wall((0, 0)), Wall((32, 0))]
    char = Character()
    char.move(16, 0, walls)
    assert char.rect.topleft == (48, 32)
    char.move(-16, 0, walls)
    assert char.rect.topleft == (32, 32)
    char.move(0, 16, walls)
    assert char.rect.topleft == (32, 48)
    char.move(0, -16, walls)
    assert char.rect.topleft == (32, 32)

def test_character_collision():
    walls = [Wall((48, 32))]
    char = Character()
    char.move(16, 0, walls)
    assert char.rect.right == 48  # should collide and stop at the wall

# Test for Coin class
def test_coin_initialization():
    coin = Coin((10, 10), negative=True)
    assert coin.rect.topleft == (10, 10)
    assert coin.negative is True

# Test for Wall class
def test_wall_initialization():
    wall = Wall((10, 10))
    assert wall.rect.topleft == (10, 10)

# Test for LevelGenerator function
def test_level_generator():
    width, height = 5, 5
    maze = LevelGenerator(width, height)
    assert len(maze) == height
    assert len(maze[0]) == width
    # Check that start and end points are passable
    assert maze[1][1] == 0
    assert maze[height - 2][width - 2] == 0

# Mock random to ensure reproducibility
@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)

if __name__ == "__main__":
    pytest.main()
