from enum import IntEnum
from typing import Any, NoReturn


class QuestLevel(IntEnum):
	""" Уровень квеста. """
	EASY = 1
	MEDIUM = 2
	HARD = 3
	LEGENDARY = 4

	@staticmethod
	def description(level):
		""" Описание типа квеста """
		return LEVEL_DESCRIPTIONS[level]


LEVEL_DESCRIPTIONS = {
	QuestLevel.EASY: 'Простой',  # ★☆☆☆
	QuestLevel.MEDIUM: 'Средний',  # ★★☆☆
	QuestLevel.HARD: 'Сложный',  # ★★★☆
	QuestLevel.LEGENDARY: 'Легендарный',  # ★★★★
}


class Goal:
	"""
	Объект задания.

	Параметры:
		name (str): Собственно текст самого задания.
		description (str): Описание задания.

	Атрибуты:
		completed (bool): True задание выполнено, иначе False. По умолчанию False.

	Методы:
		save() -> bool: Сохраняет статус выполнения задания.
		load(data: bool): Загружает статус выполнения задания.
		complete(): Отмечает задание выполненным.
	"""
	def __init__(self, goal: list[str]):
		self.text = goal[0]
		self.description = goal[1]

		self.completed = False

	def save(self) -> bool:
		""" Сохраняет статус выполнения задания. """
		return self.completed

	def load(self, data: bool) -> NoReturn:
		""" Загружает статус выполнения задания. """
		self.completed = data

	def complete(self) -> NoReturn:
		""" Отмечает задание выполненным. """
		self.completed = True

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f'<Goal name={self.text!r} completed={self.completed}>'


class Stage:
	"""
	Объект стадии квеста.

	Параметры:
		name (str): Название стадии.
		goals (list[list[str]]): Задания.
		rewards (list[str]): Награды за выполнение стадии.
	"""
	def __init__(self, data: dict[str, Any]):
		self.name: str = data['name']
		self.goals: list[list[str]] = data['goals']
		self.rewards: list[str] = data['rewards']

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f'<Stage name={self.name!r} goals={len(self.goals)}>'


class Quest:
	"""
	Объект квеста.

	Параметры:
		id (str): Уникальный идентификатор.
		name (str): Название квеста.
		description (str): Описание.
		level (QuestLevel): Сложность квеста.
		stages (dict[str | int, Stage]): Стадии квеста.
	"""
	def __init__(self, identifier: str, text: str, description: str, level: QuestLevel,
				 stages: dict[str | int, dict[str, Any]]):
		self.id = identifier
		self.text = text
		self.level = level
		self.description = description
		self.stages: dict[str | int, Stage] = {i: Stage(j) for i, j in stages.items()}

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f'<Quest id={self.id!r} name={self.text!r} stages={len(self.stages)}>'


class QuestState:
	"""
	Объект стадий квеста.

	Параметры:
		quest (Quest): Объект квеста.

	Аргументы:
		done_stages (list[str | int]): Список завершённых стадий. По умолчанию пустой список.
		done (bool): True если квест выполнен, иначе False. По умолчанию False.

	Методы:
		update(stage): Обновляет состояние квеста до определённого этапа.
		save(): Сохраняет состояние квеста.
		load(): Загружает состояние квеста.
		complete(num): Завершает задание по его номеру.
		get_goal(num): Получение задания по номеру.
		process_rewards(): Выдаёт награды за прохождение стадии.
	"""
	def __init__(self, quest: Quest):
		self.quest = quest
		self.done_stages: list[str | int] = []
		self.done = False

		self.update(next(iter(quest.stages)))

	def update(self, stage: str | int) -> NoReturn:
		"""
		Обновляет состояние квеста до определённого этапа.

		Аргументы:
			stage (str, int): Идентификатор стадии, до которой надо обновить.
		"""
		self.stage = self.quest.stages[stage]
		self.stage_id = stage
		self.goals = [Goal(goal) for goal in self.stage.goals]
		self.rewards = self.stage.rewards

	def save(self) -> bool | list[list[str | int] | list[Any] | Any]:
		"""
		Сохраняет состояние квеста.

		Возвращается:
			Union[bool, list]: Сохраняемая информация.
		"""
		if self.done:
			return True
		return [self.done_stages, self.stage_id, [g.save() for g in self.goals]]

	def load(self, data: bool | list[list[str | int] | list[Any] | Any]):
		"""
		Загружает состояние квеста.

		Аргументы:
			data (Union[bool, list]): Состояние квеста.
		"""
		if data is True:
			self.done = True
			self.done_stages = list(self.quest.stages.keys())
			print(list(self.quest.stages.keys()))
		else:
			self.done_stages = data[0]
			self.update(data[1])
			for i, goal in enumerate(self.goals):
				goal.load(data[2][i])

	def complete(self, num: int):
		"""
		Завершает задание по его номеру.

		Аргументы:
			num (int): Номер выполненного задания.
		"""
		goal = self.goals[num]
		if not goal.completed:
			goal.complete()

		if all(goal.completed for goal in self.goals):
			self.done_stages.append(self.stage_id)
			self.process_rewards()

	def get_goal(self, num: int) -> Goal:
		""" Получение задания по номеру. """
		goal = self.goals[num]
		return goal

	def process_rewards(self) -> dict | NoReturn:
		""" Выдаёт награды за прохождение стадии. """
		rewards = self.rewards

		if rewards[0] == 'stage':
			new_stage = int(rewards[1]) if rewards[1].isdigit() else rewards[1]
			self.update(new_stage)
		elif rewards[0] == 'end':
			self.done = True
			return rewards[1]


	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		count = len([goal for goal in self.goals if goal.completed])
		return f"<QuestState stage={self.stage} progress={count}/{len(self.goals)}>"


