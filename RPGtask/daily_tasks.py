from .player import SkillType


class DailyTask:
	"""
	Объект ежедневного задания.

	Параметры:
		id (str): Уникальный идентификатор задания.
		text (str): Текст задания.
		skills (list[SkillType]): Список навыков.
		done (bool): Выполнено ли задание. По умолчанию False.

	Методы:
		save() -> list[str | bool]: Возвращает идентификатор и состояние задания.
		complete(): Отмечает задание выполненным.
		get_skills_descriptions() -> list[str]: Возвращает текстовое представление навыков задачи.
	"""

	def __init__(self, identifier: str, text: str, skills: list[SkillType]):
		self.id = identifier
		self.text = text
		self.skills = skills
		self.done = False

	def save(self) -> list[str | bool]:
		""" Возвращает идентификатор и состояние задания. """
		return [self.id, self.done]

	def complete(self):
		""" Отмечает задание выполненным. """
		self.done = True

	def not_completed(self):
		self.done = False

	def get_skills_descriptions(self) -> list[str]:
		""" Возвращает текстовое представление навыков задачи. """
		return list(map(lambda skill: SkillType.description(skill), self.skills))


class DailyTaskManager:
	"""
	Менеджер всех дневных заданий.

	Атрибуты:
		daily_tasks (dict[str, DailyTask]): Словарь всех дневных заданий. По умолчанию пустой словарь.
		active_daily_tasks (list[DailyTask]): Список всех активных заданий. По умолчанию пустой список.
		done (bool): Выполнены ли задания. По умолчанию False.
		date (str): Дата, когда задание было получено. По умолчанию пустая строка.

	Методы:
		save(): Возвращает данные для сохранения дневных заданий.
		load(data): Загрузка данных из сохранения.

		get_daily_tasks(num): Получение ежедневного задания по его номеру.
		complete(num): Отмечает выполненным задание по номеру и проверяет на полное выполнение ежедневных заданий.
		update(): Если задание неактуально, то обновляет его.
		size(): Возвращает количество заданий.
	"""

	def __init__(self):
		self.daily_tasks: dict[str, DailyTask] = {}
		self.active_daily_tasks: list[DailyTask] = []

		self.done: bool = False
		self.date: str = ''

	def save(self) -> dict[str, str | bool | list[list[str, bool]]]:
		""" Возвращает данные для сохранения дневных заданий. """
		save_active_tasks = [task.save() for task in self.active_daily_tasks]

		return {'tasks': save_active_tasks, 'done': self.done, 'date': self.date}

	def load(self, data: dict[str, str | bool | list[list[str, bool]]]):
		""" Загрузка данных из сохранения. """
		self.active_daily_tasks = []

		for identifier, complete in data['tasks']:
			task = self.daily_tasks[identifier]
			if complete: task.complete()

			self.active_daily_tasks.append(task)

		self.done = data['done']
		self.date = data['date']

	def get_daily_tasks(self, num: int) -> DailyTask:
		""" Получение ежедневного задания по его номеру. """
		return self.active_daily_tasks[num]

	def complete(self, num: int) -> bool:
		""" Отмечает выполненным задание по номеру и проверяет на полное выполнение ежедневных заданий. """
		self.active_daily_tasks[num].complete()

		return self.all_complete()

	def all_complete(self) -> bool:
		if all(task.done for task in self.active_daily_tasks) and not self.done:
			self.done = True
		return self.done

	def update(self, tasks: list[DailyTask], today: str):
		""" Обновляет неактуальное задание. """
		complete = self.all_complete()

		for task in tasks: task.not_completed()
		self.active_daily_tasks = tasks
		self.date = today
		self.done = False

		return complete

	def size(self) -> int:
		""" Возвращает количество заданий. """
		return len(self.active_daily_tasks)
