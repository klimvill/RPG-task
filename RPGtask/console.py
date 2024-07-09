import os
from itertools import groupby
from typing import Literal, NoReturn, Any, Optional, Callable

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree

from .inventory import ItemType, Slot, Item
from .utils import get_item, calculate


class MyConsole:
	def __init__(self, interface):
		self.interface = interface

		self.console = Console()

	def menu(self, prompt: str, variants: list, title: str, clear: bool = True) -> Any:
		text_menu = '\n'

		for i, j in enumerate(variants, 1):
			text_menu += f'[{i}] {j}\n'

		while True:
			if clear:
				self.clear_console()

			self.panel_print(text_menu, title)
			res = Prompt.ask(prompt)

			if res.isnumeric() and 1 <= int(res) <= len(variants):
				return res

	def panel_print(self, text: str, title: str,
					title_align: Literal['left', 'center', 'right'] = 'left',
					border_style: str = 'cyan') -> NoReturn:
		self.console.print(Panel(text, title=title, title_align=title_align, border_style=border_style))

	def title(self, text, clear: bool = True) -> NoReturn:
		if clear:
			self.clear_console()

		self.console.print(text, justify='center')

	def print_tree_skills(self, title: str, skills: dict[str: float]) -> NoReturn:
		tree = Tree(title)

		for key, value in skills.items():
			tree.add(f'[magenta]{key.capitalize()} [green]+{round(value, 2)}')

		self.console.print(tree)

	def print_task_tree(self) -> NoReturn:
		user_tasks = self.interface.tasks['user_tasks']
		daily_tasks = self.interface.tasks['daily_tasks']
		quests = self.interface.tasks['quests']

		tree = Tree('Задания')

		# Пользовательские задания #
		count_user_tasks = len(user_tasks)
		end = ''

		if count_user_tasks == 0:
			branch_user_tasks = tree.add(f'[b green]Пользовательские задания[/]\nВы не добавили задания\n')
		else:
			branch_user_tasks = tree.add(f'[b green]Пользовательские задания [{count_user_tasks}]')

		for i in range(count_user_tasks):
			if i == count_user_tasks - 1: end = '\n'

			text, skills = user_tasks[i]

			if skills is None:
				branch_user_tasks.add(f'[green]{text}' + end)
			else:
				branch_user_tasks.add(f'[green]{text}  [dim cyan]Навыки: {", ".join(skills)}' + end)

		# Ежедневные задания #
		done = daily_tasks['done']
		count_daily_tasks = len(daily_tasks['tasks'])
		end = ''

		if done:
			branch_user_tasks = tree.add(f'[[green]x[/]] [b yellow]Ежедневные задания')
		elif count_daily_tasks == 0:
			branch_user_tasks = tree.add(f'[b yellow]Ежедневные задания[/]\nКончились...\n')
		else:
			branch_user_tasks = tree.add(f'[ ] [b yellow]Ежедневные задания')

		for i in range(count_daily_tasks):
			if i == count_daily_tasks - 1: end = '\n'

			text, skills, done = daily_tasks['tasks'][i]

			if done:
				_ = '[dim][[green]x[/]]'
			else:
				_ = '[ ]'

			if skills is None:
				branch_user_tasks.add(f'{_} [yellow]{text}' + end)
			else:
				branch_user_tasks.add(f'{_} [yellow]{text}  [dim cyan]Навыки: {", ".join(skills)}' + end)

		# Квесты #
		count_quests = len(self.interface.quest_manager.active_quests)

		if count_quests == 0:
			branch_quests = tree.add(f'[b red]Квесты[/]\nВозьмите квест в гильдии')

		for active in self.interface.quest_manager.active_quests:
			# QUEST_NAME 1/3 QUEST_DESCRIPTION
			c = "green" if active.done else "red"
			quest_tree = tree.add(
				f"[{c} b]{active.quest.name} [white b]{len(active.done_stages)}/{len(active.quest.stages)}\n{active.quest.description}"
			)
			for sid in active.done_stages:
				# "[x] STAGE_NAME"
				stage = active.quest.stages[sid]
				quest_tree.add(f"[white][[green]x[white]] [green]{stage.name}")
			# if completed, skip stage progress tree
			if active.done:
				continue
			# "[ ] STAGE_NAME"
			stage_tree = quest_tree.add(f"[white][ ] [green]{active.stage.name}")
			for goal in active.goals:
				# "[ ] GOAL_NAME"
				#       GOAL_DESCRIPTION
				mark = "x" if goal.completed else " "
				stage_tree.add(
					f"[white][[green]{mark}[white]] [blue]{goal.name}\n"
					f"[yellow]{goal.description}"
				)


		self.console.print(tree)
		input()

	def print_user_tasks(self, count: int = 1) -> int:
		user_tasks = self.interface.tasks['user_tasks']

		self.console.print('[green]Пользовательские задания')
		if len(user_tasks) == 0: print('Вы не добавили задания')

		for _ in range(len(user_tasks)):
			text, skills = user_tasks[_]

			if skills is None:
				self.console.print(f'[white]({count}) {text}')
			else:
				self.console.print(f'[white]({count}) {text}  [dim cyan]Навыки: {", ".join(skills)}')

			count += 1

		print()
		return count

	def print_daily_tasks(self, count: int) -> int:
		daily_tasks = self.interface.tasks['daily_tasks']

		self.console.print('[yellow]Ежедневные задания')
		if len(daily_tasks) == 0: print('Вы не добавили задания')

		for i in range(len(daily_tasks)):
			text, skills, done = daily_tasks['tasks'][i]

			if done:
				_ = '[dim][[green]x[/]]'
			else:
				_ = '[ ]'

			if skills is None:
				self.console.print(f'[white]({count}) {_} {text}')
			else:
				self.console.print(f'[white]({count}) {_} {text}  [dim cyan]Навыки: {", ".join(skills)}')

			count += 1

		print()
		return count

	def print_quests(self, count: int) -> int:
		# quests = self.interface.tasks['quests']

		if len(self.interface.quest_manager.active_quests) == 0:
			self.console.print('[red]Квесты')
			print('Возьмите квест в гильдии')

		for active in self.interface.quest_manager.active_quests:
			# "[ ] STAGE_NAME"
			# self.console.print(f"[white][ ] [green]{active.stage.name}")

			# "[ ] GOAL_NAME"
			#       GOAL_DESCRIPTION
			"""
			mark = "v" if goal.completed else " "


			self.console.print(
				f"[white]({count}) [[green]{mark}[white]] [yellow]{goal.description}  [dim blue]{goal.name}"
			)
			"""
			c = "green" if active.done else "red"
			tree = Tree(f"[{c} b]{active.quest.name} [white b]{len(active.done_stages)}/{len(active.quest.stages)}\n{active.quest.description}")

			for sid in active.done_stages:
				# "[x] STAGE_NAME"
				stage = active.quest.stages[sid]
				tree.add(f"[white][[green]x[white]] [green]{stage.name}")
			# if completed, skip stage progress tree
			if active.done:
				continue
			# "[ ] STAGE_NAME"
			stage_tree = tree.add(f"[white][ ] [green]{active.stage.name}")
			for goal in active.goals:
				# "[ ] GOAL_NAME"
				#       GOAL_DESCRIPTION
				mark = "x" if goal.completed else " "
				stage_tree.add(
					f"[white]({count}) [[green]{mark}[white]] [blue]{goal.name}\n"
					f"[yellow]{goal.description}"
				)

				count += 1

		self.console.print(tree)
		print()
		return count

	def print_all_task(self) -> NoReturn:
		count = self.print_user_tasks()  # Вывод пользовательских заданий
		count = self.print_daily_tasks(count)  # Вывод ежедневных заданий
		return self.print_quests(count)  # Вывод квестов

	def print_table_characteristics(self, skills: dict[str: float]):
		table = Table()

		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan')
		table.add_column('Опыт', style='green')
		table.add_column('Бонус')

		for skill, item in skills.items():
			bonus = calculate(self.interface.inventory, skill, percent=True)

			if bonus == 0: bonus = '[dim]0%'
			elif bonus > 1: bonus = f'[green]+{bonus}%'
			else: bonus = f'[red]{bonus}%'

			table.add_row(skill.capitalize(), str(round(item[0], 2)), str(round(item[1], 2)), bonus)

		self.console.print(table)

	def print_table_price(self):
		hero_info = self.interface.hero_info
		skills = hero_info['skills']
		table = Table()

		table.add_column('№')
		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan', justify='center')
		table.add_column('Мин. опыт', style='red')
		table.add_column('Стоимость', style='yellow')

		gold = float(hero_info['money'])
		count = 1

		for skill, item in skills.items():
			lvl, skill_exp = item

			demand_exp, demand_gold = self.interface.awards.get_price_skill(lvl)

			if lvl == 0:
				demand_exp, demand_gold = 0.25, 0.1
			elif lvl == 1:
				demand_exp, demand_gold = 0.5, 0.25

			if skill_exp >= demand_exp and gold >= demand_gold:
				table.add_row(
					f'{count}',
					skill.capitalize(),
					f'{lvl}',
					f'[green]{demand_exp} ({round(skill_exp, 2)})',
					f'{demand_gold}'
				)
			else:  # Поскольку пользователь не может купить улучшение оно затемнено
				table.add_row(
					f'{count}',
					f'[dim]{skill.capitalize()}',
					f'[dim]{lvl}',
					f'[dim]{demand_exp} ({round(skill_exp, 2)})',
					f'[dim]{demand_gold}'
				)
			count += 1

		self.console.print(table)

	def print_item_tree(self, items: list[Item]) -> NoReturn:
		tree = Tree('\n[bold cyan]Вы нашли предметы:')

		for item in items:
			tree.add(f'{item.name}')

		self.console.print(tree)

	def presence_item(self, item: Item):
		"""
		Presents the information of the given item to the user interface.

		Args:
			item (Item): The item to present.
		"""

		def get_effects_string(effects: dict[str, int]) -> str:
			if not effects:
				return "[b red]Эффектов нет[/]\n"
			result = "[b red]Эффекты[/]:\n"
			for key, value in effects.items():
				if value > 1:
					result += f"    {key}: [green]+{int(value * 100 - 100)}%[/]\n"
				else:
					result += f"    {key}: [red]{int(value * 100 - 100)}%[/]\n"
			return result

		item_type_info = f"[b green]Тип[/]: {ItemType.description(item.type)}\n"
		effects_info = get_effects_string(item.effects)
		sell_info = (
			f"[b yellow]Цена продажи[/]: {item.sell}\n"
			if item.sell > 0
			else "[b yellow]Ничего не стоит[/]\n"
		)
		cost_info = (
			f"[b yellow]Цена покупки[/]: {item.cost}\n"
			if item.cost > 0
			else "[b yellow]Не продается[/]\n"
		)
		result = f"[purple b]{item.name}[/] - [white]{item.description}\n"
		result += item_type_info
		result += effects_info
		result += cost_info
		result += sell_info
		self.console.print(result)

	def show_item(
			self, slot: Slot, show_amount=True, additional: Optional[Callable] = None
	):
		"""
		Generates a string representation of the item in the given slot.

		Args:
			slot (Slot): The slot containing the item.
			show_amount (bool, optional): Whether to display the amount of the item. Defaults to True.
			additional (callable, optional): Additional information to display about the item. Defaults to None.

		Returns:
			str: The generated string representation of the item.
		"""
		if slot.empty:
			return "[yellow]-[/] "
		item = get_item(slot.id)
		text = ""
		if show_amount:
			text += f"[white]{slot.amount}x"
		text += f"[green]{item.name}[/] "
		if additional:
			text += additional(item)
		return text

	def show_inventory(
			self,
			show_number=True,
			show_amount=False,
			allow: Optional[list[ItemType]] = None,
			inverse: bool = False,
	):
		"""
		Presents the player's inventory to the user interface.

		Args:
			show_number (bool, optional): Whether to display numbers for each item. Defaults to False.
			show_amount (bool, optional): Whether to display the amount of each item. Defaults to True.
			allow (list[ItemType], optional): The list of allowed item types to display. Defaults to None.
			inverse (bool, optional): Whether to display items not in the allowed list. Defaults to False.
		"""
		inventory = self.interface.inventory

		grouped_slots = groupby(inventory.slots, lambda i: i.type)
		counter = 1
		for slot_type, slots in grouped_slots:
			if allow:
				# whitelist
				if not inverse and slot_type not in allow:
					continue
				# blacklist
				if inverse and slot_type in allow:
					continue
			self.console.print("[yellow b]" + ItemType.description(slot_type), end=" ")
			for slot in slots:
				if show_number:
					self.console.print(f"[blue]\\[{counter}][/]", end="")
					counter += 1
				self.console.print(self.show_item(slot, show_amount), end="")
			self.console.print()

	def input(self, *args, **kwargs) -> Any:
		return self.console.input(*args, **kwargs)

	def print(self, *args, **kwargs) -> NoReturn:
		"""Prints the given arguments."""
		self.console.print(*args, **kwargs, highlight=False)

	@staticmethod
	def clear_console():
		os.system('cls')
