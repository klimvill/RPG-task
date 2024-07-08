import json
from os import path

base_path = path.dirname(__file__)
hero_path = path.abspath(path.join(base_path, "..", "data/hero.json"))


def read_hero_info() -> dict[str: int, str: list[int, int]]:
	with open(hero_path, "r", encoding='utf-8') as file:
		return json.load(file)


def save_hero_info(data):
	with open(hero_path, "w", encoding='utf-8') as file:
		json.dump(data, file, ensure_ascii=False)
