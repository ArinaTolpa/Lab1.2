[![Python application](https://github.com/ArinaTolpa/Lab1.2/actions/workflows/connect.yml/badge.svg)](https://github.com/ArinaTolpa/Lab1.2/actions/workflows/connect.yml)
[![Coverage Status](https://coveralls.io/repos/github/ArinaTolpa/Lab1.2/badge.svg?branch=master)](https://coveralls.io/github/ArinaTolpa/Lab1.2?branch=master)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ArinaTolpa_Lab1.2&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ArinaTolpa_Lab1.2)


Описание приложения
	•	Игра “Человечек в лабиринте”
	•	Игра содержит несколько лабиринтов, которые определяются рандомно 
	•	Игрок проходя лабиринт собирает “хорошие” монетки, которые помогут ему одержать победу, не доходя до конца лабиринта
	•	Существуют “плохие” монетки, которые собирать нельзя, потому что они уменьшают количество собранных “хороших” монеток
	•	Игрок может закончить игру добровольно или при неудачном результате

 

	
Сценарий работы: 
Пользователь нажимает: приложение отображает 
	1.	Enter: Начало игры 
	2. PgUp: Передвижение на шаг вверх 
	3. PgDn: Передвижение на шаг вниз 
	4. Home: Передвижение влево
	5. End: Передвижение вправо 
	6. Esc: Добровольный выход из игры 

1. Начало игры:
- пользователь нажимает Enter, игра начинается
2. Управление персонажем и начало игры:
- Пользователь может использовать клавиши PgUp, PgDn, Home, End для передвижения персонажа по лабиринту.

3. Выход из игры и защита от случайного выхода:
- Если пользователь нажимает клавишу Esc, игра показывает диалоговое окно с предложением подтвердить выход из игры.
- Если пользователь подтверждает выход, игра завершается.
- Эта функциональность объединяет защиту от случайного выхода из игры и возможность добровольного выхода.

4. Перемещение по лабиринту и обработка событий:
- Пользователь использует клавиши управления для передвижения персонажа.
- Приложение отслеживает позицию персонажа и взаимодействует с игровым миром в зависимости от его действий.
- Эта функциональность объединяет управление перемещением персонажа и обработку игровых событий.

Алгоритмы: 
	1.	Проход лабиринта (передвижение игрока)
	2.	Сбор монеток и “хороших” (которые можно собирать) и “плохих” (которые уменьшают количество собранных монеток) 
(при сборе определенного количества монеток игрок автоматически побеждает) 
	3.	Выбор лабиринта 
Д

* [Описание функциональных моделей](docs/functions.md)
* [Описание структурных моделей](docs/struct.md) 
* [Oписание поведенческих моделей](docs/behavior.md)
