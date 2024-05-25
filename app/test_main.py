import unittest
import pygame
from main import (
    Character, Wall, Coin, GameStats, ConfirmExit, ShowStartScreen, initialize_game,
    generate_maze_and_elements, check_coin_collection, check_game_end, handle_events, move_player, draw_scene

)
from pygame.locals import QUIT, KEYDOWN, K_y, K_n, K_RETURN
import os
from unittest.mock import patch, MagicMock
import time
import sys

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
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.font = pygame.font.SysFont(None, 36)

    def tearDown(self):
        pygame.quit()

    def test_confirm_exit_yes(self):
        # Simulate pressing 'Y' key
        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': K_y}))

        # Allow some time for event processing
        pygame.time.wait(100)

        # Check that ConfirmExit triggers a system exit
        with self.assertRaises(SystemExit):
            ConfirmExit(self.screen, self.font, 640, 480)

    def test_confirm_exit_no(self):
        # Simulate pressing 'N' key
        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': K_n}))

        # Allow some time for event processing
        pygame.time.wait(100)

        # Check that ConfirmExit does not exit the system
        try:
            ConfirmExit(self.screen, self.font, 640, 480)
        except SystemExit:
            self.fail("ConfirmExit triggered sys.exit() when 'N' was pressed")

    def test_confirm_exit_quit_event(self):
        # Simulate quit event
        pygame.event.post(pygame.event.Event(QUIT))

        # Allow some time for event processing
        pygame.time.wait(100)

        # Check that ConfirmExit triggers a system exit
        with self.assertRaises(SystemExit):
            ConfirmExit(self.screen, self.font, 640, 480)

class TestShowStartScreen(unittest.TestCase):
    def setUp(self):
        # Initialize pygame and create screen
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen_width, self.screen_height = 740, 580
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Actual screen
        self.font = pygame.font.SysFont(None, 36)
        
    def test_show_start_screen(self):
        # Simulate pressing ENTER key to start the game
        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': K_RETURN}))

        # Allow some time for event processing
        pygame.time.wait(100)
        
        ShowStartScreen(self.screen, self.font, self.screen_width, self.screen_height)
        
        # Verify that the function exited the while loop
        self.assertTrue(True)
    
    def test_quit_game(self):
        # Simulate quitting the game
        pygame.event.post(pygame.event.Event(QUIT))

        # Allow some time for event processing
        pygame.time.wait(100)
        
        with self.assertRaises(SystemExit):
            ShowStartScreen(self.screen, self.font, self.screen_width, self.screen_height)
        
    def tearDown(self):
        pygame.quit()

class TestCoinCollection(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.player = Character()
        self.coins = [
            Coin((50, 50), negative=False),  # Positive coin
            Coin((100, 100), negative=True)  # Negative coin
        ]
        self.coin_count = 0

    def test_collect_positive_coin(self):
        # Simulate player movement to the position of the positive coin
        self.player.rect.topleft = (50, 50)
        self.player_collision()
        self.assertEqual(self.coin_count, 1)
        self.assertEqual(len(self.coins), 1)

    def test_collect_negative_coin(self):
        # First collect a positive coin
        self.player.rect.topleft = (50, 50)
        self.player_collision()
        # Now collect the negative coin
        self.player.rect.topleft = (100, 100)
        self.player_collision()
        self.assertEqual(self.coin_count, 0)
        self.assertEqual(len(self.coins), 0)

    def test_collect_negative_coin_with_zero_count(self):
        # Simulate player movement to the position of the negative coin without collecting any positive coins first
        self.player.rect.topleft = (100, 100)
        self.player_collision()
        self.assertEqual(self.coin_count, 0)
        self.assertEqual(len(self.coins), 1)

    def player_collision(self):
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                if coin.negative:
                    if self.coin_count > 0:
                        self.coin_count -= 1
                else:
                    self.coin_count += 1

    def tearDown(self):
        pygame.quit()

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((740, 580))
        self.font = pygame.font.SysFont(None, 36)
        
    def tearDown(self):
        pygame.quit()
        
    def test_initialization(self):
        # Test the initialization of the game
        pygame.display.set_caption("Достигните красного квадрата!")
        self.assertEqual(pygame.display.get_caption()[0], "Достигните красного квадрата!")
                    
    def test_confirm_exit(self):
        # Simulate pressing 'ESC' key
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}))
        # Allow some time for the event to be processed
        pygame.time.wait(100)
        # Simulate pressing 'Y' key
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_y}))
        # Allow some time for the event to be processed
        pygame.time.wait(100)

        # Check that ConfirmExit triggers a system exit
        with self.assertRaises(SystemExit):
            ConfirmExit(self.screen, self.font, 740, 580)
        
    def test_player_movement(self):
        # Simulate player movement
        player = Character()
        walls = [Wall((48, 48))]  # Add a wall to collide with
        player.move(2, 0, walls)
        self.assertEqual(player.rect.topleft, (34, 32))  # Check if player moved correctly

    def test_collect_coin(self):
        player = Character()
        player.rect.topleft = (32, 32)
        coins = [Coin((32, 32))]
        self.assertTrue(player.rect.colliderect(coins[0].rect))  # Check collision
        coins.remove(coins[0])
        self.assertEqual(len(coins), 0)  # Coin should be collected
        
    def test_game_win(self):
        # Simulate collecting 20 coins to win the game
        player = Character()
        player.rect.topleft = (32, 32)
        coins = [Coin((32, 32)) for _ in range(20)]
        coin_count = 0
        for coin in coins[:]:
            player.rect.topleft = coin.rect.topleft
            if player.rect.colliderect(coin.rect):
                coin_count += 1
                coins.remove(coin)
        
        self.assertEqual(coin_count, 20)  # Player should have collected 20 coins
        
        # Check for game win condition
        end_rect = pygame.Rect(608, 448, 16, 16)
        player.rect.topleft = (608, 448)
        self.assertTrue(player.rect.colliderect(end_rect))  # Player reached the end

    def test_time_out(self):
        # Simulate the game running out of time
        start_time = time.time()
        max_time = 120  # seconds
        elapsed_time = time.time() - start_time
        self.assertTrue(elapsed_time <= max_time)  # Check if time out condition is met

    def test_reach_end(self):
        # Simulate the player reaching the end of the maze
        player = Character()
        player.rect.topleft = (624, 464)  # Position exactly at the end
        end_rect = pygame.Rect(624, 464, 16, 16)  # End position
        self.assertTrue(player.rect.colliderect(end_rect))  # Check if player reached the end


