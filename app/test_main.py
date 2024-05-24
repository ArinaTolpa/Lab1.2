import unittest
import pygame
from main import Character, Wall, Coin, GameStats, ConfirmExit, ShowStartScreen
from pygame.locals import QUIT, KEYDOWN, K_y, K_n
import os
from unittest.mock import MagicMock

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

class TestGameStats(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont(None, 36)
    
    def tearDown(self):
        pygame.quit()

    def test_game_stats_display(self):
        message = "Test Message"
        coin_count = 10
        GameStats(self.screen, self.font, message, coin_count, self.screen_width, self.screen_height)
        self.assertTrue(pygame.display.get_surface() is not None)
    
    def test_game_stats_content(self):
        message = "Test Message"
        coin_count = 10
        GameStats(self.screen, self.font, message, coin_count, self.screen_width, self.screen_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fail("GameStats caused the window to close unexpectedly")


class TestConfirmExit(unittest.TestCase):
    def test_confirm_exit_yes(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        font = pygame.font.SysFont(None, 36)

        # Добавление события в очередь
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_y))

        # Проверка, что вызов ConfirmExit вызывает выход из системы
        with self.assertRaises(SystemExit):
            ConfirmExit(screen, font, 640, 480)

    def test_confirm_exit_no(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        font = pygame.font.SysFont(None, 36)

        # Добавление события в очередь
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_n))

        # Проверка, что ConfirmExit не завершает работу
        try:
            ConfirmExit(screen, font, 640, 480)
        except SystemExit:
            self.fail("ConfirmExit вызвал sys.exit() при нажатии 'N'")

    def test_confirm_exit_quit_event(self):
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        font = pygame.font.SysFont(None, 36)

        # Добавление события в очередь
        pygame.event.post(pygame.event.Event(QUIT))

        # Проверка, что вызов ConfirmExit вызывает выход из системы
        with self.assertRaises(SystemExit):
            ConfirmExit(screen, font, 640, 480)

###########################################
class TestShowStartScreen(unittest.TestCase):
    
    def setUp(self):
        # Инициализация pygame и создание экрана
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen_width, self.screen_height = 740, 580
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Настоящий экран
        self.font = pygame.font.SysFont(None, 36)
        
    def test_show_start_screen(self):
        # Симуляция нажатия клавиши ENTER для начала игры
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}))
        
        ShowStartScreen(self.screen, self.font, self.screen_width, self.screen_height)
        
        # Проверка, что функция вышла из цикла while
        self.assertTrue(True)
    
    def test_quit_game(self):
        # Симуляция выхода из игры
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        with self.assertRaises(SystemExit):
            ShowStartScreen(self.screen, self.font, self.screen_width, self.screen_height)
        
    def tearDown(self):
        pygame.quit()

class CoinCollectionTest(unittest.TestCase):
    def setUp(self):
        # Initialize Pygame modules
        pygame.init()
        
        # Create a screen (not displayed in tests)
        self.screen = pygame.display.set_mode((100, 100))
        
        # Create a player
        self.player = Character()
        self.player.rect.topleft = (50, 50)
        
        # Create some coins
        self.positive_coin = Coin((60, 50), negative=False)
        self.negative_coin = Coin((70, 50), negative=True)
        
        # Initialize coin count
        self.coin_count = 0

    def test_positive_coin_collection(self):
        # Mock the player's rectangle to collide with the positive coin
        self.player.rect = pygame.Rect(60, 50, 16, 16)
        self.coins = [self.positive_coin]
        
        # Run the coin collection logic
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                if coin.negative:
                    if self.coin_count > 0:
                        self.coin_count -= 1
                else:
                    self.coin_count += 1
        
        # Check if the coin count is increased
        self.assertEqual(self.coin_count, 1, "Positive coin collection failed")

    def test_negative_coin_collection(self):
        # Set the coin count to 1
        self.coin_count = 1
        
        # Mock the player's rectangle to collide with the negative coin
        self.player.rect = pygame.Rect(70, 50, 16, 16)
        self.coins = [self.negative_coin]
        
        # Run the coin collection logic
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                if coin.negative:
                    if self.coin_count > 0:
                        self.coin_count -= 1
                else:
                    self.coin_count += 1
        
        # Check if the coin count is decreased
        self.assertEqual(self.coin_count, 0, "Negative coin collection failed")

    def tearDown(self):
        pygame.quit()



if __name__ == '__main__':
    unittest.main()
