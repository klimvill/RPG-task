from datetime import date

from .player import SkillType


class DailyTask:
	def __init__(self, identifier: str, text: str, skills: list[SkillType]):
		self.id = identifier
		self.text = text
		self.skills = skills

	def get_skills_descriptions(self) -> list[str] | None:
		if self.skills is None:
			return None
		return list(map(lambda skill: SkillType.description(skill), self.skills))


class DailyTaskManager:
	def __init__(self):
		self.daily_tasks: dict[str, DailyTask] = {}

		self.active_daily_tasks: list[list[str | bool]] = []
		self.done: bool = False
		self.date: str = ''

	def save(self) -> dict[str, str | bool | list[list[str, bool]]]:
		return {'tasks': self.active_daily_tasks, 'done': self.done, 'date': self.date}

	def load(self, data: dict[str, str | bool | list[list[str, bool]]]):
		self.active_daily_tasks = data['tasks']
		self.done = data['done']
		self.date = data['date']

	def get_daily_tasks(self, num: int) -> DailyTask:
		identifier = self.active_daily_tasks[num][0]

		for task in list(self.daily_tasks.values()):
			if task.id == identifier:
				return task

		raise ValueError(f"Quest {identifier} not found")

	def complete(self, num: int) -> bool:
		self.active_daily_tasks[num][1] = True

		if all(task[1] for task in self.active_daily_tasks) and not self.done:
			self.done = True
			return True
		return False

	def update(self, tasks: list[DailyTask]):
		today = str(date.today())

		if self.date == '' or self.date != today:
			self.active_daily_tasks = []
			self.date = today
			self.done = False

			for task in tasks:
				self.active_daily_tasks.append([task.id, False])

	def size(self) -> int:
		""" Возвращает количество заданий. """
		return len(self.active_daily_tasks)