class TestInitializeGame(unittest.TestCase):

    def test_initialize_game(self):
        screen, clock, walls, player, coins, screen_width, screen_height, maze_offset_x, maze_offset_y = initialize_game()

        # Check if screen dimensions are correct
        self.assertEqual(screen_width, 740)
        self.assertEqual(screen_height, 580)

        # Check if maze offsets are correct
        self.assertEqual(maze_offset_x, 0)
        self.assertEqual(maze_offset_y, 50)

        # Check if screen is a pygame Surface
        self.assertIsInstance(screen, pygame.Surface)

        # Check if the clock is a pygame.time.Clock object
        self.assertIsInstance(clock, pygame.time.Clock)

        # Check if walls list is initialized and empty
        self.assertIsInstance(walls, list)
        self.assertEqual(len(walls), 0)

        # Check if player is an instance of Character
        self.assertIsInstance(player, Character)

        # Check if coins list is initialized and empty
        self.assertIsInstance(coins, list)
        self.assertEqual(len(coins), 0)


class TestMazeGeneration(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.maze_width = 40
        self.maze_height = 30
        self.maze_offset_x = 0
        self.maze_offset_y = 50
        self.player = Character()

    def test_maze_generation(self):
        maze, player_start, end_rect, walls, coins = generate_maze_and_elements(
            self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
        )

        # Проверка начальной позиции игрока
        self.assertEqual(player_start, (1, 1))

        # Проверка конечной позиции
        expected_end_position = pygame.Rect(
            (self.maze_width - 2) * 16 + self.maze_offset_x, 
            (self.maze_height - 2) * 16 + self.maze_offset_y, 
            16, 16
        )
        self.assertEqual(end_rect, expected_end_position)

        # Проверка наличия стен
        self.assertTrue(all(isinstance(wall, Wall) for wall in walls))

        # Проверка наличия монет
        self.assertTrue(all(isinstance(coin, Coin) for coin in coins))

        # Проверка количества монет
        positive_coins = [coin for coin in coins if not coin.negative]
        negative_coins = [coin for coin in coins if coin.negative]
        self.assertGreaterEqual(len(positive_coins), len(negative_coins))

        # Проверка, что количество отрицательных монет меньше положительных
        self.assertLessEqual(len(negative_coins), len(positive_coins) // 2)

    # def test_walls_positions(self):
    #     _, _, _, walls, _ = generate_maze_and_elements(
    #         self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
    #     )

    #     for wall in walls:
    #         x, y = wall.rect.topleft
    #         self.assertTrue(x % 16 == 0 and y % 16 == 0, f"Wall at ({x}, {y}) is not aligned to the grid")

    # def test_coins_positions(self):
    #     _, _, _, _, coins = generate_maze_and_elements(
    #         self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
    #     )

    #     for coin in coins:
    #         x, y = coin.rect.topleft
    #         self.assertTrue(x % 16 == 0 and y % 16 == 0, f"Coin at ({x}, {y}) is not aligned to the grid")

    def test_player_start_position(self):
        _, player_start, _, _, _ = generate_maze_and_elements(
            self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
        )
        self.assertEqual(player_start, (1, 1))

    def test_end_position(self):
        _, _, end_rect, _, _ = generate_maze_and_elements(
            self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
        )
        expected_end_position = pygame.Rect(
            (self.maze_width - 2) * 16 + self.maze_offset_x, 
            (self.maze_height - 2) * 16 + self.maze_offset_y, 
            16, 16
        )
        self.assertEqual(end_rect, expected_end_position)


class TestCheckCoinCollection(unittest.TestCase):
    
    def setUp(self):
        # Инициализация pygame
        pygame.init()
        self.player = Character()
        self.player.rect.topleft = (50, 50)
        
    def test_collect_positive_coin(self):
        coin = Coin((50, 50), negative=False)
        coins = [coin]
        initial_coin_count = 0

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)
        
        self.assertEqual(new_coin_count, 1)
        self.assertNotIn(coin, coins)

    def test_collect_negative_coin(self):
        coin = Coin((50, 50), negative=True)
        coins = [coin]
        initial_coin_count = 1

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)
        
        self.assertEqual(new_coin_count, 0)
        self.assertNotIn(coin, coins)
        
    def test_collect_negative_coin_with_zero_count(self):
        coin = Coin((50, 50), negative=True)
        coins = [coin]
        initial_coin_count = 0

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)
        
        self.assertEqual(new_coin_count, 0)
        self.assertNotIn(coin, coins)
        
    def test_no_coin_collision(self):
        coin = Coin((100, 100), negative=False)
        coins = [coin]
        initial_coin_count = 0

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)
        
        self.assertEqual(new_coin_count, 0)
        self.assertIn(coin, coins)


