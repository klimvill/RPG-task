from pyxdameraulevenshtein import damerau_levenshtein_distance

from .content import all_items
from .inventory import Item, ItemType, Inventory
from .player import SKILL_DESCRIPTIONS, SkillType


def skill_check(skill: str) -> SkillType | None:
	""" Проверка на ошибки при записи навыков """
	for d, correct_skill in SKILL_DESCRIPTIONS.items():
		number = damerau_levenshtein_distance(skill.lower(), correct_skill.lower())
		if number < 3:  # Считаем что разница в 2 символа и меньше еще нормальная
			return d
	return None


def get_item(identifier: str | Item) -> Item:
	"""
	Получение предмета по идентификатору.

	Аргументы:
		identifier (Union[str, Item]): идентификатор предмета.
	"""
	if isinstance(identifier, Item):
		return identifier

	if identifier in all_items['one']:
		return all_items['one'][identifier]
	elif identifier in all_items['two']:
		return all_items['two'][identifier]
	elif identifier in all_items['three']:
		return all_items['three'][identifier]

	raise ValueError(f"Item {identifier} not found")


def calculate_item_bonus(inventory: Inventory, skill: SkillType, percent: bool = False) -> int:
	"""
	Считает бонусы предметов к навыку.

	Аргументы:
		inventory (Inventory): объект инвентаря.
		skill (SkillType): тип навыка, бонус к которому мы считаем.
		percent (bool): Если True, то возвращаем результат в виде процента, иначе в десятичном виде.
	"""
	result: int = int(not percent)

	for _, slot in inventory.get(ItemType.ITEM, True):
		if not slot.empty:
			item = get_item(slot.id)

			try:
				if percent:
					result += int(item.effects[skill] * 100 - 100)
				else:
					if item.effects[skill] >= 1:
						result += item.effects[skill] % 1
					else:
						result -= 1 - item.effects[skill]
			except KeyError:
				continue
	return result
