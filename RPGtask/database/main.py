import json
from os import path
from typing import Any

from ..player import SkillType

base_path = path.dirname(__file__)
task_path = path.abspath(path.join(base_path, "..", "data/tasks.json"))
hero_path = path.abspath(path.join(base_path, "..", "data/player.json"))
inventory_path = path.abspath(path.join(base_path, "..", "data/inventory.json"))


def all_save(tasks, hero_info, inventory):
	save_tasks(tasks)
	save_hero_info(hero_info)
	save_read_inventory(inventory)


def save_tasks(data):
	with open(task_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)


def read_tasks() -> dict[str, list[list[str | list[SkillType] | None]] |
							  dict[str, str | bool | list[list[str, bool]]] |
							  dict[str, bool | list[list[str | int] | list[Any] | Any]]]:
	with open(task_path, "r", encoding='utf-8') as file:
		return json.load(file)


def save_hero_info(data):
	with open(hero_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)


def read_player_info() -> dict[str, float | list[list[int | float]]]:
	with open(hero_path, "r", encoding='utf-8') as file:
		return json.load(file)


def save_read_inventory(data):
	with open(inventory_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)


def read_inventory():
	with open(inventory_path, "r", encoding='utf-8') as file:
		return json.load(file)
