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
import main
from pygame.locals import *


class TestCharacter(unittest.TestCase):
    def setUp(self):
        # Инициализация Pygame
        pygame.init()
        # Создание объекта персонажа
        self.character = Character()
        # Создание списка объектов стен
        self.walls = [Wall((50, 50)), Wall((100, 100))]
        print(f"Initial character position: {self.character.rect.topleft}")

    def tearDown(self):
        # Завершение работы Pygame
        pygame.quit()

    def test_move_with_collision_right(self):
        # Установка начальной позиции персонажа
        self.character.rect.topleft = (34, 50)  
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        # Попытка передвижения персонажа вправо на 20 пикселей
        self.character.move(20, 0, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving right to the wall: {new_position}")
        # Проверка, что правый край персонажа совпадает с левым краем стены
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)

    def test_move_with_collision_left(self):
        # Установка начальной позиции персонажа
        self.character.rect.topleft = (116, 100)
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        # Попытка передвижения персонажа влево на 20 пикселей
        self.character.move(-20, 0, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving left to the wall: {new_position}")
        # Проверка, что левый край персонажа совпадает с правым краем стены
        self.assertEqual(self.character.rect.left, self.walls[1].rect.right)

    def test_move_with_collision_down(self):
        # Установка начальной позиции персонажа
        self.character.rect.topleft = (50, 34) 
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        # Попытка передвижения персонажа вниз на 20 пикселей
        self.character.move(0, 20, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving down to the wall: {new_position}")
        # Проверка, что нижний край персонажа совпадает с верхним краем стены
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

    def test_move_with_collision_up(self):
        # Установка начальной позиции персонажа
        self.character.rect.topleft = (100, 116)
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        # Попытка передвижения персонажа вверх на 20 пикселей
        self.character.move(0, -20, self.walls)
        new_position = self.character.rect.topleft
        print(f"Position after moving up to the wall: {new_position}")
        # Проверка, что верхний край персонажа совпадает с нижним краем стены
        self.assertEqual(self.character.rect.top, self.walls[1].rect.bottom)

    def test_move_with_multiple_collisions(self):
        # Установка начальной позиции персонажа
        self.character.rect.topleft = (32, 32)  
        initial_position = self.character.rect.topleft
        print(f"Initial position: {initial_position}")
        # Попытка передвижения персонажа на 18 пикселей вправо и 18 пикселей вниз
        self.character.move(18, 18, self.walls)  
        new_position = self.character.rect.topleft
        print(f"Position after moving to the corner: {new_position}")
        # Проверка, что правый край персонажа совпадает с левым краем стены и нижний край с верхним краем стены
        self.assertEqual(self.character.rect.right, self.walls[0].rect.left)
        self.assertEqual(self.character.rect.bottom, self.walls[0].rect.top)

class TestCoin(unittest.TestCase):
    def setUp(self):
        # Инициализация модуля pygame перед каждым тестом
        pygame.init()

    def tearDown(self):
        # Завершение работы модуля pygame после каждого теста
        pygame.quit()

    def test_coin_initialization(self):
        # Тестирование инициализации монеты с положением (100, 150)
        pos = (100, 150)
        coin = Coin(pos)
        # Проверка, что верхний левый угол прямоугольника монеты соответствует заданной позиции
        self.assertEqual(coin.rect.topleft, pos)
        # Проверка, что атрибут negative установлен в False (монета не является отрицательной)
        self.assertFalse(coin.negative)

    def test_negative_coin_initialization(self):
        # Тестирование инициализации отрицательной монеты с положением (200, 250)
        pos = (200, 250)
        coin = Coin(pos, negative=True)
        # Проверка, что верхний левый угол прямоугольника монеты соответствует заданной позиции
        self.assertEqual(coin.rect.topleft, pos)
        # Проверка, что атрибут negative установлен в True (монета является отрицательной)
        self.assertTrue(coin.negative)

    def test_coin_size(self):
        # Тестирование размера монеты с положением (300, 350)
        pos = (300, 350)
        coin = Coin(pos)
        # Проверка, что ширина прямоугольника монеты равна 10 пикселям
        self.assertEqual(coin.rect.width, 10)
        # Проверка, что высота прямоугольника монеты равна 10 пикселям
        self.assertEqual(coin.rect.height, 10)

class TestGameStats(unittest.TestCase):
    def setUp(self):
        # Инициализация модуля pygame и создание экрана и шрифта перед каждым тестом
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont(None, 36)
    
    def tearDown(self):
        # Завершение работы модуля pygame после каждого теста
        pygame.quit()

    def test_game_stats_display(self):
        # Тестирование отображения игрового статуса
        message = "Test Message"
        coin_count = 10
        GameStats(self.screen, self.font, message, coin_count, self.screen_width, self.screen_height)
        # Проверка, что поверхность дисплея инициализирована и не является None
        self.assertTrue(pygame.display.get_surface() is not None)
    
    def test_game_stats_content(self):
        # Тестирование содержимого игрового статуса
        message = "Test Message"
        coin_count = 10
        GameStats(self.screen, self.font, message, coin_count, self.screen_width, self.screen_height)
        # Проверка, что окно не закрывается из-за события pygame.QUIT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.fail("GameStats вызвал неожиданное закрытие окна")

class TestConfirmExit(unittest.TestCase):
    def setUp(self):
        # Инициализация модуля pygame и создание экрана и шрифта перед каждым тестом
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.font = pygame.font.SysFont(None, 36)

    def tearDown(self):
        # Завершение работы модуля pygame после каждого теста
        pygame.quit()

    def test_confirm_exit_yes(self):
        # Тестирование подтверждения выхода при нажатии 'Y'
        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': K_y}))
        # Ожидание для обработки события
        pygame.time.wait(100)
        # Проверка, что при нажатии 'Y' происходит выход из системы
        with self.assertRaises(SystemExit):
            ConfirmExit(self.screen, self.font, 640, 480)

    def test_confirm_exit_no(self):
        # Тестирование отклонения выхода при нажатии 'N'
        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': K_n}))
        # Ожидание для обработки события
        pygame.time.wait(100)
        # Проверка, что при нажатии 'N' не происходит выход из системы
        try:
            ConfirmExit(self.screen, self.font, 640, 480)
        except SystemExit:
            self.fail("ConfirmExit вызвал sys.exit() при нажатии 'N'")

    def test_confirm_exit_quit_event(self):
        # Тестирование подтверждения выхода при событии pygame.QUIT
        pygame.event.post(pygame.event.Event(QUIT))
        # Ожидание для обработки события
        pygame.time.wait(100)
        # Проверка, что при событии QUIT происходит выход из системы
        with self.assertRaises(SystemExit):
            ConfirmExit(self.screen, self.font, 640, 480)
            
class TestShowStartScreen(unittest.TestCase):
    def setUp(self):
        # Центрирование окна и инициализация модуля pygame перед каждым тестом
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen_width, self.screen_height = 740, 580
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))  
        self.font = pygame.font.SysFont(None, 36)
        
    def test_show_start_screen(self):
        # Тестирование отображения стартового экрана при нажатии клавиши ENTER
        pygame.event.post(pygame.event.Event(KEYDOWN, {'key': K_RETURN}))
        # Ожидание для обработки события
        pygame.time.wait(100)
        # Вызов функции ShowStartScreen для отображения стартового экрана
        ShowStartScreen(self.screen, self.font, self.screen_width, self.screen_height)
        # Проверка, что функция завершилась корректно
        self.assertTrue(True)
    
    def test_quit_game(self):
        # Тестирование выхода из игры при событии QUIT
        pygame.event.post(pygame.event.Event(QUIT))
        # Ожидание для обработки события
        pygame.time.wait(100)
        # Проверка, что при событии QUIT происходит выход из системы
        with self.assertRaises(SystemExit):
            ShowStartScreen(self.screen, self.font, self.screen_width, self.screen_height)
        
    def tearDown(self):
        # Завершение работы модуля pygame после каждого теста
        pygame.quit()

