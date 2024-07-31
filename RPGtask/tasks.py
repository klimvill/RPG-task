from typing import NoReturn

from .player import SkillType


class Task:
	"""
	Объект задания.

	Параметры:
		name (str): Имя задания.
		skills (Union[list[str], None]): Список навыков или None, если их нет.

	Методы:
		save(): Возвращает информацию для сохранения задачи.
		get_skills_descriptions(): Возвращает текстовое представление навыков задачи.
	"""

	def __init__(self, text: str, skills: list[SkillType] | None):
		self.text = text
		self.skills = skills

	def save(self) -> list[str | list[str] | None]:
		""" Возвращает информацию для сохранения задачи. """
		return [self.text, self.skills]

	def get_skills_descriptions(self) -> list[str] | None:
		""" Возвращает текстовое представление навыков задачи. """
		if self.skills is None:
			return None
		return list(map(lambda skill: SkillType.description(skill), self.skills))

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f'<Task name={self.text!r} skills={len(self.skills)}>'


class TaskManager:
	"""
	Менеджер всех пользовательских заданий.

	Аргументы:
		tasks (list[Task]): Список всех активных заданий.

	Методы:
		save(): Возвращает данные для сохранения всех заданий.
		load(data): Загружает данные заданий.
		add_task(name, skills): Добавляет задачу.
		get_task(num): Получение задания по номеру в списке.
		delete_task(num): Удаляет задание по номеру в списке.
		size(): Возвращает количество заданий.
		is_empty(): True если заданий нет, иначе False.
	"""

	def __init__(self):
		self.tasks: list[Task] = []

	def save(self) -> list[list[str | list[SkillType] | None]]:
		""" Возвращает данные для сохранения всех заданий. """
		return [task.save() for task in self.tasks]

	def load(self, data: list[list[str | list[int] | None]]) -> NoReturn:
		""" Загружает данные заданий. """
		self.tasks = [Task(*d) for d in data]

	def add_task(self, text: str, skills: list[SkillType] | None = None) -> NoReturn:
		"""
		Добавляет задачу.

		Аргументы:
			text (str): Текст задания.
			skills (Union[list[str], None]): Список навыков или None, если их нет.
		"""
		if not skills:
			skills = None
		self.tasks.append(Task(text, skills))

	def get_task(self, num: int) -> Task:
		"""
		Получение задания по номеру в списке.

		Аргументы:
			num (int): Номер задания.

		Возвращается:
			Task: Найденный объект задания.
		"""
		if num <= self.size():
			return self.tasks[num - 1]
		raise ValueError(f'Задание {num} не найдено')

	def delete_task(self, num: int) -> NoReturn:
		"""
		Удаляет задание по номеру в списке.

		Аргументы:
			num (int): Номер задания.
		"""
		if num <= self.size():
			self.tasks.pop(num - 1)
		else:
			raise ValueError(f'Задание {num} не найдено')

	def size(self) -> int:
		""" Возвращает количество заданий. """
		return len(self.tasks)

	def is_empty(self) -> bool:
		""" True если заданий нет, иначе False. """
		return not len(self.tasks)
