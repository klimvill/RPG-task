from __future__ import annotations

from random import Random
from typing import TYPE_CHECKING

from .config import *
from .content import all_items
from .inventory import Item
from .utils import calculate_item_bonus

if TYPE_CHECKING:
	from .interface import Interface


class AwardsManager:
	"""
	Менеджер наград и наказаний.

	Параметры:
		interface (Interface): Экземпляр главного класса.

	Аргументы:
		rnd (Random): Объект класса Random.

	Методы:
		get_rewards_user_tasks(nums): Получение наград и наказаний для пользовательских заданий.
		get_rewards_daily_tasks(need_items): Получение наград и наказаний за ежедневные задания.
		get_price_skill(lvl): Получение цены.
		uniform(): Генерирует рандомное число в промежутке.
	"""

	def __init__(self, interface: Interface):
		self.interface = interface
		self.rnd = Random()

	def get_rewards_user_tasks(self, nums: list | set, need_items: bool = True) -> tuple[int, dict, list | list[Item]]:
		"""
		Получение наград и наказаний для пользовательских заданий.

		Аргументы:
			nums (list[int]): Номера заданий, за которые надо выдать награду.
			need_items (bool): Нужно ли выдавать предметы. Параметр необходим для наказаний. По умолчанию True.

		Возвращается:
			tuple: Кортеж, содержащий золото, опыт за навыки и предметы.
		"""
		gold, skills_exp, items = 0, {}, []
		sum_all_skills = self.interface.player.sum_level()
		if sum_all_skills < DIVISOR_SUM_LEVELS:
			sum_all_skills = DIVISOR_SUM_LEVELS

		for num in nums:
			skills = self.interface.task_manager.get_task(num).skills

			if skills is None:
				gold += self.uniform() * (sum_all_skills / DIVISOR_SUM_LEVELS) * MULTIPLIER_OBTAINING_GOLD
			else:
				gold += self.uniform() * (sum_all_skills / DIVISOR_SUM_LEVELS)

				for skill in skills:
					skill = self.interface.player.skills[skill]
					item_bonus = calculate_item_bonus(self.interface.inventory, skill)

					if skill.level > 0:
						exp = self.uniform() * skill.level * item_bonus
					else:
						exp = self.uniform() * item_bonus

					if skill in skills_exp:
						skills_exp[skill] += exp
					else:
						skills_exp[skill] = exp

			if self.rnd.choices([False, True], weights=PROBABILITY_ITEM_FALL_OUT)[0] and need_items:
				item_lvl = self.rnd.choices(['one', 'two', 'three'], weights=PROBABILITY_DROP_ITEM_CERTAIN_LEVEL)[0]
				identifier = self.rnd.choice(list(all_items[item_lvl].keys()))
				item = all_items[item_lvl][identifier]

				items.append(item)

		return gold, skills_exp, items

	def get_rewards_daily_tasks(self, tasks: list, need_items: bool = True) -> tuple[int, dict, list | list[Item]]:
		"""
		Получение наград и наказаний за ежедневные задания.

		Аргументы:
			nums (list[int | DailyTask]): Номера заданий, за которые надо выдать награду.
			need_items (bool): Нужно ли выдавать предметы. Параметр необходим для наказаний. По умолчанию True.

		Возвращается:
			tuple: Кортеж, содержащий золото, опыт за навыки и предметы.
		"""
		gold, skills_exp, items = 0, {}, []
		sum_all_skills = self.interface.player.sum_level()
		sum_all_skills = DIVISOR_SUM_LEVELS if sum_all_skills < DIVISOR_SUM_LEVELS else sum_all_skills

		for task in tasks:
			if isinstance(task, int):
				task = self.interface.daily_tasks_manager.get_task(task)

			if task.skills is None:
				gold += self.uniform() * (sum_all_skills / DIVISOR_SUM_LEVELS) * MULTIPLIER_OBTAINING_GOLD
			else:
				gold += self.uniform() * (sum_all_skills / DIVISOR_SUM_LEVELS)

				for skill in task.skills:
					skill = self.interface.player.skills[skill]
					item_bonus = calculate_item_bonus(self.interface.inventory, skill)

					if skill.level > 0:
						exp = self.uniform() * skill.level * item_bonus * DAILY_TASK_EXPERIENCE_MULTIPLIER
					else:
						exp = self.uniform() * item_bonus * DAILY_TASK_EXPERIENCE_MULTIPLIER

					if skill in skills_exp:
						skills_exp[skill] += exp
					else:
						skills_exp[skill] = exp

			if self.rnd.choices([False, True], weights=PROBABILITY_ITEM_FALL_OUT_DAILY_TASK)[0] and need_items:
				item_lvl = self.rnd.choices(['one', 'two', 'three'], weights=PROBABILITY_DROP_ITEM_CERTAIN_LEVEL)[0]
				identifier = self.rnd.choice(list(all_items[item_lvl].keys()))
				item = all_items[item_lvl][identifier]

				items.append(item)

		return gold, skills_exp, items

	@staticmethod
	def get_price_skill(lvl: int) -> tuple[float, float]:
		"""
		Получение цены навыка по его уровню.

		Аргументы:
			lvl (int): Уровень навыка.

		Возвращается:
			tuple: Количество опыта, цена.
		"""
		if lvl == 0:
			demand_exp, demand_gold = 0.25, 0.1
		elif lvl == 1:
			demand_exp, demand_gold = 0.5, 0.25
		else:
			demand_exp = round(CONSTANT_SKILL * lvl ** MULTIPLIER_SKILL, 2)
			demand_gold = round(CONSTANT_GOLD * lvl ** MULTIPLIER_GOLD, 2)

		return demand_exp, demand_gold

	def uniform(self, min_n: float = 0.01, max_n: float = 0.05) -> float:
		""" Генерирует рандомное число в промежутке """
		return self.rnd.uniform(min_n, max_n)