class TestCoinCollection(unittest.TestCase):
    def setUp(self):
        # Инициализация модуля pygame и создание экрана перед каждым тестом
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        # Создание экземпляра игрока
        self.player = Character()
        # Создание списка монет, одна положительная и одна отрицательная
        self.coins = [
            Coin((50, 50), negative=False),  # Положительная монета
            Coin((100, 100), negative=True)  # Отрицательная монета
        ]
        # Изначальное количество собранных монет
        self.coin_count = 0

    def test_collect_positive_coin(self):
        # Тестирование сбора положительной монеты
        self.player.rect.topleft = (50, 50)  # Перемещение игрока на позицию монеты
        self.player_collision()  # Проверка коллизии
        # Проверка, что количество собранных монет увеличилось на 1
        self.assertEqual(self.coin_count, 1)
        # Проверка, что одна монета была удалена из списка монет
        self.assertEqual(len(self.coins), 1)

    def test_collect_negative_coin(self):
        # Тестирование сбора положительной, а затем отрицательной монеты
        self.player.rect.topleft = (50, 50)  # Перемещение игрока на позицию положительной монеты
        self.player_collision()  # Проверка коллизии
        self.player.rect.topleft = (100, 100)  # Перемещение игрока на позицию отрицательной монеты
        self.player_collision()  # Проверка коллизии
        # Проверка, что количество собранных монет уменьшилось до 0
        self.assertEqual(self.coin_count, 0)
        # Проверка, что обе монеты были удалены из списка монет
        self.assertEqual(len(self.coins), 0)

    def test_collect_negative_coin_with_zero_count(self):
        # Тестирование сбора отрицательной монеты при нулевом количестве собранных монет
        self.player.rect.topleft = (100, 100)  # Перемещение игрока на позицию отрицательной монеты
        self.player_collision()  # Проверка коллизии
        # Проверка, что количество собранных монет осталось 0
        self.assertEqual(self.coin_count, 0)
        # Проверка, что отрицательная монета не была удалена из списка монет
        self.assertEqual(len(self.coins), 1)

    def player_collision(self):
        # Проверка коллизии игрока с монетами
        for coin in self.coins[:]:
            if self.player.rect.colliderect(coin.rect):  # Если игрок столкнулся с монетой
                self.coins.remove(coin)  # Удалить монету из списка монет
                if coin.negative:
                    if self.coin_count > 0:
                        self.coin_count -= 1  # Уменьшить количество монет, если монета отрицательная и количество монет больше 0
                else:
                    self.coin_count += 1  # Увеличить количество монет, если монета положительная

    def tearDown(self):
        # Завершение работы модуля pygame после каждого теста
        pygame.quit()

