import unittest
import pygame
from main import Character, Wall

class TestCharacter(unittest.TestCase):

    def setUp(self):
        pygame.init()
        self.character = Character()
        self.walls = [Wall((50, 50)), Wall((100, 100)), Wall((150, 150))]
        self.character.rect.topleft = (32, 32)
        print(f"Initial position: {self.character.rect.topleft}")

    def tearDown(self):
        pygame.quit()

    def test_initial_position(self):
        self.assertEqual(self.character.rect.topleft, (32, 32))

    def test_move_no_collision(self):
        self.character.move(10, 0, self.walls)
        print(f"Position after moving right: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.topleft, (42, 32))

        self.character.move(0, 10, self.walls)
        print(f"Position after moving down: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.topleft, (42, 42))

    def test_move_with_collision_x(self):
        # Движение вправо в стену
        self.character.rect.topleft = (34, 50)
        self.character.move(20, 0, self.walls)
        print(f"Position after moving right into wall: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)

        # Движение влево в стену
        self.character.rect.topleft = (116, 100)
        self.character.move(-20, 0, self.walls)
        print(f"Position after moving left into wall: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.left, self.walls[1].rect.right)

    def test_move_with_collision_y(self):
        # Движение вниз в стену
        self.character.rect.topleft = (50, 34)
        self.character.move(0, 20, self.walls)
        print(f"Position after moving down into wall: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

        # Движение вверх в стену
        self.character.rect.topleft = (100, 116)
        self.character.move(0, -20, self.walls)
        print(f"Position after moving up into wall: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.top, self.walls[1].rect.bottom)

    def test_move_with_multiple_collisions(self):
        # Движение в угол, образованный двумя стенами
        self.character.rect.topleft = (34, 34)
        self.character.move(16, 16, self.walls)
        print(f"Position after moving into corner: {self.character.rect.topleft}")
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

if __name__ == '__main__':
    unittest.main()
