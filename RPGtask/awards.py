import random

from .config import *
from .data.items import all_items
from .database import get_information_about_task
from .inventory import Item, Inventory
from .utils import calculate


class AwardsManager:
	def __init__(self, inventory: Inventory):
		self.rnd = random.Random()
		self.inventory = inventory

	def uniform(self, min_n: float = 0.01, max_n: float = 0.05) -> float:
		""" Генерирует рандомное число в промежутке """
		return self.rnd.uniform(min_n, max_n)

	def get_rewards_user_tasks(self, nums: set[int], tasks,
							   hero_skills: dict[str, list[float, float]]) -> tuple[int, dict, list | list[Item]]:
		# todo: Добавить функцию получения множителей для золота и навыков
		gold_multiplier = 1

		gold, skills_exp, items = 0, {}, []

		for num in nums:
			task_info = get_information_about_task(num, tasks)

			if task_info is None or task_info[0] != 'user_tasks':
				continue

			# Если задание без навыков, то даём больше золота.
			elif task_info[2] is None:
				gold += self.uniform() * MULTIPLIER_OBTAINING_GOLD * gold_multiplier

			else:
				gold += self.uniform() * gold_multiplier

				for skill in task_info[2]:
					skill_lvl = hero_skills[skill][0]
					item_bonus = calculate(self.inventory, skill)

					if skill_lvl == 0: skill_lvl = 1

					exp = self.uniform() * skill_lvl * item_bonus

					if skill in skills_exp:
						skills_exp[skill] += exp
					else:
						skills_exp[skill] = exp

			if self.rnd.choices([False, True], weights=[0.98, 0.02])[0]:
				item_lvl = self.rnd.choices(['one', 'two', 'three'], weights=[0.7, 0.25, 0.05])[0]

				identifier = self.rnd.choice(list(all_items[item_lvl].keys()))
				items.append(all_items[item_lvl][identifier])

		return gold, skills_exp, items

	def get_rewards_daily_tasks(self, daily_tasks: list[list[str, list | None, bool]],
								hero_skills: dict[str, list[float, float]]) -> tuple[int, dict, list | list[Item]]:
		gold, skills_exp, items = 0, {}, []
		gold_multiplier = 1

		for i in range(len(daily_tasks)):
			gold += self.uniform() * gold_multiplier

			for skill in daily_tasks[i][1]:
				skill_lvl = hero_skills[skill][0]
				if skill_lvl == 0: skill_lvl = 1

				item_bonus = calculate(self.inventory, skill)

				exp = self.uniform() * skill_lvl * item_bonus

				if skill in skills_exp:
					skills_exp[skill] += exp
				else:
					skills_exp[skill] = exp

		if self.rnd.choices([False, True], weights=[0.95, 0.05])[0]:
			item_lvl = self.rnd.choices(['one', 'two', 'three'], weights=[0.7, 0.25, 0.05])[0]

			identifier = self.rnd.choice(list(all_items[item_lvl].keys()))
			items.append(all_items[item_lvl][identifier])

		return gold, skills_exp, items

	@staticmethod
	def get_price_skill(lvl: int) -> tuple[float, float]:
		demand_exp = round(CONSTANT_SKILL * lvl ** MULTIPLIER_SKILL, 2)
		demand_gold = round(CONSTANT_GOLD * lvl ** MULTIPLIER_GOLD, 2)
		return demand_exp, demand_gold