class TestGame(unittest.TestCase):
    def setUp(self):
        # Инициализация модуля pygame и создание экрана перед каждым тестом
        pygame.init()
        self.screen = pygame.display.set_mode((740, 580))
        self.font = pygame.font.SysFont(None, 36)
        
    def tearDown(self):
        # Завершение работы модуля pygame после каждого теста
        pygame.quit()
        
    def test_initialization(self):
        # Тестирование инициализации окна с заголовком
        pygame.display.set_caption("Достигните красного квадрата!")
        # Проверка, что заголовок окна установлен корректно
        self.assertEqual(pygame.display.get_caption()[0], "Достигните красного квадрата!")
                    
    def test_confirm_exit(self):
        # Тестирование подтверждения выхода из игры при нажатии клавиши ESC и подтверждении клавишей Y
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_ESCAPE}))
        pygame.time.wait(100)
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_y}))
        pygame.time.wait(100)

        with self.assertRaises(SystemExit):
            ConfirmExit(self.screen, self.font, 740, 580)
        
    def test_player_movement(self):
        # Тестирование перемещения игрока с учетом стены
        player = Character()
        walls = [Wall((48, 48))]  # Создание стены на позиции (48, 48)
        player.move(2, 0, walls)  # Перемещение игрока вправо на 2 пикселя
        self.assertEqual(player.rect.topleft, (34, 32))  # Проверка новой позиции игрока

    def test_collect_coin(self):
        # Тестирование сбора монеты игроком
        player = Character()
        player.rect.topleft = (32, 32)  # Перемещение игрока на позицию монеты
        coins = [Coin((32, 32))]
        self.assertTrue(player.rect.colliderect(coins[0].rect))  # Проверка коллизии игрока с монетой
        coins.remove(coins[0])  # Удаление монеты при сборе
        self.assertEqual(len(coins), 0)  # Проверка, что монет не осталось

    def test_game_win(self):
        # Тестирование завершения игры при сборе всех монет и достижении конечной точки
        player = Character()
        player.rect.topleft = (32, 32)  # Начальная позиция игрока
        coins = [Coin((32, 32)) for _ in range(20)]  # Создание 20 монет
        coin_count = 0
        for coin in coins[:]:
            player.rect.topleft = coin.rect.topleft  # Перемещение игрока на позицию монеты
            if player.rect.colliderect(coin.rect):
                coin_count += 1  # Увеличение счетчика собранных монет
                coins.remove(coin)  # Удаление монеты из списка

        self.assertEqual(coin_count, 20)  # Проверка, что все 20 монет были собраны
        
        end_rect = pygame.Rect(608, 448, 16, 16)  # Конечная точка
        player.rect.topleft = (608, 448)  # Перемещение игрока в конечную точку
        self.assertTrue(player.rect.colliderect(end_rect))  # Проверка коллизии игрока с конечной точкой

    def test_time_out(self):
        # Тестирование ограничения времени игры
        start_time = time.time()  # Начальное время
        max_time = 120  # Максимальное время игры в секундах
        elapsed_time = time.time() - start_time
        self.assertTrue(elapsed_time <= max_time)  # Проверка, что текущее время не превышает максимальное время

    def test_reach_end(self):
        # Тестирование достижения конечной точки
        player = Character()
        player.rect.topleft = (624, 464)  # Позиция игрока рядом с конечной точкой
        end_rect = pygame.Rect(624, 464, 16, 16)  # Конечная точка
        self.assertTrue(player.rect.colliderect(end_rect))  # Проверка коллизии игрока с конечной точкой

