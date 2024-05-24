import unittest
import pygame
from main import Character, Wall, Coin, LevelGenerator
import os
import random
import time

class TestCharacter(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.character = Character()
        self.walls = [Wall((50, 50)), Wall((100, 100))]
        print(f"Initial character position: {self.character.rect.topleft}")

    def tearDown(self):
        pygame.quit()

    def test_move_with_collision_right(self):
        self.character.rect.topleft = (34, 50)  # Initial position near the wall
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        self.character.move(20, 0, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving right to the wall: {new_position}")
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)

    def test_move_with_collision_left(self):
        self.character.rect.topleft = (116, 100)
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        self.character.move(-20, 0, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving left to the wall: {new_position}")
        self.assertEqual(self.character.rect.left, self.walls[1].rect.right)

    def test_move_with_collision_down(self):
        self.character.rect.topleft = (50, 34)  # Initial position near the wall
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        self.character.move(0, 20, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving down to the wall: {new_position}")
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

    def test_move_with_collision_up(self):
        self.character.rect.topleft = (100, 116)
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        self.character.move(0, -20, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving up to the wall: {new_position}")
        self.assertEqual(self.character.rect.top, self.walls[1].rect.bottom)

    def test_move_with_multiple_collisions(self):
        self.character.rect.topleft = (32, 32)  # Initial position
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        self.character.move(18, 18, self.walls)  # Move to first collision
        new_position = self.character.rect.topleft
        print(f"Position after moving to the corner: {new_position}")
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

class TestCoin(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def tearDown(self):
        pygame.quit()

    def test_coin_initialization(self):
        pos = (100, 150)
        coin = Coin(pos)
        self.assertEqual(coin.rect.topleft, pos)
        self.assertFalse(coin.negative)

    def test_negative_coin_initialization(self):
        pos = (200, 250)
        coin = Coin(pos, negative=True)
        self.assertEqual(coin.rect.topleft, pos)
        self.assertTrue(coin.negative)

    def test_coin_size(self):
        pos = (300, 350)
        coin = Coin(pos)
        self.assertEqual(coin.rect.width, 10)
        self.assertEqual(coin.rect.height, 10)

class TestLevelGenerator(unittest.TestCase):
    def test_level_generator(self):
        width, height = 5, 5
        maze = LevelGenerator(width, height)
        self.assertEqual(len(maze), height)
        self.assertEqual(len(maze[0]), width)
        self.assertEqual(maze[1][1], 0)  # Check start point is clear
        self.assertEqual(maze[height - 2][width - 2], 0)  # Check end point is clear
        self.assertIn(0, maze[1])  # There should be at least one path in the second row

class TestGameLoop(unittest.TestCase):
    def setUp(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen_width, self.screen_height = 740, 580
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont(None, 36)
        self.player = Character()
        self.walls = [Wall((50, 50)), Wall((100, 100))]
        self.coins = [Coin((150, 150)), Coin((200, 200), negative=True)]
        self.end_rect = pygame.Rect(300, 300, 16, 16)

    def tearDown(self):
        pygame.quit()

    def test_player_collect_coin(self):
        initial_coin_count = 0
        coin_count = initial_coin_count

        self.player.rect.topleft = (150, 150)
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                if coin.negative:
                    if coin_count > 0:
                        coin_count -= 1
                else:
                    coin_count += 1

        self.assertEqual(coin_count, initial_coin_count + 1)
        self.assertEqual(len(self.coins), 1)

    def test_player_reach_end(self):
        self.player.rect.topleft = (300, 300)
        self.assertTrue(self.player.rect.colliderect(self.end_rect))

    def test_timer_expired(self):
        start_time = time.time()
        max_time = 2  # 2 seconds for quick test
        time.sleep(3)
        elapsed_time = time.time() - start_time
        self.assertTrue(elapsed_time > max_time)

if __name__ == '__main__':
    unittest.main()
