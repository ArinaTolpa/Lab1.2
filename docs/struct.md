# Структурные модели

```marmade
classDiagram
    class Game {
        - levelGenerator: LevelGenerator
        - character: Character
        - timer: Timer
        - gameStats: GameStats
        + initializeGame()
        + startGame()
        + update()
        + endGame()
    }
    class LevelGenerator {
        + generateLevel()
        + placeCoins()
    }
    class Character {
        - position: Point
        - collectedGoodCoins: int
        - collectedBadCoins: int
        + move(direction: Direction)
        + collectCoin(coin: Coin)
    }
    class Timer {
        - startTime: int
        - timeLimit: int
        + startTimer()
        + stopTimer()
        + checkTimeLimit()
    }
    class GameStats {
        - goodCoinsCollected: int
        - badCoinsCollected: int
        + updateCoinCount(coinType: CoinType)
        + displayStats()
    }
    class Point {
        - x: int
        - y: int
    }
    class Direction {
        - direction: int
    }
    class Coin {
        - type: CoinType
    }
    class CoinType {
        - value: int
    }

    Game --> LevelGenerator
    Game --> Character
    Game --> Timer
    Game --> GameStats
    Character --> Point
    Character --> Coin
    Character --> Direction
 
    Timer --> Point
    GameStats --> CoinType
```


1. **Game (Игра)**:
- Основной класс, управляющий игровым процессом.
- Содержит экземпляры классов `LevelGenerator`, `Character`, `Timer`, `GameStats`.
- Методы:
- `initializeGame()`: Инициализирует игру перед началом.
- `startGame()`: Запускает игру.
- `update()`: Обновляет состояние игры на каждом кадре.
- `endGame()`: Завершает игру.

2. **LevelGenerator (Генератор уровней)**:
- Генерирует игровой уровень, размещает монеты и секретные комнаты.
- Методы:
- `generateLevel()`: Генерирует новый игровой уровень.
- `placeCoins()`: Размещает монеты на уровне.

3. **Character (Персонаж)**:
- Представляет игрового персонажа.
- Содержит текущую позицию, количество собранных хороших и плохих монет.
- Методы:
- `move(direction: Direction)`: Перемещает персонажа в указанном направлении.
- `collectCoin(coin: Coin)`: Обрабатывает сбор монеты.

4. **Timer (Таймер)**:
- Отслеживает время игры и проверяет наличие ограничения времени.
- Методы:
- `startTimer()`: Запускает таймер.
- `stopTimer()`: Останавливает таймер.
- `checkTimeLimit()`: Проверяет, истекло ли ограничение времени.

5. **GameStats (Статистика игры)**:
- Отслеживает статистику игры, такую как количество собранных монет.
- Методы:
- `updateCoinCount(coinType: CoinType)`: Обновляет количество собранных монет.
- `displayStats()`: Отображает статистику игры.

6. **Point (Точка)**:
- Представляет координаты на игровом поле.

7. **Direction (Направление)**:
- Представляет направление движения персонажа.

8. **Coin (Монета)**:
- Представляет монету, которую может собрать персонаж.
- Содержит информацию о типе монеты.

9. **CoinType (Тип монеты)**:
- Представляет тип монеты, определяет её свойства.