class QuestManager:
	"""
	Менеджер всех квестов.

	Аргументы:
		quests (list[Quest]): Список всех квестов. По умолчанию пустой список.
		active_quests (list[QuestState]): Список активных квестов. По умолчанию пустой список.

	Методы:
		save(): Сохраняет идентификатор и состояние квестов.
		load(data): Загружает идентификатор и состояние квестов.
		get_quest(identifier): Возвращает квест по идентификатору.
		start_quest(identifier): Начинает квест по идентификатору.
		complete_goal(num): Выполняет задание из активного квеста по номеру.
		is_done(): Проверяет выполнено ли задание.
	"""
	def __init__(self):
		self.quests: list[Quest] = []
		self.active_quests: list[QuestState] = []

	def save(self) -> dict[str, bool | list[list[str | int] | list[Any] | Any]]:
		""" Возвращает идентификатор и состояние квестов. """
		return {q.quest.id: q.save() for q in self.active_quests}

	def load(self, data: dict[str, bool | list[list[str | int] | list[Any] | Any]]):
		""" Загружает идентификатор и состояние квестов. """
		self.active_quests = []

		for identifier, state in data.items():
			quest = self.get_quest(identifier)
			if quest:
				new_state = QuestState(quest)
				new_state.load(state)
				self.active_quests.append(new_state)
			else:
				raise ValueError(f"Quest {identifier} not found")

	def get_quest(self, identifier: str | Quest) -> Quest:
		"""
		Возвращает квест по идентификатору.

		Аргументы:
			identifier (str | Quest): Идентификатор квеста

		Возвращается:
			Quest: Собственно полученный квест.
		"""
		if isinstance(identifier, Quest):
			return identifier
		for quest in self.quests:
			if quest.id == identifier:
				return quest
		raise ValueError(f"Quest {identifier} not found")

	def start_quest(self, identifier: str) -> NoReturn:
		"""
		Начинает квест по идентификатору.

		Аргументы:
			identifier (str | Quest): Идентификатор квеста
		"""
		quest = self.get_quest(identifier)
		if quest:
			self.active_quests.append(QuestState(quest))
		else:
			raise ValueError(f"Quest {identifier} not found")

	def complete_goal(self, num: int) -> NoReturn:
		"""
		Выполняет задание из активного квеста по номеру.

		Аргументы:
			num (int): Номер выполненного задания.
		"""
		if not len(self.active_quests):
			raise ValueError(f"Goal {num} not found")

		quest = self.active_quests[0]  # Пока может быть только один активный квест
		if not quest.done:
			quest.complete(num)

	def is_done(self, identifier: str) -> bool:
		"""
		Проверяет выполнено ли задание.

		Возвращается:
			bool: True если задание выполнено, иначе False.
		"""
		quest = self.get_quest(identifier)
		if quest:
			return quest.id in [q.quest.id for q in self.active_quests if q.done]
		raise ValueError(f"Quest {identifier} not found")

	def quest_been_launched(self, identifier: str) -> bool:
		return bool(self.active_quests)

	def clear_active_quest(self):
		self.active_quests = []

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<QuestManager q={len(self.quests)}>"
