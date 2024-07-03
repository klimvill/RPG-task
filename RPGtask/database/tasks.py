import json
from os import path

base_path = path.dirname(__file__)
task_path = path.abspath(path.join(base_path, "..", "data/tasks.json"))


def read_tasks():
	with open(task_path, "r", encoding='utf-8') as file:
		return json.load(file)


def save_tasks(data):
	with open(task_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)
