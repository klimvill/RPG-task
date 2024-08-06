from abc import ABC, abstractmethod
from typing import Any

from .player import RankType


class GoalAbstract(ABC):
	def __init__(self):
		self.completed = False

	@abstractmethod
	def save(self): ...

	@abstractmethod
	def load(self, data): ...

	@abstractmethod
	def complete(self): ...


class BossFight(GoalAbstract):
	def __init__(self, data: list[str]):
		super().__init__()
		self.name, self.hp = data

		self.damage: int = 0

	def save(self) -> int:
		""" Сохраняет статус выполнения задания. """
		return self.damage

	def load(self, data: int):
		""" Загружает статус выполнения задания. """
		self.damage = data
		self.complete()

	def add_damage(self, amount: int):
		""" Прибавляет урон, проверяет выполнение. """
		self.damage += amount
		self.complete()

	def complete(self):
		""" Если нанесенного урона больше, чем жизней у боса, то отмечает задание выполненным. """
		self.completed = self.damage >= self.hp

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Goal name={self.name!r} hp={self.hp} damage={self.damage} completed={self.completed}>"


class Goal(GoalAbstract):
	""" Объект задания. """

	def __init__(self, goal: list[str]):
		super().__init__()
		self.task, self.description = goal

	def save(self) -> bool:
		""" Сохраняет статус выполнения задания. """
		return self.completed

	def load(self, data: bool):
		""" Загружает статус выполнения задания. """
		self.completed = data

	def complete(self):
		""" Отмечает задание выполненным. """
		self.completed = True

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Goal name={self.task!r} description={self.description!r} completed={self.completed}>"


class Stage:
	""" Объект стадии квеста. """

	def __init__(self, data: dict):
		self.name: str = data['name']
		self.goals: list[list[str]] = data['goals']
		self.rewards: list[str] = data['rewards']

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Stage name={self.name!r} goals={len(self.goals)} rewards={self.rewards}>"


class Quest:
	""" Объект квеста. """

	def __init__(self, identifier, name, description, rank: RankType, stages: dict[int, dict[str, list]], reward):
		self.id = identifier
		self.name = name
		self.rank = rank
		self.description = description
		self.reward = reward

		self.stages: dict[int, Stage] = {i: Stage(j) for i, j in stages.items()}

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Quest id={self.id!r} name={self.name!r} stages={len(self.stages)}>"


class QuestState:
	"""
	Объект текущей стадий квеста.

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
		self.done_stages: list[int] = []
		self.done = False

		self.update(next(iter(quest.stages)))

	def update(self, stage: int):
		"""
		Обновляет состояние квеста до определённого этапа.

		Аргументы:
			stage (int): Идентификатор стадии, до которой надо обновить.
		"""
		self.stage_id = stage
		self.stage = self.quest.stages[stage]

		self.goals = []

		for goal in self.stage.goals:
			if goal[0] == 'boss':
				self.goals.append(BossFight(goal[1:]))
			else:
				self.goals.append(Goal(goal))

		# self.goals = [Goal(goal) for goal in self.stage.goals]

		self.rewards = self.stage.rewards

	def save(self) -> bool | tuple[list[int], int, list[bool]]:
		""" Сохраняет состояние квеста. """
		if self.done:
			return True
		return self.done_stages, self.stage_id, [g.save() for g in self.goals]

	def load(self, data: bool | tuple[list[str], int, list[bool]]):
		""" Загружает состояние квеста. """
		if isinstance(data, bool):
			self.done = True
			self.done_stages = list(self.quest.stages.keys())
		else:
			self.done_stages = data[0]
			self.update(data[1])

			for num, goal in enumerate(self.goals):
				goal.load(data[2][num])

	def complete(self, num: int):
		""" Завершает задание по его номеру. """
		self.goals[num].complete()
		self.check_all_goal_completed()

	def add_damage(self, amount: int):
		# Планируется, что босы всегда будут единственным заданием в стадии.
		self.goals[0].add_damage(amount)
		self.check_all_goal_completed()

	def check_boss_fight(self) -> bool:
		# Планируется, что босы всегда будут единственным заданием в стадии.
		return isinstance(self.goals[0], BossFight)

	def check_all_goal_completed(self):
		if all(goal.completed for goal in self.goals):
			self.done_stages.append(self.stage_id)
			self.process_rewards()

	def get_goal(self, num: int) -> Goal:
		""" Получение задания по номеру. """
		return self.goals[num]

	def process_rewards(self):
		""" Выдаёт награды за прохождение стадии. """
		rewards = self.rewards

		if "stage" == rewards[0]:
			self.update(int(rewards[1]))
		elif "end" == rewards[0]:
			self.done = True

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
		start_quest(identifier): Начинает квест по идентификатору.
		complete_goal(num): Выполняет задание из активного квеста по номеру.
		get_quest(identifier): Возвращает квест по идентификатору.
		is_done(): Проверяет выполнено ли задание.
		quest_been_launched(): Квест был запущен.
	"""

	def __init__(self):
		self.quests: list[Quest] = []
		self.active_quests: list[QuestState] = []

	def save(self) -> dict[str, bool | tuple[list[int], int, list[bool]]]:
		""" Возвращает идентификатор и состояние квестов. """
		return {q.quest.id: q.save() for q in self.active_quests}

	def load(self, data: dict[str, bool | list[list[str | int] | list[Any] | Any]]):
		""" Загружает идентификатор и состояние квестов. """
		self.active_quests = []

		for identifier, state in data.items():
			new_state = QuestState(self.get_quest(identifier))
			new_state.load(state)
			self.active_quests.append(new_state)

	def start_quest(self, identifier: str):
		""" Начинает квест по идентификатору. """
		self.active_quests.append(QuestState(self.get_quest(identifier)))

	def complete_goal(self, num: int):
		""" Выполняет задание из активного квеста по номеру. """
		if not self.quest_been_launched():
			raise ValueError(f"Goal {num - 1} not found")

		self.active_quests[0].complete(num - 1)

	def add_damage(self, damage: int):
		if self.quest_been_launched() and self.active_quests[0].check_boss_fight():
			self.active_quests[0].add_damage(damage)

	def get_quest(self, identifier: str) -> Quest:
		""" Возвращает квест по идентификатору. """
		for quest in self.quests:
			if quest.id == identifier:
				return quest
		raise ValueError(f"Quest {identifier} not found")

	def is_done(self) -> bool:
		""" Проверяет выполнено ли задание. """
		if not self.quest_been_launched():
			return False
		return self.active_quests[0].done

	def quest_been_launched(self) -> bool:
		""" Был ли квест запущен. """
		return bool(self.active_quests)

	def clear_active_quest(self):
		""" Удаляет квесты из активных. """
		self.active_quests = []

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<QuestManager quests={len(self.quests)}>"
