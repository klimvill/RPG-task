import os
from typing import Sequence, NoReturn, Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree

from .config import CONSTANT_SKILL, MULTIPLIER_SKILL, CONSTANT_GOLD, MULTIPLIER_GOLD


class GameConsole:
	def __init__(self):
		self.console = Console()

	def menu(self, prompt: str, variants: Sequence, title: str, clear: bool = True) -> str:
		if not isinstance(variants, list):
			variants = list(variants)

		text_menu = '\n'
		for i, j in enumerate(variants, 1):
			text_menu += f'[{i}] {j}\n'

		while True:
			if clear: self.clear_console()

			self.console.print(Panel(text_menu, title=title, title_align='left', border_style="cyan"))
			res = Prompt.ask(prompt, console=self.console)

			if res.isnumeric() and 1 <= int(res) <= len(variants):
				return res

	def title(self, text, clear: bool = True) -> NoReturn:
		if clear:
			self.clear_console()

		self.console.print(text, justify='center')

	def print_task_tree(self, user_tasks: Sequence, daily_tasks: dict, quests: Sequence) -> NoReturn:
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

			text = user_tasks[i][0]
			skills = user_tasks[i][1]

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
		count_quests = len(quests)

		if count_quests == 0:
			branch_quests = tree.add(f'[b red]Квесты[/]\nВозьмите квест в гильдии')
		else:
			branch_quests = tree.add(f'[b red]Квесты [{count_daily_tasks}]')

		self.console.print(tree)
		input()

	def print_all_task(self, user_tasks: Sequence, daily_tasks: Sequence, quests: Sequence) -> NoReturn:
		count = 1

		# Вывод пользовательских заданий #
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

		# Вывод ежедневных заданий #
		self.console.print('[yellow]Ежедневные задания')
		if len(daily_tasks) == 0: print('Вы не добавили задания')

		for i in range(len(daily_tasks)):
			text, skills, done = daily_tasks[i]

			if done: _ = '[dim][[green]x[/]]'
			else: _ = '[ ]'

			if skills is None:
				self.console.print(f'[white]({count}) {_} {text}')
			else:
				self.console.print(f'[white]({count}) {_} {text}  [dim cyan]Навыки: {", ".join(skills)}')

			count += 1

		print()

		# Квесты #
		self.console.print('[red]Квесты')
		if len(quests) == 0: print('Вы не добавили задания')

		for i in range(len(quests)):
			text, skills = quests[i]

			if skills is None:
				self.console.print(f'[white]({i + 1}) {text}')
			else:
				self.console.print(f'[white]({i + 1}) {text}  [dim cyan]Навыки: {", ".join(skills)}')

		print()

	def print_tree_skills(self, title: str, skills: dict[str: float]) -> NoReturn:
		tree = Tree(title)

		for key, value in skills.items():
			tree.add(f'[magenta]{key.capitalize()} [green]+{round(value, 2)}')

		self.console.print(tree)

	def print_table_characteristics(self, skills: dict[str: float]):
		table = Table()

		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan')
		table.add_column('Опыт', style='green')

		for skill, item in skills.items():
			table.add_row(skill.capitalize(), str(round(item[0], 2)), str(round(item[1], 2)))

		self.console.print(table)

	def print_table_price(self, skills: dict[str: float], hero_info) -> list[str]:
		count = 1
		data = []
		table = Table()

		table.add_column('№')
		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan', justify='center')
		table.add_column('Мин. опыт', style='red')
		table.add_column('Стоимость', style='yellow')


		gold = float(hero_info['money'])

		for skill, item in skills.items():
			item = item[0]

			skill_exp = hero_info['skills'][skill][1]
			demand_exp = round(CONSTANT_SKILL * item ** MULTIPLIER_SKILL, 2)
			demand_gold = round(CONSTANT_GOLD * item ** MULTIPLIER_GOLD, 2)

			if item == 0: demand_exp, demand_gold = 0.25, 0.1
			elif item == 1: demand_exp, demand_gold = 0.5, 0.25


			if skill_exp >= demand_exp and gold >= demand_gold:
				table.add_row(
					f'{count}',
					skill.capitalize(),
					f'{round(item, 2)}',
					f'[green]{demand_exp} ({round(skill_exp, 2)})',
					f'{demand_gold}'
				)
			else:  # Поскольку пользователь не может купить улучшение оно затемнено
				table.add_row(
					f'{count}',
					f'[dim]{skill.capitalize()}',
					f'[dim]{round(item, 2)}',
					f'[dim red]{demand_exp} ({round(skill_exp, 2)})',
					f'[dim]{demand_gold}'
				)

			data.append(skill)
			count += 1

		self.console.print(table)
		return data

	def input(self, *args, **kwargs) -> Any:
		return self.console.input(*args, **kwargs)

	def print(self, *args, **kwargs) -> NoReturn:
		"""Prints the given arguments."""
		self.console.print(*args, **kwargs, highlight=False)

	@staticmethod
	def clear_console():
		os.system('cls')
