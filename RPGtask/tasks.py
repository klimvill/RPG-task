from .player import SkillType


class Task:
	def __init__(self, task: str, skills: list[SkillType] | None):
		self.task = task
		self.skills = skills

	def save(self) -> tuple[str, list[SkillType] | None]:
		""" Возвращает данные для сохранения заданий. """
		return self.task, self.skills

	def __str__(self):
		""" Формирует удобочитаемое представление объекта. """
		if self.skills:
			return f"[green]{self.task}  [d cyan]Навыки: {', '.join(map(lambda s: SkillType.description(s), self.skills))}"
		return '[green]' + self.task

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Task name={self.task!r} skills={len(self.skills)}>"


class TaskManager:
	"""
	Менеджер обычных заданий.

	Атрибуты:
		tasks (list[Task]): Список активных заданий.

	Методы:
		save(): Возвращает данные для сохранения обычных заданий.
		load(data): Загружает данные обычных заданий.
		add_task(name, skills): Добавляет задачу в список активных.
		delete_task(num): Удаляет задание по номеру. Если номер некорректный вызывает ошибку.
		get_task(num): Получение задания по номеру. Если номер некорректный вызывает ошибку.
		is_empty(): True если заданий нет, иначе False.
	"""

	def __init__(self):
		self.tasks: list[Task] = []

	def save(self) -> list[tuple[str, list[SkillType] | None]]:
		""" Возвращает данные для сохранения обычных заданий. """
		return [task.save() for task in self.tasks]

	def load(self, data: list[tuple[str, list[SkillType] | None]]):
		""" Загружает данные обычных заданий. """
		self.tasks = [Task(*task) for task in data]

	def add_task(self, task: str, skills: list[SkillType] = None):
		""" Добавляет задачу в список активных. """
		self.tasks.append(Task(task, skills or None))

	def delete_task(self, num: int) -> Task:
		""" Удаляет задание по номеру. Если номер некорректный вызывает ошибку. """
		if len(self.tasks) >= num:
			return self.tasks.pop(num - 1)
		raise ValueError(f"Task {num - 1} not found")

	def get_task(self, num: int) -> Task:
		""" Получение задания по номеру. Если номер некорректный вызывает ошибку. """
		if len(self.tasks) >= num:
			return self.tasks[num - 1]
		raise ValueError(f"Task {num - 1} not found")

	def is_empty(self) -> bool:
		""" True если заданий нет, иначе False. """
		return not self.tasks

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<TaskManager tasks={len(self.tasks)}>"
