from typing import NoReturn, Self

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
		save() -> list[str | bool]: Возвращает информацию для сохранения задачи.
		complete(): Отмечает задание выполненным.
		not_completed(): Отмечает задание не выполненным.
		get_skills_descriptions() -> list[str]: Возвращает текстовое представление навыков задачи.
	"""

	def __init__(self, text: str, skills: list[SkillType] | None = None, done: bool = False):
		self.text = text
		self.skills = skills
		self.done = done

	def save(self) -> list[str | list[SkillType] | None | bool]:
		""" Возвращает информацию для сохранения задачи. """
		return [self.text, self.skills, self.done]

	def complete(self) -> NoReturn:
		""" Отмечает задание выполненным. """
		self.done = True

	def not_completed(self) -> Self:
		""" Отмечает задание не выполненным.  """
		self.done = False
		return self

	def get_skills_descriptions(self) -> list[str] | None:
		""" Возвращает текстовое представление навыков задачи. """
		if self.skills is None:
			return None

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
		add_task(task, skills): Добавляет ежедневное задание.
		delete_task(num): Удаляет задание по номеру в списке.
		all_complete(): Проверяет выполнение всех заданий.
		update(): Обновляет неактуальное задание.
		size(): Возвращает количество заданий.
	"""

	def __init__(self):
		self.active_daily_tasks: list[DailyTask] = []

		self.done: bool = False
		self.date: str = ''

	def save(self) -> dict[str, str | bool | list[list[str, bool]]]:
		""" Возвращает данные для сохранения дневных заданий. """
		save_active_tasks = [task.save() for task in self.active_daily_tasks]

		return {'tasks': save_active_tasks, 'done': self.done, 'date': self.date}

	def load(self, data: dict[str, str | bool | list[list[str, bool]]]) -> NoReturn:
		""" Загрузка данных из сохранения. """
		self.active_daily_tasks = [DailyTask(text, skills, done) for text, skills, done in data['tasks']]

		self.done = data['done']
		self.date = data['date']

	def get_daily_tasks(self, num: int) -> DailyTask:
		""" Получение ежедневного задания по его номеру. """
		return self.active_daily_tasks[num]

	def complete(self, num: int) -> NoReturn:
		""" Отмечает выполненным задание по номеру и проверяет на полное выполнение ежедневных заданий. """
		self.active_daily_tasks[num].complete()

		self.all_complete()

	def add_task(self, task: str, skills: list[SkillType] | None = None) -> NoReturn:
		"""
		Добавляет ежедневное задание.

		Аргументы:
			text (str): Текст задания.
			skills (Union[list[str], None]): Список навыков или None, если их нет.
		"""
		self.done = False

		if not skills: skills = None
		self.active_daily_tasks.append(DailyTask(task, skills))

	def delete_task(self, num: int) -> NoReturn:
		"""
		Удаляет задание по номеру в списке.

		Аргументы:
			num (int): Номер задания.
		"""
		if num <= self.size():
			self.active_daily_tasks.pop(num - 1)
		else:
			raise ValueError(f'Задание {num} не найдено')

	def all_complete(self) -> NoReturn:
		""" Проверяет выполнение всех заданий. """
		if all(task.done for task in self.active_daily_tasks) and not self.done:
			self.done = True

	def update(self, today: str) -> list[int]:
		""" Обновляет неактуальное задание. """
		not_complete_tasks = [self.active_daily_tasks.index(task) for task in self.active_daily_tasks if not task.done]

		self.active_daily_tasks = [task.not_completed() for task in self.active_daily_tasks]
		self.date = today
		self.done = False

		return not_complete_tasks

	def size(self) -> int:
		""" Возвращает количество заданий. """
		return len(self.active_daily_tasks)
