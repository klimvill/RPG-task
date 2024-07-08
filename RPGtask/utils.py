from pyxdameraulevenshtein import damerau_levenshtein_distance
from .inventory import Item
from .data.items import all_items


def skill_check(skill: str, hero_info) -> str | None:
	"""
	Проверка на ошибки при записи навыков
	"""
	skills_list = list(hero_info['skills'].keys())

	for correct_skill in skills_list:
		number = damerau_levenshtein_distance(skill.lower(), correct_skill)
		if number < 3:  # Считаем что разница в 2 символа и меньше еще нормальная
			return correct_skill
	return None


def get_item(identifier: str | Item) -> Item:
	if isinstance(identifier, Item):
		return identifier

	if identifier in all_items['one']:
		return all_items['one'][identifier]
	elif identifier in all_items['two']:
		return all_items['two'][identifier]
	elif identifier in all_items['three']:
		return all_items['three'][identifier]

	raise ValueError(f"Item {identifier} not found")
