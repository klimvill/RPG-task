from random import uniform

from pyxdameraulevenshtein import damerau_levenshtein_distance

from .config import MULTIPLIER_OBTAINING_GOLD
from .database import get_information_about_task


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


def get_rewards_user_tasks(nums: list[int], tasks, hero_info):
	nums = set(nums)
	hero_skills = hero_info['skills']

	# todo: Добавить функцию получения множителей для золота и навыков
	gold_multiplier = 1

	data = [0, {}, []]  # Золото, навыки и полученный опыт, предметы

	for num in nums:
		if (task_info := get_information_about_task(num, tasks)) is None:
			continue
		elif task_info[1] is None:
			# Если задание без навыков, то даём в два раза больше золота.
			data[0] += uniform(0.01 * gold_multiplier, 0.05 * gold_multiplier) * MULTIPLIER_OBTAINING_GOLD
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


def receiving_awards(nums: set[int], tasks, hero_info) -> list[int | dict | list]:
	daily_tasks = tasks['daily_tasks']['tasks']
	hero_skills = hero_info['skills']

	# todo: Добавить функцию получения множителей для золота и навыков
	gold_multiplier = 1

	data = [0, {}, []]  # Золото, навыки и полученный опыт, предметы

	for num in nums:
		if (task_info := get_information_about_task(num, tasks)) is None: continue
		where = task_info[0]

		if where == 'user_tasks':
			if task_info[2] is None:
				data[0] += uniform(0.01 * gold_multiplier,
								   0.05 * gold_multiplier) * MULTIPLIER_OBTAINING_GOLD  # Если задание без навыков, то даём в два раза больше золота
				continue

			data[0] += uniform(0.01 * gold_multiplier, 0.05 * gold_multiplier)

		elif where == 'daily_tasks': continue

		for skill in task_info[2]:
			skill_lvl = hero_skills[skill][0]
			if skill_lvl == 0: skill_lvl = 1

			exp = uniform(0.01, 0.05) * skill_lvl

			if skill in data[1]:
				data[1][skill] += exp
			else:
				data[1][skill] = exp

	return data


def get_rewards_daily_tasks(daily_tasks, hero_info):
	data = [0, {}, []]  # Золото, навыки и полученный опыт, предметы
	hero_skills = hero_info['skills']

	gold_multiplier = 1

	for i in range(len(daily_tasks)):
		skills = daily_tasks[i][1]
		data[0] += uniform(0.01 * gold_multiplier, 0.05 * gold_multiplier)

		for skill in skills:
			skill_lvl = hero_skills[skill][0]
			if skill_lvl == 0: skill_lvl = 1
			exp = uniform(0.01, 0.05) * skill_lvl

			if skill in data[1]:
				data[1][skill] += exp
			else:
				data[1][skill] = exp

	return data
