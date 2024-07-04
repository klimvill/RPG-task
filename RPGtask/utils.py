from random import uniform

from pyxdameraulevenshtein import damerau_levenshtein_distance
from .config import MULTIPLIER_OBTAINING_GOLD


def skill_check(skill: str, hero_info) -> str | None:
	"""
	Проверка на ошибки при записи навыков

	:param skill: str - навык
	:param hero_info:
	:return: str | None - правильная запись навыка или None
	"""
	skills_list = list(hero_info['skills'].keys())

	for correct_skill in skills_list:
		number = damerau_levenshtein_distance(skill.lower(), correct_skill)
		if number < 3:  # Считаем что разница в 2 символа и меньше еще нормальная
			return correct_skill
	return None


def get_information_about_task(num: int, tasks) -> tuple[str, list[str] | None, str | None] | None:
	# todo: Перенести в database

	user_tasks = tasks['user_tasks']
	daily_tasks = tasks['daily_tasks']
	quests = tasks['quests']

	if 0 < num <= len(user_tasks):
		text, skills, time = user_tasks[num - 1]

	elif len(user_tasks) < num <= len(daily_tasks):
		text, skills, time = daily_tasks[num - 1]

	elif len(daily_tasks) < num <= len(quests):
		text, skills, time = quests[num - 1]

	else:
		return None
	return text, skills, time


def get_task_text(num: int, tasks) -> str | None:
	# todo: Перенести в database

	if (_ := get_information_about_task(num, tasks)) is not None:
		return _[0]
	return None


def receiving_awards(nums: list[int], tasks, hero_info) -> list[int | dict | list]:
	nums = set(nums)
	hero_skills = hero_info['skills']

	# todo: Добавить функцию получения множителей для золота и навыков
	gold_multiplier = 1

	data = [0, {}, []]  # Золото, навыки и полученный опыт, предметы

	for num in nums:
		if (task_info := get_information_about_task(num, tasks)) is None:
			continue
		elif task_info[1] is None:
			data[0] += uniform(0.01 * gold_multiplier,
							   0.05 * gold_multiplier) * MULTIPLIER_OBTAINING_GOLD  # Если задание без навыков, то даём в два раза больше золота
			continue

		data[0] += uniform(0.01 * gold_multiplier, 0.05 * gold_multiplier)

		for skill in task_info[1]:
			skill_lvl = hero_skills[skill][0]
			if skill_lvl == 0: skill_lvl = 1

			exp = uniform(0.01, 0.05) * skill_lvl

			if skill in data[1]:
				data[1][skill] += exp
			else:
				data[1][skill] = 0
				data[1][skill] += exp

	return data
