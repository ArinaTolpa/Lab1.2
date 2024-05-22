# test_game.py
import pytest
import pygame
from main import Character, Wall

# Тестирование перемещения игрока
def test_character_movement():
    walls = [Wall((50, 50), [])]  # Создание стены
    player = Character()  # Создание игрока
    
    # Начальная позиция
    assert player.rect.topleft == (32, 32)
    
    # Движение вправо, без столкновений
    player.move(10, 0, walls)
    assert player.rect.topleft == (42, 32)
    
    # Движение вправо в стену
    player.move(10, 0, walls)
    assert player.rect.right == 50
    
    # Движение вниз, без столкновений
    player.move(0, 10, walls)
    assert player.rect.bottom == 58
    
    # Движение вниз в стену
    player.move(0, 10, walls)
    assert player.rect.bottom == 50
    
    # Движение влево, без столкновений
    player.move(-10, 0, walls)
    assert player.rect.left == 32
    
    # Движение влево в стену
    player.move(-10, 0, walls)
    assert player.rect.left == 50
    
    # Движение вверх, без столкновений
    player.move(0, -10, walls)
    assert player.rect.top == 42
    
    # Движение вверх в стену
    player.move(0, -10, walls)
    assert player.rect.top == 50

# Тестирование генерации лабиринта
def test_level_generator():
    width, height = 21, 21  # Должны быть нечетные числа
    maze = LevelGenerator(width, height)
    
    assert len(maze) == height  # Проверка высоты лабиринта
    assert len(maze[0]) == width  # Проверка ширины лабиринта
    
    # Проверка, что начальная и конечная позиции открыты
    assert maze[1][1] == 0
    assert maze[height-2][width-2] == 0
    
    # Проверка, что все стены (1) не имеют смежных открытых пространств (0)
    for y in range(1, height-1, 2):
        for x in range(1, width-1, 2):
            assert maze[y][x] == 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                assert 0 <= x+dx < width
                assert 0 <= y+dy < height
                if maze[y+dy][x+dx] == 1:
                    continue
                assert maze[y+dy][x+dx] == 0

# Инициализация pygame перед запуском тестов
if __name__ == "__main__":
    pygame.init()
    pytest.main()