class TestInitializeGame(unittest.TestCase):
    def test_initialize_game(self):
        # Вызов функции initialize_game и получение ее результатов
        screen, clock, walls, player, coins, screen_width, screen_height, maze_offset_x, maze_offset_y = initialize_game()

        # Проверка ширины экрана
        self.assertEqual(screen_width, 740)
        # Проверка высоты экрана
        self.assertEqual(screen_height, 580)

        # Проверка смещения лабиринта по оси X
        self.assertEqual(maze_offset_x, 0)
        # Проверка смещения лабиринта по оси Y
        self.assertEqual(maze_offset_y, 50)
        
        # Проверка, что объект screen является экземпляром pygame.Surface
        self.assertIsInstance(screen, pygame.Surface)

        # Проверка, что объект clock является экземпляром pygame.time.Clock
        self.assertIsInstance(clock, pygame.time.Clock)

        # Проверка, что объект walls является списком
        self.assertIsInstance(walls, list)
        # Проверка, что начальное количество стен равно 0
        self.assertEqual(len(walls), 0)

        # Проверка, что объект player является экземпляром класса Character
        self.assertIsInstance(player, Character)

        # Проверка, что объект coins является списком
        self.assertIsInstance(coins, list)
        # Проверка, что начальное количество монет равно 0
        self.assertEqual(len(coins), 0)

