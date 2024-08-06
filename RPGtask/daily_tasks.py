from .player import SkillType


class DailyTask:
	def __init__(self, task: str, skills: list[SkillType] | None, done: bool = False):
		self.task = task
		self.skills = skills
		self.done = done

	def save(self) -> tuple[str, list[SkillType] | None, bool]:
		""" Возвращает данные для сохранения заданий. """
		return self.task, self.skills, self.done

	def __str__(self):
		""" Формирует удобочитаемое представление объекта. """
		c = "[d][[green]x[/]]" if self.done else "[ ]"

		if self.skills:
			return f"{c} [yellow]{self.task}  [d cyan]Навыки: {', '.join(map(lambda s: SkillType.description(s), self.skills))}"
		return f"{c} [yellow]{self.task}"

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<DailyTask name={self.task!r} skills={len(self.skills)} done={self.done}>"


class DailyTaskManager:
	"""
	Менеджер ежедневных заданий.

	Атрибуты:
		daily_tasks (list[DailyTask]): Список всех ежедневных заданий. По умолчанию пустой список.
		date (str): Дата, когда задание было получено. По умолчанию пустая строка.
		done (bool): Выполнены ли задания. По умолчанию False.

	Методы:
		save(): Возвращает данные для сохранения ежедневных заданий.
		load(data): Загружает данные ежедневных заданий.
		add_task(task, skills): Добавляет ежедневную задачу в список активных.
		delete_task(num): Удаляет ежедневное задание по номеру. Если номер некорректный вызывает ошибку.
		get_task(num): Получение ежедневного задания по номеру. Если номер некорректный вызывает ошибку.
		complete(num): Отмечает ежедневную задачу выполненной и проверяет выполнение всех заданий.
		all_complete(): Если все задания выполнены, то отмечает это.
		update(): Начинает новый день.
	"""

	def __init__(self):
		self.daily_tasks: list[DailyTask] = []

		self.date: str = ''
		self.done: bool = False

	def save(self) -> dict[str, str | tuple[str, list[SkillType] | None, bool]]:
		""" Возвращает данные для сохранения ежедневных заданий. """
		return {'tasks': [task.save() for task in self.daily_tasks], 'date': self.date}

	def load(self, data: dict[str, str | tuple[str, list[SkillType] | None, bool]]):
		""" Загружает данные ежедневных заданий. """
		self.daily_tasks = [DailyTask(*task) for task in data['tasks']]
		self.date = data['date']

		self.all_complete()

	def add_task(self, task: str, skills: list[SkillType] = None):
		""" Добавляет ежедневную задачу в список активных. """
		self.daily_tasks.append(DailyTask(task, skills or None))
		self.done = False

	def delete_task(self, num: int) -> DailyTask:
		""" Удаляет ежедневное задание по номеру. Если номер некорректный вызывает ошибку. """
		if len(self.daily_tasks) >= num:
			return self.daily_tasks.pop(num - 1)
		raise ValueError(f"Daily task {num - 1} not found")

	def get_task(self, num: int) -> DailyTask:
		""" Получение ежедневного задания по номеру. Если номер некорректный вызывает ошибку. """
		if len(self.daily_tasks) >= num:
			return self.daily_tasks[num - 1]
		raise ValueError(f"Daily task {num - 1} not found")


	def complete(self, num: int):
		""" Отмечает ежедневную задачу выполненной и проверяет выполнение всех заданий. """
		self.get_task(num).done = True
		self.all_complete()

	def all_complete(self):
		""" Если все задания выполнены, то отмечает это. """
		self.done = all(task.done for task in self.daily_tasks)

	def update(self, today: str) -> list[DailyTask]:
		""" Начинает новый день. """
		# Получение невыполненных заданий. Для выдачи наказаний.
		not_complete_tasks = [task for task in self.daily_tasks if not task.done]

		# Сброс всех данных.
		self.daily_tasks = [DailyTask(task.task, task.skills) for task in self.daily_tasks]
		self.date = today
		self.done = False

		return not_complete_tasks

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<DailyTaskManager daily_tasks={len(self.daily_tasks)} date={self.date} done={self.done}>"