class TestCheckGameEnd(unittest.TestCase):

    def setUp(self):
        # Инициализация pygame
        pygame.init()
        self.screen, self.clock, self.walls, self.player, self.coins, self.screen_width, self.screen_height, self.maze_offset_x, self.maze_offset_y = initialize_game()
        self.font = pygame.font.SysFont(None, 36)

    def tearDown(self):
        pygame.quit()

    def test_check_game_end_victory(self):
        coin_count = 20  # Условие для победы
        start_time = time.time() - 50  # Убедимся, что время меньше max_time
        max_time = 120

        self.player.rect.topleft = (100, 100)
        end_rect = pygame.Rect(200, 200, 16, 16)

        with self.assertRaises(SystemExit):
            check_game_end(self.player, end_rect, coin_count, start_time, self.screen, self.font, self.screen_width, self.screen_height, max_time)

    def test_check_game_end_reach_end(self):
        coin_count = 15  # Условие для победы не выполнено
        start_time = time.time() - 50  # Убедимся, что время меньше max_time
        max_time = 120

        self.player.rect.topleft = (200, 200)  # Игрок достигает конца
        end_rect = pygame.Rect(200, 200, 16, 16)

        with self.assertRaises(SystemExit):
            check_game_end(self.player, end_rect, coin_count, start_time, self.screen, self.font, self.screen_width, self.screen_height, max_time)

    def test_check_game_end_time_out(self):
        coin_count = 10  # Условие для победы не выполнено
        start_time = time.time() - 130  # Время больше max_time
        max_time = 120

        self.player.rect.topleft = (100, 100)
        end_rect = pygame.Rect(200, 200, 16, 16)

        with self.assertRaises(SystemExit):
            check_game_end(self.player, end_rect, coin_count, start_time, self.screen, self.font, self.screen_width, self.screen_height, max_time)
############################################

class TestMovePlayer(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.player = Character()
        self.walls = [Wall((50, 50)), Wall((100, 100))]
        self.key_state = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        
    def test_move_left(self):
        self.key_state[pygame.K_LEFT] = True
        initial_position = self.player.rect.topleft
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.topleft, (initial_position[0] - 2, initial_position[1]))
    
    def test_move_right(self):
        self.key_state[pygame.K_RIGHT] = True
        initial_position = self.player.rect.topleft
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.topleft, (initial_position[0] + 2, initial_position[1]))
    
    def test_move_up(self):
        self.key_state[pygame.K_UP] = True
        initial_position = self.player.rect.topleft
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.topleft, (initial_position[0], initial_position[1] - 2))
    
    def test_move_down(self):
        self.key_state[pygame.K_DOWN] = True
        initial_position = self.player.rect.topleft
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.topleft, (initial_position[0], initial_position[1] + 2))
    
    def test_collision_right(self):
        self.player.rect.topleft = (34, 50)  # Place player near the wall
        self.key_state[pygame.K_RIGHT] = True
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.right, 50)  # The player should not pass the wall
    
    def test_collision_left(self):
        self.player.rect.topleft = (116, 100)  # Place player near the wall
        self.key_state[pygame.K_LEFT] = True
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.left, 116)  # The player should not pass the wall

    def test_collision_up(self):
        self.player.rect.topleft = (100, 116)  # Place player near the wall
        self.key_state[pygame.K_UP] = True
        move_player(self.player, self.walls, self.key_state)
        self.assertEqual(self.player.rect.top, 116)  # The player should not pass the wall
    
    # def test_collision_down(self):
    #     self.player.rect.topleft = (100, 34)  # Place player near the wall
    #     self.key_state[pygame.K_DOWN] = True
    #     move_player(self.player, self.walls, self.key_state)
    #     self.assertEqual(self.player.rect.bottom, 50)  # The player should not pass the wall

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



if __name__ == '__main__':
    unittest.main()