class TestMazeGeneration(unittest.TestCase):
    def setUp(self):
        # Инициализация pygame и установка параметров теста
        pygame.init()
        self.maze_width = 40  # Ширина лабиринта в клетках
        self.maze_height = 30  # Высота лабиринта в клетках
        self.maze_offset_x = 0  # Смещение лабиринта по оси X
        self.maze_offset_y = 50  # Смещение лабиринта по оси Y
        self.player = Character()  # Создание экземпляра игрока

    def test_maze_generation(self):
        # Генерация лабиринта и связанных элементов
        maze, player_start, end_rect, walls, coins = generate_maze_and_elements(
            self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
        )

        # Проверка начальной позиции игрока
        self.assertEqual(player_start, (1, 1))  # Начальная позиция игрока должна быть (1, 1)

        # Проверка конечной позиции
        expected_end_position = pygame.Rect(
            (self.maze_width - 2) * 16 + self.maze_offset_x,  # Координата X конечной позиции
            (self.maze_height - 2) * 16 + self.maze_offset_y,  # Координата Y конечной позиции
            16, 16  # Размер прямоугольника конечной позиции
        )
        self.assertEqual(end_rect, expected_end_position)  # Конечная позиция должна соответствовать ожидаемой

        # Проверка, что все элементы в walls являются экземплярами класса Wall
        self.assertTrue(all(isinstance(wall, Wall) for wall in walls))  # Все стены должны быть экземплярами класса Wall

        # Проверка, что все элементы в coins являются экземплярами класса Coin
        self.assertTrue(all(isinstance(coin, Coin) for coin in coins))  # Все монеты должны быть экземплярами класса Coin

        # Проверка количества положительных и отрицательных монет
        positive_coins = [coin for coin in coins if not coin.negative]  # Список положительных монет
        negative_coins = [coin for coin in coins if coin.negative]  # Список отрицательных монет
        self.assertGreaterEqual(len(positive_coins), len(negative_coins))  # Количество положительных монет должно быть больше или равно количеству отрицательных

        # Убедитесь, что количество отрицательных монет меньше или равно половине количества положительных монет
        self.assertLessEqual(len(negative_coins), len(positive_coins) // 2)  # Количество отрицательных монет не должно превышать половины количества положительных

    def test_player_start_position(self):
        # Генерация элементов лабиринта и проверка начальной позиции игрока
        _, player_start, _, _, _ = generate_maze_and_elements(
            self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
        )
        self.assertEqual(player_start, (1, 1))  # Начальная позиция игрока должна быть (1, 1)

    def test_end_position(self):
        # Генерация элементов лабиринта и проверка конечной позиции
        _, _, end_rect, _, _ = generate_maze_and_elements(
            self.maze_width, self.maze_height, self.maze_offset_x, self.maze_offset_y, self.player
        )
        expected_end_position = pygame.Rect(
            (self.maze_width - 2) * 16 + self.maze_offset_x,  # Координата X конечной позиции
            (self.maze_height - 2) * 16 + self.maze_offset_y,  # Координата Y конечной позиции
            16, 16  # Размер прямоугольника конечной позиции
        )
        self.assertEqual(end_rect, expected_end_position)  # Конечная позиция должна соответствовать ожидаемой


class TestCheckCoinCollection(unittest.TestCase):
    def setUp(self):
        # Инициализация pygame для использования функционала игрового движка
        pygame.init()
        self.player = Character()  # Создание экземпляра игрока
        self.player.rect.topleft = (50, 50)  # Установка начальной позиции игрока

    def test_collect_positive_coin(self):
        # Тестирование сбора положительной монеты
        coin = Coin((50, 50), negative=False)  # Создание положительной монеты на позиции игрока
        coins = [coin]  # Список монет, содержащий только что созданную монету
        initial_coin_count = 0  # Начальное количество собранных монет

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)  # Проверка сбора монеты
        
        self.assertEqual(new_coin_count, 1)  # Проверка, что количество монет увеличилось на 1
        self.assertNotIn(coin, coins)  # Проверка, что монета была удалена из списка монет

    def test_collect_negative_coin(self):
        # Тестирование сбора отрицательной монеты
        coin = Coin((50, 50), negative=True)  # Создание отрицательной монеты на позиции игрока
        coins = [coin]  # Список монет, содержащий только что созданную монету
        initial_coin_count = 1  # Начальное количество собранных монет

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)  # Проверка сбора монеты
        
        self.assertEqual(new_coin_count, 0)  # Проверка, что количество монет уменьшилось на 1
        self.assertNotIn(coin, coins)  # Проверка, что монета была удалена из списка монет

    def test_collect_negative_coin_with_zero_count(self):
        # Тестирование сбора отрицательной монеты при начальном количестве монет равном 0
        coin = Coin((50, 50), negative=True)  # Создание отрицательной монеты на позиции игрока
        coins = [coin]  # Список монет, содержащий только что созданную монету
        initial_coin_count = 0  # Начальное количество собранных монет

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)  # Проверка сбора монеты
        
        self.assertEqual(new_coin_count, 0)  # Проверка, что количество монет осталось равным 0
        self.assertNotIn(coin, coins)  # Проверка, что монета была удалена из списка монет

    def test_no_coin_collision(self):
        # Тестирование отсутствия коллизии с монетой
        coin = Coin((100, 100), negative=False)  # Создание положительной монеты на позиции, отличной от позиции игрока
        coins = [coin]  # Список монет, содержащий только что созданную монету
        initial_coin_count = 0  # Начальное количество собранных монет

        new_coin_count = check_coin_collection(self.player, coins, initial_coin_count)  # Проверка сбора монеты
        
        self.assertEqual(new_coin_count, 0)  # Проверка, что количество монет не изменилось
        self.assertIn(coin, coins)  # Проверка, что монета осталась в списке монет



