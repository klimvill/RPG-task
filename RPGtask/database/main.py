from os import path
import json

from .hero import save_hero_info
from .tasks import save_tasks

base_path = path.dirname(__file__)
inventory_path = path.abspath(path.join(base_path, "..", "data/inventory.json"))


def all_save(tasks, hero_info, data):
	save_tasks(tasks)
	save_hero_info(hero_info)
	save_read_inventory(data)


def read_inventory():
	with open(inventory_path, "r", encoding='utf-8') as file:
		return json.load(file)


def save_read_inventory(data):
	with open(inventory_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)
