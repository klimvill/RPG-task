import os
from typing import Sequence, NoReturn, Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree


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

	def print_task_tree(self, user_tasks: Sequence, daily_tasks: Sequence, quests: Sequence) -> NoReturn:
		tree = Tree('Задания')

		# Пользовательские задания #
		count_user_tasks = len(user_tasks)
		end = ''

		if count_user_tasks == 0:
			branch_user_tasks = tree.add(f'[b green]Пользовательские задания[/b green]\nВы не добавили задания\n')
		else:
			branch_user_tasks = tree.add(f'[b green]Пользовательские задания [{count_user_tasks}]')

		for i in range(count_user_tasks):
			if i == count_user_tasks - 1: end = '\n'

			text = user_tasks[i][0]
			skills = user_tasks[i][1]
			time = user_tasks[i][2]

			if skills is None and time is None:
				branch_user_tasks.add(f'[green]{text}[/green]' + end)
			elif skills is None:
				branch_user_tasks.add(f'[green]{text}[/green]  [dim cyan]Кончается через: {time}[/dim cyan]' + end)
			elif time is None:
				branch_user_tasks.add(f'[green]{text}[/green]  [dim cyan]Навыки: {", ".join(skills)}[/dim cyan]' + end)
			else:
				branch_user_tasks.add(
					f'[green]{text}[/green]  [dim cyan]Навыки: {", ".join(skills)} | Кончается через: {time}[/dim cyan]' + end)

		# Ежедневные задания #
		count_daily_tasks = len(daily_tasks)

		if count_daily_tasks == 0:
			branch_user_tasks = tree.add(f'[b yellow]Ежедневные задания[/b yellow]\nКончились...\n')
		else:
			branch_user_tasks = tree.add(f'[b yellow]Ежедневные задания [{count_daily_tasks}]')

		# Квесты #
		count_quests = len(quests)

		if count_quests == 0:
			branch_quests = tree.add(f'[b red]Квесты[/b red]\nВозьмите квест в гильдии')
		else:
			branch_quests = tree.add(f'[b red]Квесты [{count_daily_tasks}]')

		self.console.print(tree)
		input()

	def print_all_task(self, user_tasks: Sequence, daily_tasks: Sequence, quests: Sequence) -> NoReturn:
		# Вывод пользовательских заданий #
		self.console.print(f'[green]Пользовательские задания[/green]')

		if len(user_tasks) == 0: print('Вы не добавили задания')

		for i in range(len(user_tasks)):
			text, skills, time = user_tasks[i]

			if skills is None and time is None:
				self.console.print(f'[white]({i + 1}) {text}[/white]')
			elif skills is None:
				self.console.print(f'[white]({i + 1}) {text}[/white]  [dim cyan]Кончается через: {time}[/dim cyan]')
			elif time is None:
				self.console.print(f'[white]({i + 1}) {text}[/white]  [dim cyan]Навыки: {", ".join(skills)}[/dim cyan]')
			else:
				self.console.print(
					f'[white]({i + 1}) {text}[/white]  [dim cyan]Навыки: {", ".join(skills)} | Кончается через: {time}[/dim cyan]')

		print()

	def print_tree_skills(self, title: str, skills: dict[str: float]) -> NoReturn:
		tree = Tree(title)

		for key, value in skills.items():
			tree.add(f'[magenta]{key.capitalize()} [green]+{round(value, 2)}[/green][/magenta]')

		self.console.print(tree)

	def print_table_characteristics(self, skills: dict[str: float]):
		table = Table(row_styles=['', 'dim'])

		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan')
		table.add_column('Опыт', style='green')

		for skill, i in skills.items():
			table.add_row(skill.capitalize(), str(round(i[0], 2)), str(round(i[1], 2)))

		self.console.print(table)

	def print_table_price(self, skills: dict[str: float]):
		count = 1
		table = Table(row_styles=['', 'dim'])

		table.add_column('№', style='green')
		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan')
		table.add_column('Стоимость', style='yellow')

		for skill, i in skills.items():
			table.add_row(str(count), skill.capitalize(), str(round(i[0], 2)), str(round(0.05 * i[0] * 1.5, 2)))
			count += 1

		self.console.print(table)

	def input(self, *args, **kwargs) -> Any:
		return self.console.input(*args, **kwargs)

	def print(self, *args, **kwargs) -> NoReturn:
		"""Prints the given arguments."""
		self.console.print(*args, **kwargs, highlight=False)

	@staticmethod
	def clear_console():
		os.system('cls')