class TestCheckGameEnd(unittest.TestCase):
    def setUp(self):
        # Инициализация pygame для использования функционала игрового движка
        pygame.init()
        # Инициализация элементов игры, таких как экран, часы, стены, игрок, монеты и размеры экрана
        self.screen, self.clock, self.walls, self.player, self.coins, self.screen_width, self.screen_height, self.maze_offset_x, self.maze_offset_y = initialize_game()
        # Инициализация шрифта для отображения текста
        self.font = pygame.font.SysFont(None, 36)

    def tearDown(self):
        # Завершение работы pygame
        pygame.quit()

    def test_check_game_end_victory(self):
        # Тест на проверку завершения игры при достижении условия победы по количеству монет
        coin_count = 20  # Условие для победы - сбор 20 монет
        start_time = time.time() - 50  # Установим начальное время так, чтобы текущее время было меньше max_time
        max_time = 120  # Максимальное время для игры в секундах

        self.player.rect.topleft = (100, 100)  # Установка позиции игрока
        end_rect = pygame.Rect(200, 200, 16, 16)  # Установка позиции конца игры

        # Проверка, что игра завершается при выполнении условий победы
        with self.assertRaises(SystemExit):  # Ожидаем завершение игры (выход из программы)
            check_game_end(self.player, end_rect, coin_count, start_time, self.screen, self.font, self.screen_width, self.screen_height, max_time)

    def test_check_game_end_reach_end(self):
        # Тест на проверку завершения игры при достижении конца лабиринта
        coin_count = 15  # Количество монет меньше необходимого для победы
        start_time = time.time() - 50  # Установим начальное время так, чтобы текущее время было меньше max_time
        max_time = 120  # Максимальное время для игры в секундах

        self.player.rect.topleft = (200, 200)  # Установка позиции игрока на конец лабиринта
        end_rect = pygame.Rect(200, 200, 16, 16)  # Установка позиции конца игры

        # Проверка, что игра завершается при достижении конца лабиринта
        with self.assertRaises(SystemExit):  # Ожидаем завершение игры (выход из программы)
            check_game_end(self.player, end_rect, coin_count, start_time, self.screen, self.font, self.screen_width, self.screen_height, max_time)

    def test_check_game_end_time_out(self):
        # Тест на проверку завершения игры при превышении максимального времени
        coin_count = 10  # Количество монет меньше необходимого для победы
        start_time = time.time() - 130  # Установим начальное время так, чтобы текущее время было больше max_time
        max_time = 120  # Максимальное время для игры в секундах

        self.player.rect.topleft = (100, 100)  # Установка позиции игрока
        end_rect = pygame.Rect(200, 200, 16, 16)  # Установка позиции конца игры

        # Проверка, что игра завершается при превышении максимального времени
        with self.assertRaises(SystemExit):  # Ожидаем завершение игры (выход из программы)
            check_game_end(self.player, end_rect, coin_count, start_time, self.screen, self.font, self.screen_width, self.screen_height, max_time)


