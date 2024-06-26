
# Поведенческие модели
**Диаграммы состояний**
```mermaid
stateDiagram
    [*] --> Начало_игры
    Начало_игры --> Ожидание_ввода: Нажатие_Enter
    Ожидание_ввода --> Игра_начата: Игра_началась
    Игра_начата --> Прохождение_уровня: Нажатие_PgUp/PgDn/Home/End
    Прохождение_уровня --> Завершение_игры: Персонаж_достиг_конца_уровня
    Завершение_игры --> Конец_игры: Игра_завершена
    Завершение_игры --> Прохождение_уровня: Нажатие_Enter
    Прохождение_уровня --> Конец_игры: Необходимое_количество_монет_собрано
    Конец_игры --> Начало_игры: Нажатие_Enter
    Конец_игры --> [*]: 
```

1. **Начало**: Начальное состояние.
2. **Ожидание ввода**: Нажатие_Enter.
3. **Игра начата**: Игра_началась.
4. **Прохождение уровня**: Нажатие_PgUp/PgDn/Home/End.
5. **Завершение игры**: Персонаж_достиг_конца_уровня.
6. **Конец игры**: Игра_завершена.
7. **Завершение игры**: Нажатие_Enter.
8. **Конец игры**: Необходимое_количество_монет_собрано.
9. **Конец игры**: Конец.

```mermaid
stateDiagram
    [*] --> Начало_игры
    Начало_игры --> Ожидание_ввода: Нажатие_Enter
    Ожидание_ввода --> Генерация_уровня: Нажатие_пробела
    Генерация_уровня --> Игра_начата: Уровень_сгенерирован
    Игра_начата --> Прохождение_уровня: Нажатие_PgUp/PgDn/Home/End
    Прохождение_уровня --> [*]
```

1. **Начало**: Начальное состояние.
2. **Ожидание ввода**: Нажатие_Enter.
3. **Генерация уровня**: Нажатие_пробела.
4. **Игра начата**: Уровень_сгенерирован.
5. **Прохождение уровня**: Конец.


```mermaid
stateDiagram
    [*] --> Начало_игры
    Начало_игры --> Ожидание_ввода: Нажатие_Enter
    Ожидание_ввода --> Игра_начата: Игра_началась
    Игра_начата --> Сбор_монеты: Персонаж_на_монете
    Сбор_монеты --> Сбор_хорошей_монеты: На_хорошей_монете
    Сбор_монеты --> [*]
    Сбор_монеты --> Сбор_плохой_монеты: На_плохой_монете
    Сбор_хорошей_монеты --> Сбор_монеты: Персонаж_покинул_монету
    Сбор_плохой_монеты --> Сбор_монеты: Персонаж_покинул_монету
```

1. **Начало**: Начальное состояние.
2. **Ожидание ввода**: Нажатие_Enter.
3. **Игра начата**: Игра_началась.
4. **Сбор монеты**: Персонаж_на_монете.
5. **Сбор хорошей монеты**: На_хорошей_монете.
6. **Сбор плохой монеты**: На_плохой_монете.
7. **Сбор монеты**: Персонаж_покинул_монету.
8. **Сбор монеты**: Конец.

**Диаграмма последовательности**
```mermaid
sequenceDiagram
    participant Пользователь
    participant Игровой мир

    Пользователь ->> Игровой мир: Прохождение лабиринта
    loop Управление персонажем
        Пользователь ->> Игровой мир: Нажатие управляющей клавиши
        Игровой мир ->> Игровой мир: Обновление положения
        Игровой мир ->> Пользователь: Пермещение
    end
```

Описание: Пользователь проходит лабиринт. ПАользователь нажимает клавишу управления. Игровой мир обновлят положение персонажа. Пользователь перемещается.
