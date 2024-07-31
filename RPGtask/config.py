# Используются для подсчёта стоимости прокачки. Формула - const * lvl ^ multiplier.
CONSTANT_GOLD = 0.1
MULTIPLIER_GOLD = 2

# Используется для подсчёта необходимого количества опыта для прокачки. Формула - const * lvl ^ multiplier.
CONSTANT_SKILL = 0.3
MULTIPLIER_SKILL = 2

MULTIPLIER_OBTAINING_GOLD = 2  # Коэффициент увеличения награды за задачи, у которых нет навыков.
DAILY_TASK_EXPERIENCE_MULTIPLIER = 1.1  # Коэффициент увеличения опыта для ежедневных задач.

DIVISOR_SUM_LEVELS = 3  # Число, на которое делится сумма всех уровней. Необходимо для подобия баланса между опытом и золотом.


PROBABILITY_ITEM_FALL_OUT = [0.99, 0.01]  # Вероятность выпадения предметов с пользовательских заданий.
PROBABILITY_ITEM_FALL_OUT_DAILY_TASK = [0.98, 0.02]  # Вероятность выпадения предметов с ежедневных заданий.

# Вероятность выпадения предмета определённого уровня. [первый, второй, третий].
PROBABILITY_DROP_ITEM_CERTAIN_LEVEL = [0.7, 0.25, 0.05]

RANK_EXPERIENCE_MULTIPLIER = 10
NUMBER_QUEST_STORE = 10
NUMBER_ITEM_STORE = 10
