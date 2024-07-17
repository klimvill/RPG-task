from random import Random

from .content import all_items
from .data.config import MULTIPLIER_OBTAINING_GOLD, DAILY_TASK_EXPERIENCE_MULTIPLIER, CONSTANT_SKILL, MULTIPLIER_SKILL, \
	CONSTANT_GOLD, MULTIPLIER_GOLD, DIVISOR_SUM_LEVELS
from .inventory import Item
from .player import Skill
from .utils import calculate_item_bonus


class AwardsManager:
	def __init__(self, interface):
		self.interface = interface
		self.rnd = Random()

	def get_rewards_user_tasks(self, nums: list[int]) -> tuple[int, dict, list | list[Item]]:
		gold, skills_exp, items = 0, {}, []
		sum_all_skills = self.interface.player.sum_level()
		if sum_all_skills < DIVISOR_SUM_LEVELS:
			sum_all_skills = DIVISOR_SUM_LEVELS

		for num in nums:
			skills = self.interface.task_manager.get_task(num).skills

			if skills is None:
				gold += self.uniform() * MULTIPLIER_OBTAINING_GOLD * (sum_all_skills / DIVISOR_SUM_LEVELS)

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

			if self.rnd.choices([False, True], weights=[0.98, 0.02])[0]:
				item_lvl = self.rnd.choices(['one', 'two', 'three'], weights=[0.7, 0.25, 0.05])[0]
				identifier = self.rnd.choice(list(all_items[item_lvl].keys()))
				item = all_items[item_lvl][identifier]

				items.append(item)

		return gold, skills_exp, items

	def get_rewards_daily_tasks(self, need_items: bool = True) -> tuple[int, dict, list | list[Item]]:
		gold, skills_exp, items = 0, {}, []
		sum_all_skills = self.interface.player.sum_level()
		if sum_all_skills < DIVISOR_SUM_LEVELS:
			sum_all_skills = DIVISOR_SUM_LEVELS

		for num in range(len(self.interface.daily_tasks_manager.daily_tasks)):
			gold += self.uniform() * (sum_all_skills / DIVISOR_SUM_LEVELS)

			skills = self.interface.daily_tasks_manager.get_daily_tasks(num).skills

			for skill in skills:
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

			if self.rnd.choices([False, True], weights=[0.95, 0.05])[0] and need_items:
				item_lvl = self.rnd.choices(['one', 'two', 'three'], weights=[0.7, 0.25, 0.05])[0]
				identifier = self.rnd.choice(list(all_items[item_lvl].keys()))
				item = all_items[item_lvl][identifier]

				items.append(item)

		return gold, skills_exp, items

	def punishment_delete_tasks(self, nums: set[int]) -> tuple[int, dict[Skill, float]]:
		gold, skills_exp = 0, {}
		sum_all_skills = self.interface.player.sum_level()
		if sum_all_skills < DIVISOR_SUM_LEVELS:
			sum_all_skills = DIVISOR_SUM_LEVELS

		for num in nums:
			skills = self.interface.task_manager.get_task(num).skills

			if skills is None:
				gold += self.uniform() * MULTIPLIER_OBTAINING_GOLD * (sum_all_skills / DIVISOR_SUM_LEVELS)

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

		return gold, skills_exp

	@staticmethod
	def get_price_skill(lvl: int) -> tuple[float, float]:
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