class TestMovePlayer(unittest.TestCase):
    def setUp(self):
        # Инициализация pygame для использования функционала игрового движка
        pygame.init()
        self.player = Character()  # Создание экземпляра игрока
        # Создание списка стен с фиксированными позициями
        self.walls = [Wall((50, 50)), Wall((100, 100))]
        # Инициализация состояния клавиш, все клавиши не нажаты
        self.key_state = {
            pygame.K_LEFT: False, 
            pygame.K_RIGHT: False, 
            pygame.K_UP: False, 
            pygame.K_DOWN: False
        }

    def test_move_left(self):
        # Тестирование движения игрока влево
        self.key_state[pygame.K_LEFT] = True  # Установка нажатия клавиши влево
        initial_position = self.player.rect.topleft  # Запоминание начальной позиции игрока
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок сдвинулся влево на 2 пикселя
        self.assertEqual(self.player.rect.topleft, (initial_position[0] - 2, initial_position[1]))
    
    def test_move_right(self):
        # Тестирование движения игрока вправо
        self.key_state[pygame.K_RIGHT] = True  # Установка нажатия клавиши вправо
        initial_position = self.player.rect.topleft  # Запоминание начальной позиции игрока
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок сдвинулся вправо на 2 пикселя
        self.assertEqual(self.player.rect.topleft, (initial_position[0] + 2, initial_position[1]))
    
    def test_move_up(self):
        # Тестирование движения игрока вверх
        self.key_state[pygame.K_UP] = True  # Установка нажатия клавиши вверх
        initial_position = self.player.rect.topleft  # Запоминание начальной позиции игрока
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок сдвинулся вверх на 2 пикселя
        self.assertEqual(self.player.rect.topleft, (initial_position[0], initial_position[1] - 2))
    
    def test_move_down(self):
        # Тестирование движения игрока вниз
        self.key_state[pygame.K_DOWN] = True  # Установка нажатия клавиши вниз
        initial_position = self.player.rect.topleft  # Запоминание начальной позиции игрока
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок сдвинулся вниз на 2 пикселя
        self.assertEqual(self.player.rect.topleft, (initial_position[0], initial_position[1] + 2))
    
    def test_collision_right(self):
        # Тестирование столкновения игрока со стеной при движении вправо
        self.player.rect.topleft = (34, 50)  # Установка позиции игрока рядом со стеной
        self.key_state[pygame.K_RIGHT] = True  # Установка нажатия клавиши вправо
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок остановился перед стеной
        self.assertEqual(self.player.rect.right, 50)  
    
    def test_collision_left(self):
        # Тестирование столкновения игрока со стеной при движении влево
        self.player.rect.topleft = (116, 100)  # Установка позиции игрока рядом со стеной
        self.key_state[pygame.K_LEFT] = True  # Установка нажатия клавиши влево
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок остановился перед стеной
        self.assertEqual(self.player.rect.left, 116)  

    def test_collision_up(self):
        # Тестирование столкновения игрока со стеной при движении вверх
        self.player.rect.topleft = (100, 116)  # Установка позиции игрока рядом со стеной
        self.key_state[pygame.K_UP] = True  # Установка нажатия клавиши вверх
        move_player(self.player, self.walls, self.key_state)  # Движение игрока
        # Проверка, что игрок остановился перед стеной
        self.assertEqual(self.player.rect.top, 116)  


# Глобальные переменные для экрана и шрифта
screen = None
font = None
screen_width = None
screen_height = None

class TestHandleEvents(unittest.TestCase):
    def setUp(self):
        global screen, font, screen_width, screen_height

        # Инициализация pygame для использования функционала игрового движка
        pygame.init()
        screen = pygame.display.set_mode((800, 600))  # Установка параметров экрана
        font = pygame.font.SysFont(None, 36)  # Инициализация шрифта
        screen_width = 800  # Ширина экрана
        screen_height = 600  # Высота экрана

        # Сохранение оригинальной функции ConfirmExit из модуля main
        self.original_confirm_exit = main.ConfirmExit

        # Мокирование функции ConfirmExit
        self.confirm_exit_mock = MagicMock()
        main.ConfirmExit = self.confirm_exit_mock

    def tearDown(self):
        # Завершение работы pygame
        pygame.quit()

        # Восстановление оригинальной функции ConfirmExit
        main.ConfirmExit = self.original_confirm_exit

    def test_handle_quit_event(self):
        # Тестирование обработки события выхода (QUIT)
        for event in [pygame.event.Event(pygame.QUIT)]:
            pygame.event.post(event)  # Постим событие QUIT в очередь событий pygame
        with self.assertRaises(SystemExit):  # Ожидаем завершение программы при обработке события QUIT
            handle_events()

    def test_no_event(self):
        # Тестирование обработки отсутствия событий
        handle_events()  # Вызов функции обработки событий без постинга событий
        # Здесь нет утверждений, так как проверяется отсутствие ошибок при отсутствии событий

    def test_handle_other_key_event(self):
        # Тестирование обработки других клавишных событий
        for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)]:
            pygame.event.post(event)  # Постим событие нажатия клавиши 'A' в очередь событий pygame
        handle_events()  # Вызов функции обработки событий
        self.confirm_exit_mock.assert_not_called()  # Проверка, что функция ConfirmExit не была вызвана


if __name__ == '__main__':
    unittest.main()