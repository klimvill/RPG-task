from __future__ import annotations

import logging
import os
from itertools import groupby
from typing import Any, NoReturn, Literal, Optional, TYPE_CHECKING

from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from .inventory import Slot, Item, ItemType
from .player import SkillType, Skill, RankType
from .quests import Quest, BossFight
from .utils import get_item

if TYPE_CHECKING:
	from .interface import Interface


class AppConsole:
	"""
	Класс представляющий консоль.

	Параметры:
		interface (Interface): Экземпляр главного класса.

	Аргументы:
		console (Console): Объект консоли.
		log (Logger): Объект логгера. Печатает ошибки.

	Методы:
		menu(prompt, variants, title, clear): Печатает меню и текст, который предлагает пользователю сделать выбор.
		panel_print(text, title, title_align, border_style): Печатает текст в 	панели.
		title(text, clear): Печатает заголовок, в котором обычно находится справочная информация.

		print_tree_skills(title, skills): Печатает дерево наград для навыков.
		print_task_tree(): Печатает дерево для просмотра всех заданий.

		print_user_tasks(): Печатает пользовательские задания.
		print_daily_tasks(count): Печатает ежедневные задания.
		print_quests(count): Печатает квесты.
		print_all_task(): Печатает все задания.

		print_item_tree(items): Печатает красивое представление найденных предметов.

		print_shop_quest(quests): Печатает магазин квестов.
		print_shop(items): Печатает магазин предмет.
		print_skill_shop(gold, skills): Печатает магазин навыков.

		presence_item(item): Отображает информацию о предмете.
		show_item(slot): Генерирует строковое представление предмета в заданном слоте.
		show_inventory():Отображает инвентарь игрока.

		create_progress_bar(value, maximum):Создаёт индикатор выполнения.

		input(): Запрашивает ввод пользователя.
		print(): Выводит заданные аргументы.
		clear_console(): Очищает консоль.
	"""

	def __init__(self, interface: Interface):
		self.interface = interface
		self.console = Console()

		handler = RichHandler(markup=True, rich_tracebacks=True, console=self.console, tracebacks_show_locals=True)
		logging.basicConfig(level="NOTSET", format="%(message)s", datefmt="[%X]", handlers=[handler])

		self.log = logging.getLogger('console')

	def menu(self, prompt: str, variants: list, title: str) -> str:
		"""
		Печатает меню и текст, который предлагает пользователю сделать выбор.

		Аргументы:
			prompt (str): Текст, который предлагает пользователю сделать выбор.
			variants (list): Список вариантов выбора.
			title (str): Заголовок панели меню.

		Возвращается:
			str: Вариант, который выбрал пользователь.
		"""
		text_menu = f'\n{'\n'.join(f'[{num}] {j}' for num, j in enumerate(variants, 1))}\n'

		while True:
			self.clear_console()
			self.panel_print(text_menu, title)
			res = self.input(prompt)

			if res.isnumeric() and 1 <= int(res) <= len(variants):
				return res

	def panel_print(self, text: str, title: str, title_align: Literal['left', 'center', 'right'] = 'left',
					border_style: str = 'cyan') -> NoReturn:
		"""
		Печатает текст в панели.

		Аргументы:
			text (str): Текст внутри панели.
			title (str): Заголовок панели.
			title_align (Literal['left', 'center', 'right'], optional): Расположение заголовка. По умолчанию 'left'.
			border_style (str, optional): Цвет обводки. По умолчанию 'cyan'.
		"""
		self.console.print(Panel(text, title=title, title_align=title_align, border_style=border_style))

	def title(self, text: str, clear: bool = True) -> NoReturn:
		"""
		Печатает заголовок, в котором обычно находится справочная информация.

		Аргументы:
			text (str): Текст заголовка
			clear (bool, optional): Если True очищает консоль перед выводом. По умолчанию True.
		"""
		if clear:
			self.clear_console()

		self.console.print(text, justify='center')

	def print_tree_skills(self, skills: dict[SkillType: float], minus: bool = False) -> NoReturn:
		"""
		Печатает дерево наград для навыков.

		Аргументы:
			skills (dict[str: float]): Ключ — навык, значение — опыт прибавляемый к этому навыку.
			minus (bool, optional): Если True, то значения выводятся со знаком минус. По умолчанию False.
		"""
		tree = Tree('\n[magenta]Навыки:', guide_style='dim magenta')

		c = '[red]-' if minus else '[green]+'

		for skill, exp in skills.items():
			skill = skill if isinstance(skill, SkillType) else skill.skill_type
			tree.add(f'[magenta]{SkillType.description(skill)} {c}{round(exp, 2)}')

		if skills:
			self.console.print(tree)

	def print_task_tree(self, hide_root: bool = True):
		user_tasks = self.interface.task_manager.tasks
		daily_tasks_manager = self.interface.daily_tasks_manager
		quests = self.interface.quest_manager.active_quests

		tree = Tree('Задания', hide_root=hide_root)

		# Пользовательские задания #
		if not user_tasks:
			tree.add('[b green]Пользовательские задания[/]\nВы не добавили задания\n')
		else:
			branch_user_tasks = tree.add(f'[b green]Пользовательские задания')

			for i, task in enumerate(user_tasks, 1):
				end = '\n' if len(user_tasks) == i else ''
				branch_user_tasks.add(str(task) + end)

		# Ежедневные задания #
		if not daily_tasks_manager.daily_tasks:
			tree.add('[b yellow]Ежедневные задания[/]\nВы не добавили задания\n')
		else:
			c = '[green]x[/]' if daily_tasks_manager.done else ' '
			branch_user_tasks = tree.add(f'[{c}] [b yellow]Ежедневные задания')

			for i, task in enumerate(daily_tasks_manager.daily_tasks, 1):
				end = '\n' if len(daily_tasks_manager.daily_tasks) == i else ''
				branch_user_tasks.add(str(task) + end)

		# Квесты #
		if not quests:
			tree.add(f'[b red]Квесты[/]\nВозьмите квест в гильдии')

		for active in quests:
			c = 'green' if active.done else 'red'

			quest_tree = tree.add(
				f"[{c} b]{active.quest.name} [white b]{len(active.done_stages)}/{len(active.quest.stages)}\n"
				f"{active.quest.description}"
			)

			for sid in active.done_stages:
				stage = active.quest.stages[sid]
				quest_tree.add(f'[[green]x[/]] [green]{stage.name}')

			if active.done:
				continue

			stage_tree = quest_tree.add(f"[ ] [green]{active.stage.name}")
			for goal in active.goals:
				mark = '[green]x[/]' if goal.completed else ' '

				if isinstance(goal, BossFight):
					# goal.add_damage(3)
					stage_tree.add(
						f'[{mark}] [blue]{goal.name}[/]\n'
						f'HP: {self.create_progress_bar(goal.hp - goal.damage, goal.hp, 'red')}'
					)
				else:
					# mark = '[green]x[/]' if goal.completed else ' '
					stage_tree.add(
						f'[{mark}] [blue]{goal.task}\n'
						f'[yellow]{goal.description}'
					)

		self.console.print(tree)

	def print_all_task(self) -> tuple[int, int, int]:
		""" Печатает все задания с номерами. """
		user_tasks_count = self.print_user_tasks()
		daily_tasks_count = self.print_daily_tasks(user_tasks_count)
		quests_count = self.print_quests(daily_tasks_count)

		return user_tasks_count, daily_tasks_count, quests_count

	def print_user_tasks(self, count: int = 1) -> int:
		"""
		Печатает пользовательские задания с номерами.

		Аргументы:
			count (int): Число, с которого номера заданий будут брать отсчёт. По умолчанию 1.
		"""
		user_tasks = self.interface.task_manager.tasks

		self.console.print('[green]Пользовательские задания')

		if not user_tasks:
			self.console.print('Вы не добавили задания')
		else:
			for task in user_tasks:
				self.console.print(f"[white]({count}) " + str(task))
				count += 1

		print()
		return count

	def print_daily_tasks(self, count: int) -> int:
		"""
		Печатает ежедневные задания с номерами.

		Аргументы:
			count (int): Число, с которого номера заданий будут брать отсчёт. По умолчанию 1.
		"""
		daily_tasks = self.interface.daily_tasks_manager.daily_tasks

		self.console.print('[yellow]Ежедневные задания')

		if not daily_tasks:
			self.console.print('Вы не добавили задания')
		else:
			for task in daily_tasks:
				self.console.print(f"[white]({count}) " + str(task))
				count += 1

		print()
		return count

	def print_quests(self, count: int) -> int:
		"""
		Печатает квесты.

		Аргументы:
			count (int): Число, с которого номера заданий будут брать отсчёт. По умолчанию 1.
		"""
		active_quests = self.interface.quest_manager.active_quests

		if len(active_quests) == 0:
			self.console.print('[b red]Квесты[/]\nВозьмите квест в гильдии')
			return count

		for active in active_quests:
			c = "green" if active.done else "red"
			tree = Tree(
				f"[{c} b]{active.quest.name} [white b]{len(active.done_stages)}/{len(active.quest.stages)}\n"
				f"{active.quest.description}"
			)

			for sid in active.done_stages:
				stage = active.quest.stages[sid]
				tree.add(f"[white][[green]x[white]] [green]{stage.name}")

			if active.done:
				continue

			stage_tree = tree.add(f"[white][ ] [green]{active.stage.name}")
			for goal in active.goals:
				mark = "x" if goal.completed else " "

				if isinstance(goal, BossFight):
					stage_tree.add(
						f'[{mark}] [blue]{goal.name}[/]\n'
						f'HP: {self.create_progress_bar(goal.hp - goal.damage, goal.hp, 'red')}'
					)
				else:
					stage_tree.add(
						f"[white]({count}) [[green]{mark}[white]] [blue]{goal.task}\n"
						f"[yellow]{goal.description}"
					)
					count += 1

		self.console.print(tree)
		return count

	def print_item_tree(self, items: list[Item]) -> NoReturn:
		"""
		Печатает красивое представление найденных предметов.

		Аргументы:
			items (list[Item]): Предметы, которые надо напечатать.
		"""
		tree = Tree('\n[bold cyan]Вы нашли предметы:')

		for item in items:
			tree.add(f'{item.name}')

		if items:
			self.console.print(tree)

	def print_shop_quest(self, quests: list[Quest]):
		"""
		Печатает магазин квестов.

		Аргументы:
			quests (list[Quest]): Список квестов, которые будут в магазине.
		"""
		table = Table(box=box.SIMPLE)

		table.add_column('№')
		table.add_column('Квест', style='magenta')
		table.add_column('Ранг', style='cyan', justify='center')
		table.add_column('Описание', style='green', min_width=25)
		table.add_column('Награда', style='yellow')

		for count, quest in enumerate(quests, 1):
			items = quest.reward['items']

			description_sup = '[d]' if count % 2 == 0 else ''
			sup_str = 'предмета' if len(items) > 1 else 'предмет'
			reward_str = f', {len(items)} {sup_str}' if items else ''

			table.add_row(
				str(count),
				quest.name,
				RankType.description(quest.rank),
				description_sup + quest.description,
				f'{quest.reward['gold']}G' + reward_str
			)

		self.console.print(table)

	def print_shop(self, items: list[Item]):
		"""
		Печатает магазин предмет.

		Аргументы:
			items (list[Item]): Список предметов, которые будут в магазине.
		"""
		table = Table(box=box.SIMPLE)

		table.add_column('№')
		table.add_column('Предмет', style='magenta')
		table.add_column('Описание', style='green', min_width=25)
		table.add_column('Цена', justify='right', style='yellow')

		for count, item in enumerate(items, 1):
			description_sup = '[d]' if count % 2 == 0 else ''
			table.add_row(
				str(count),
				item.name,
				description_sup + item.description.capitalize(),
				str(item.cost)
			)

		self.console.print(table)

	def print_skill_shop(self, gold: float, skills: list[Skill]):
		"""
		Печатает магазин навыков.

		Аргументы:
			gold (float): Текущее количество денег у пользователя.
			skills (list[Skill]): Список навыков, которые надо напечатать.
		"""
		table = Table(box=box.SIMPLE)

		table.add_column('№')
		table.add_column('Навык', style='magenta')
		table.add_column('Уровень', style='cyan', justify='center')
		table.add_column('Мин. опыт', style='red', justify='right')
		table.add_column('Стоимость', style='yellow', justify='center')

		for count, skill in enumerate(skills, 1):
			level, exp = skill.level, skill.exp

			demand_exp, demand_gold = self.interface.awards_manager.get_price_skill(level)

			if exp >= demand_exp and gold >= demand_gold:
				table.add_row(
					str(count),
					SkillType.description(skill.skill_type),
					str(level),
					f'[green]{demand_exp} ({round(exp, 2)})',
					str(demand_gold)
				)
			else:  # Поскольку пользователь не может купить улучшение оно затемнено
				table.add_row(
					str(count),
					f'[d]{SkillType.description(skill.skill_type)}',
					f'[d]{level}',
					f'[d]{demand_exp} ({round(exp, 2)})',
					f'[d]{demand_gold}'
				)
			count += 1

		self.console.print(table)

	def presence_item(self, item: Item):
		"""
		Отображает информацию о предмете.

		Аргументы:
			item (Item): Предмет информацию, о котором надо вывести.
		"""

		def get_effects_string(effects: dict[str | int, float]) -> str:
			if not effects or len(effects) == 1 and effects.get('text') is not None:
				return "[b red]Эффектов нет[/]\n"

			effects_str = "[b red]Эффекты[/]:\n"
			for key, value in effects.items():
				if key == 'text': continue

				if key == 'quest':
					quest = self.interface.quest_manager.get_quest(value)
					effects_str += f'    Запускает квест: [green]{quest.text.lower()}[/]\n'
				elif key == 'textbook':
					effects_str += f'   Прокачивает навыки персонажа.\n'
				elif value > 1:
					effects_str += f'    {SkillType.description(key)}: [green]+{round(value * 100 - 100)}%[/]\n'
				else:
					effects_str += f'    {SkillType.description(key)}: [red]{round(value * 100 - 100)}%[/]\n'
			return effects_str

		item_type_info = f'[b green]Тип[/]: {ItemType.description(item.type)}\n'
		effects_info = get_effects_string(item.effects)
		cost_info = (
			f'[b yellow]Цена покупки[/]: {item.cost}\n'
			if item.cost > 0
			else '[b yellow]Не продается[/]\n'
		)
		sell_info = (
			f'[b yellow]Цена продажи[/]: {item.sell}'
			if item.sell > 0
			else '[b yellow]Ничего не стоит[/]'
		)

		result = f'[purple b]{item.name}[/] - [white]{item.description}[/]\n'
		result += item_type_info
		result += effects_info
		result += cost_info
		result += sell_info
		self.console.print(result)

	@staticmethod
	def show_item(slot: Slot, show_amount=True) -> str:
		"""
		Генерирует строковое представление предмета в заданном слоте.

		Аргументы:
			slot (Slot): Ячейка, содержащая элемент.
			show_amount (bool, optional): Следует ли отображать количество товара. По умолчанию True.

		Возвращает:
			str: Сгенерированное строковое представление предмета.
		"""
		if slot.empty:
			return "[yellow]-[/] "

		item = get_item(slot.id)
		text = ""
		if show_amount:
			text += f"[white]{slot.amount}x"
		text += f"[green]{item.name}[/] "

		return text

	def show_inventory(self,
					   show_number: bool = True,
					   show_amount: bool = False,
					   allow: Optional[list[ItemType]] = None,
					   inverse: bool = False,
					   ):
		"""
		Отображает инвентарь игрока.

		Аргументы:
			show_number (bool, optional): Следует ли отображать номера для каждого элемента. По умолчанию True.
			show_amount (bool, optional): Следует ли отображать количество каждого товара. По умолчанию False.
			allow (list[ItemType], optional): Список разрешенных для отображения типов элементов. По умолчанию None.
			inverse (bool, optional): Отображать ли элементы, которых нет в списке разрешенных. По умолчанию False.
		"""
		inventory = self.interface.inventory

		grouped_slots = groupby(inventory.slots, lambda i: i.type)
		counter = 1
		for slot_type, slots in grouped_slots:
			if allow:
				if not inverse and slot_type not in allow:
					continue
				if inverse and slot_type in allow:
					continue

			self.console.print("[yellow b]" + ItemType.description(slot_type), end=" ")
			for slot in slots:
				if show_number:
					self.console.print(f"[blue]\\[{counter}][/]", end="")
					counter += 1
				self.console.print(self.show_item(slot, show_amount), end="")
			self.console.print()

	@staticmethod
	def create_progress_bar(value: int, maximum: int, color: str = 'green', width: int = 26, suffix: bool = True):
		"""
		Создаёт индикатор выполнения.

		Аргументы:
			value (int): Значение индикатора выполнения.
			maximum (int): Максимальное значение индикатора выполнения.
			color (str): Цвет индикатора. По умолчанию green.
			width (int): Длина индикатора. По умолчанию 26.
			suffix (bool): Добавить ли текущее значение и максимальное значение.
		"""
		sym_len = int(value / maximum * width) if maximum else 0
		suffix = f' {value}/{maximum}' if suffix else ''
		return f'[[{color}]{'|' * sym_len}{' ' * (width - sym_len)}[/]]{suffix}'

	def input(self, *args, **kwargs) -> Any:
		""" Запрашивает ввод пользователя. """
		return self.console.input(*args, **kwargs)

	def print(self, *args, **kwargs) -> NoReturn:
		""" Выводит заданные аргументы. """
		self.console.print(*args, **kwargs, highlight=False)

	@staticmethod
	def clear_console() -> NoReturn:
		""" Очищает консоль. """
		os.system('cls')
