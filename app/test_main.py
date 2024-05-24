import unittest
import pygame
from main import Character, Wall, Coin

class TestCharacter(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.character = Character()
        self.walls = [Wall((50, 50)), Wall((100, 100))]
        print(f"Начальная позиция персонажа: {self.character.rect.topleft}")

    def tearDown(self):
        pygame.quit()

    def test_move_no_collision(self):
        начальная_позиция = self.character.rect.topleft
        print(f"Начальная позиция: {начальная_позиция}")
        self.character.move(10, 0, self.walls)
        self.character.move(0, 10, self.walls)
        новая_позиция = self.character.rect.topleft
        print(f"Позиция после перемещения вправо и вниз: {новая_позиция}")
        self.assertEqual(новая_позиция, (42, 42))  # Предполагается, что персонаж изначально стартует с позиции (32, 32)

    def test_move_with_collision_right(self):
        self.character.rect.topleft = (34, 50)  # Начальная позиция рядом со стеной
        начальная_позиция = self.character.rect.topleft
        print(f"Начальная позиция: {начальная_позиция}")
        self.character.move(20, 0, self.walls)
        новая_позиция = self.character.rect.topleft
        print(f"Позиция после перемещения вправо к стене: {новая_позиция}")
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)

    def test_move_with_collision_left(self):
        self.character.rect.topleft = (116, 100)
        начальная_позиция = self.character.rect.topleft
        print(f"Начальная позиция: {начальная_позиция}")
        self.character.move(-20, 0, self.walls)
        новая_позиция = self.character.rect.topleft
        print(f"Позиция после перемещения влево к стене: {новая_позиция}")
        self.assertEqual(self.character.rect.left, self.walls[1].rect.right)

    def test_move_with_collision_down(self):
        self.character.rect.topleft = (50, 34)  # Начальная позиция рядом со стеной
        начальная_позиция = self.character.rect.topleft
        print(f"Начальная позиция: {начальная_позиция}")
        self.character.move(0, 20, self.walls)
        новая_позиция = self.character.rect.topleft
        print(f"Позиция после перемещения вниз к стене: {новая_позиция}")
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

    def test_move_with_collision_up(self):
        self.character.rect.topleft = (100, 116)
        начальная_позиция = self.character.rect.topleft
        print(f"Начальная позиция: {начальная_позиция}")
        self.character.move(0, -20, self.walls)
        новая_позиция = self.character.rect.topleft
        print(f"Позиция после перемещения вверх к стене: {новая_позиция}")
        self.assertEqual(self.character.rect.top, self.walls[1].rect.bottom)

    def test_move_with_multiple_collisions(self):
        self.character.rect.topleft = (32, 32)  # Начальная позиция
        начальная_позиция = self.character.rect.topleft
        print(f"Начальная позиция: {начальная_позиция}")
        self.character.move(18, 18, self.walls)  # Движение к первому столкновению
        новая_позиция = self.character.rect.topleft
        print(f"Позиция после перемещения в угол: {новая_позиция}")
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)


class TestCoin(unittest.TestCase):
    def setUp(self):
        # Инициализация Pygame, так как Coin использует pygame.Rect
        pygame.init()

    def tearDown(self):
        # Завершение Pygame после каждого теста
        pygame.quit()

    def test_coin_initialization(self):
        # Тестирование корректной инициализации монеты
        pos = (100, 150)
        coin = Coin(pos)
        self.assertEqual(coin.rect.topleft, pos)
        self.assertFalse(coin.negative)

    def test_negative_coin_initialization(self):
        # Тестирование корректной инициализации отрицательной монеты
        pos = (200, 250)
        coin = Coin(pos, negative=True)
        self.assertEqual(coin.rect.topleft, pos)
        self.assertTrue(coin.negative)

    def test_coin_size(self):
        # Тестирование размеров монеты
        pos = (300, 350)
        coin = Coin(pos)
        self.assertEqual(coin.rect.width, 10)
        self.assertEqual(coin.rect.height, 10)

if __name__ == '__main__':
    unittest.main()
