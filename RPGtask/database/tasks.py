import json
from os import path

base_path = path.dirname(__file__)
task_path = path.abspath(path.join(base_path, "..", "data/tasks.json"))


def read_tasks() -> dict[str, list | dict]:
	with open(task_path, "r", encoding='utf-8') as file:
		return json.load(file)


def save_tasks(data):
	with open(task_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)


def get_where(num: int, tasks) -> str | None:
	user_tasks = tasks['user_tasks']
	daily_tasks = tasks['daily_tasks']['tasks']
	quests = tasks['quests']

	if 0 < num <= len(user_tasks):
		where = 'user_tasks'
	elif len(user_tasks) < num <= len(daily_tasks):
		where = 'daily_tasks'
	elif len(daily_tasks) < num <= len(quests):
		where = 'quests'
	else:
		return None
	return where


def get_information_about_task(num: int, tasks) -> tuple[str, str, list[str] | None] | tuple[str, int] | None:
	user_tasks = tasks['user_tasks']
	daily_tasks = tasks['daily_tasks']['tasks']

	if 0 < num <= len(user_tasks):
		where = 'user_tasks'
		text, skills = user_tasks[num - 1]

	elif len(user_tasks) < num <= len(daily_tasks) + len(user_tasks):
		where = 'daily_tasks'
		text, skills, done = daily_tasks[num - len(user_tasks) - 1]

	elif len(daily_tasks) + len(user_tasks) < num:
		where = 'quests'
		return where, num - len(user_tasks) - len(daily_tasks) - 1

	else:
		return None
	return where, text, skills


def get_task_text(num: int, tasks) -> str | None:
	if (_ := get_information_about_task(num, tasks)) is not None:
		return _[1]
	return None
