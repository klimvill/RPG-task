import random
import re
import sys
from datetime import date

from .awards import AwardsManager
from .console import AppConsole
from .content import all_daily_tasks, all_quest, all_quest_items
from .daily_tasks import DailyTaskManager
from .data.config import NUMBER_DAILY_TASKS
from .database import all_save, read_tasks, read_player_info, read_inventory
from .inventory import Inventory, ItemType
from .player import Player, SKILL_DESCRIPTIONS
from .quests import QuestManager
from .tasks import TaskManager
from .utils import skill_check, get_item


class Interface:
	"""
	Основной класс приложения.

	Аргументы:
		console (AppConsole): Отвечает за весь вывод на экран.
		awards_manager (AwardsManager): Отвечает за выдачу наград и наказаний.

		player (Player): В этом классе хранится вся информация о деньгах и навыках.
		inventory (Inventory): Через этот класс будет происходить вся работа с инвентарём.

		task_manager (TaskManager): Отвечает за работу с пользовательскими заданиями.
		daily_tasks_manager (DailyTaskManager): Отвечает за работу с ежедневными заданиями.
		quest_manager (QuestManager): Отвечает за работу с квестами.

	Методы:
		main(): Основной цикл приложения.
		main_menu(): Основное меню игры.

		view_tasks(): Функция просмотра задания.
		add_tasks(): Функция добавления пользовательских заданий.
		mark_completion_tasks(): Функция отметки выполнения задач.
		delete_tasks(): Функция удаления заданий.
		quest_shop(): Магазин квестов.
		skill_shop(): Функция прокачки навыков.
		view_inventory(): Просмотр инвентаря.

		update(): Загрузка и обновление данных.
		save(): Сохранение данных.
	"""

	def __init__(self):
		self.console = AppConsole(self)
		self.awards_manager = AwardsManager(self)

		self.player = Player()
		self.inventory = Inventory()

		self.task_manager = TaskManager()
		self.daily_tasks_manager = DailyTaskManager()
		self.quest_manager = QuestManager()

		self.update()
		self.main()

	def main(self):
		""" Основной цикл приложения. """
		while True:
			try:
				self.main_menu()
			except Exception as e:
				self.console.log.exception(e)
				try:
					if input('Возникла ошибка. Перезагрузить? [Y/n]: ') == 'n':
						break
				except KeyboardInterrupt:
					break
			except KeyboardInterrupt:
				break
		self.save()

	def main_menu(self):
		""" Основное меню игры. """
		variants = [
			'Посмотреть задания',
			'Добавить задания',
			'Выполнить задания',
			'Удалить задание',
			'Лавка квестов',
			'Лавка навыков',
			'Инвентарь',
			'Выход',
		]
		command = self.console.menu('Введите команду: ', variants, 'Меню')

		if command == '1':
			self.view_tasks()
		elif command == '2':
			self.add_tasks()
		elif command == '3':
			self.mark_completion_tasks()
		elif command == '4':
			self.delete_tasks()
		elif command == '5':
			self.quest_shop()
		elif command == '6':
			self.skill_shop()
		elif command == '7':
			self.view_inventory()
		elif command == '8':
			self.save()
			sys.exit()

	def view_tasks(self):
		""" Функция просмотра задания. """
		self.console.title('Просмотр заданий, чтобы выйти нажмите enter')
		self.console.print_task_tree()
		self.console.input()

	def add_tasks(self):
		"""
		Функция добавления пользовательских заданий.

		Формат добавления заданий - "task1 [навык, навык, навык]"
		"""
		skills_name = SKILL_DESCRIPTIONS.values()
		self.console.title(f'Добавление заданий, чтобы выйти нажмите enter\n[dim]{", ".join(skills_name)}[/dim]')

		while (line := self.console.input('[bold cyan]Введите задание: [/bold cyan]')) != '':
			# Разделение задания на компоненты #
			task = re.sub(r'\[.*?]', '', line)
			task = re.sub(r'\(.*?\)', '', task).rstrip()
			skills = re.findall(r'\[([^]]*)]', line)

			# Определение навыков #
			skills_result = []
			if skills and skills[0] != '':
				skills = [i.strip() for i in skills[0].split(',')]
				skills_result = set([result for i in skills if (result := skill_check(i)) is not None])
				skills_result = list(skills_result)[:3]

			# Добавление задачи в список #
			self.task_manager.add_task(task, skills_result)

	def mark_completion_tasks(self):
		""" Функция отметки выполнения задач. """
		self.console.title('Отметить выполнение заданий, чтобы выйти нажмите enter')

		user_tasks_count, daily_tasks_count, quests_count = self.console.print_all_task()
		command = self.console.input('\n\nКакие задания вы выполнили: ')

		if command == '': return
		nums = set([int(i) for i in re.findall(r'\d+', command) if 0 < int(i) < quests_count])
		if not nums: return

		self.console.title('Награды, чтобы выйти нажмите enter')

		nums_user_tasks, nums_daily_tasks, nums_quests = [], [], []
		for num in nums:
			if num < user_tasks_count:
				task = self.task_manager.get_task(num - 1)
				nums_user_tasks.append(num)

			elif num < daily_tasks_count:
				num = num - user_tasks_count

				if self.daily_tasks_manager.done or self.daily_tasks_manager.active_daily_tasks[num].done:
					continue

				task = self.daily_tasks_manager.get_daily_tasks(num)
				nums_daily_tasks.append(num)

			elif num < quests_count:
				num = num - user_tasks_count - daily_tasks_count + 1

				task = self.quest_manager.active_quests[0].get_goal(num)
				nums_quests.append(num)

			self.console.print(f'- [green]{task.text}')

		# Пользовательские задания #
		gold, skills_exp, items = self.awards_manager.get_rewards_user_tasks(nums_user_tasks)
		if gold:
			self.console.print(f'\n[yellow]Золото: [green]+{round(gold, 2)}')
		if skills_exp:
			self.console.print_tree_skills('[magenta]Навыки:', skills_exp)
		if items:
			self.console.print_item_tree(items)

		for num in sorted(nums_user_tasks, reverse=True):
			self.task_manager.delete_task(num)

		# Ежедневные задания #
		for num in sorted(nums_daily_tasks, reverse=True):
			done = self.daily_tasks_manager.complete(num)

			if done:
				self.console.print('\n[dim]Вы выполнили все ежедневные задания, вот ваша награда:')

				gold_daily_tasks, skills_exp_daily_tasks, items_daily_tasks = self.awards_manager.get_rewards_daily_tasks()

				gold += gold_daily_tasks

				self.console.print(f'[yellow]Золото: [green]+{round(gold_daily_tasks, 2)}')
				self.console.print_tree_skills('[magenta]Навыки:', skills_exp_daily_tasks)

				if items_daily_tasks:
					self.console.print_item_tree(items_daily_tasks)
					items.extend(items_daily_tasks)

				for skill, exp in skills_exp_daily_tasks.items():
					if skill in skills_exp:
						skills_exp[skill] += exp
					else:
						skills_exp[skill] = exp

		# Квест #
		for num in sorted(nums_quests, reverse=True):
			self.quest_manager.complete_goal(num)

		active_quests = self.quest_manager.active_quests
		if active_quests and active_quests[0].done:
			self.console.print('\n[dim]Вы выполнили квест, вот ваша награда:')

			reward = active_quests[0].process_rewards()
			gold_quests, items_quests = reward['gold'], list(
				map(lambda identifier: get_item(identifier), reward['items']))

			gold += gold_quests

			self.console.print(f'[yellow]Золото: [green]+{round(gold_quests, 2)}')

			if items_quests:
				self.console.print_item_tree(items_quests)
				items.extend(items_quests)

			self.quest_manager.clear_active_quest()

		self.player.gold.add_money(gold)

		for skill, exp in skills_exp.items():
			self.player.skills[skill.skill_type].add_exp(exp)

		check = False
		for item in items:
			amount = self.inventory.take(item, 1)

			if amount > 0:
				if not check:
					check = True
					self.console.print(
						f'\n[red]В вашем инвентаре закончилось место, лишние предметы будут проданы автоматически.')

				self.console.print(f'- {item.name} [green]+{item.sell}')
				self.player.gold.add_money(item.sell)

		if len(nums_user_tasks + nums_daily_tasks + nums_quests) != 0:
			input()

	def delete_tasks(self):
		""" Функция удаления заданий. """
		user_tasks = self.task_manager.tasks

		self.console.title('Удаление заданий, чтобы выйти нажмите enter')
		# Поскольку мы не можем удалить ежедневные задания или квесты, то печатать их необязательно.
		self.console.print_user_tasks()
		command = self.console.input('\nКакие задания вы хотите удалить: ')

		if command == '': return
		nums = set([int(i) for i in re.findall(r'\d+', command) if 0 < int(i) <= len(user_tasks)])
		if not nums: return

		if self.console.input(
				'[red]Если вы удалите задачи, то потеряете накопленный опыт. Вы уверенны? [Y/n]: ') != 'Y':
			return

		# Вывод удалённых задач #
		self.console.title('Удалённые задачи, чтобы выйти нажмите enter')

		for num in nums:
			self.console.print(f'- [red]{self.task_manager.get_task(num).text}')

		gold, skills_exp, items = self.awards_manager.get_rewards_user_tasks(nums, False)

		self.console.print(f'\n[yellow]Золото: [red]-{round(gold, 2)}')

		if skills_exp:
			self.console.print_tree_skills('[magenta]Навыки:', skills_exp, minus=True)

		self.player.gold.payment(gold)
		for skill, exp in skills_exp.items():
			skill.reduce_exp(exp)

		# Удаление задач #
		for num in sorted(nums, reverse=True):
			self.task_manager.delete_task(num)

		input()

	def quest_shop(self):
		""" Магазин квестов. """
		self.console.title('Лавка предметов, чтобы выйти нажмите enter')

		self.console.print_shop_quest()

		command = self.console.input('\n\nКакие квесты вы хотите купить: ')

		if command == '': return
		nums = [int(i) for i in re.findall(r'\d+', command) if 0 < int(i) <= len(all_quest_items)]
		if not nums: return

		self.console.print()
		for num in nums:
			quest_item = all_quest_items[num - 1]

			if self.player.gold.gold >= quest_item.cost:
				amount = self.inventory.take(quest_item, 1)

				if amount > 0:
					self.console.print(
						f'[red]В вашем инвентаре закончилось место, квест "{quest_item.name}" не был куплен!')
				else:
					self.player.gold.payment(quest_item.cost)
					self.console.print(f'- [green]{quest_item.name}')

			else:
				self.console.print(f'[red]Вам не хватило денег на покупку квеста "{quest_item.name}"!')

		self.console.input()

	def skill_shop(self):
		""" Функция прокачки навыков. """
		while True:
			gold = self.player.gold.gold
			skills = self.player.skills

			self.console.title('Лавка навыков, чтобы выйти нажмите enter')
			self.console.print_table_price(gold, skills)
			self.console.print(f'[yellow]Золото: {round(gold, 2)}\n')

			command = self.console.input('Какие навыки хотите прокачать: ')

			if command == '': return
			nums = [int(i) for i in re.findall(r'\d+', command) if 0 < int(i) <= len(skills)]
			if not nums: return

			for num in nums:
				skill = skills[num - 1]
				level, exp = skill.level, skill.exp

				demand_exp, demand_gold = self.awards_manager.get_price_skill(level)

				if demand_exp > exp: continue
				if gold - demand_gold < 0: break

				self.player.gold.payment(demand_gold)
				skill.add_level()

	def view_inventory(self):
		""" Просмотр инвентаря. """
		while True:
			self.console.title('Инвентарь, чтобы выйти нажмите enter\n')
			self.console.show_inventory()
			slot = self.console.input('\nВведите номер слота для управления им: ')

			if slot == '': break
			if slot.isnumeric() and 0 < int(slot) <= len(self.inventory.slots):
				slot = self.inventory.slots[int(slot) - 1]
				self.console.clear_console()
			else:
				continue

			if not slot: break
			if slot.empty:
				self.console.print("Слот пуст!")
				self.console.input()
				continue

			item = get_item(slot.id)

			self.console.print(
				f"\n[bold green]Управление предметом: {self.console.show_item(slot, False)}[/]\n"
				"  [green]i[white] - информация[/]\n"
				"  [green]w[white] - надеть/снять[/]\n"
				"  [green]u[white] - использовать[/]\n"
				"  [green]s[white] - продать[/]\n"
				"  [green]e[white] - отмена[/]"
			)
			command = self.console.input('Что вы хотите сделать с предметом: ')

			if command == "i":
				self.console.print()
				self.console.presence_item(item)

			elif command == "w":
				if slot.type == ItemType.ITEM and item.type != ItemType.ITEM:
					slots = self.inventory.get(item.type, only_empty=True)
					if slots:
						slots[0][1].swap(slot)
						self.console.print("[green]Предмет надет[/]")
					else:
						self.console.print("[red]Нет доступных слотов[/]")
				elif slot.type != ItemType.ITEM:
					slots = self.inventory.get(ItemType.ITEM, only_empty=True)
					if slots:
						slots[0][1].swap(slot)
						self.console.print("[green]Предмет снят[/]")
					else:
						self.console.print("[red]Нет доступных слотов[/]")
				elif slot.type == ItemType.ITEM and item.type == ItemType.ITEM:
					self.console.print("[red]Вы не можете это надеть")

			elif command == "u":
				if item.is_usable and not item.is_wearable:
					if item.effects.get('quest') is not None and not self.quest_manager.quest_been_launched(
							item.effects.get('quest')):
						self.quest_manager.start_quest(item.effects.get('quest'))

						self.console.print('[green]Квест успешно активирован!')

						slot.amount -= 1
					else:
						self.console.print('[red]Вы не выполнили предыдущий квест!')
				else:
					self.console.print("[red]Вы не можете это использовать")

			elif command == "s":
				if item.possible_sell:
					self.player.gold.add_money(item.sell)
					slot.clear()
					self.console.print(f"[green]Предмет успешно продан за {item.sell} монеты[/]")
				else:
					self.console.print("[red]Вы не можете это продать")

			elif command == "e":
				continue

			input()

	def update(self):
		""" Загрузка и обновление данных. """
		tasks = read_tasks()
		player_info = read_player_info()
		inventory = read_inventory()

		self.task_manager.load(tasks['user_tasks'])

		self.quest_manager.quests.extend(all_quest)
		self.quest_manager.load(tasks['quests'])

		self.player.load(player_info)
		self.inventory.load(inventory)

		self.daily_tasks_manager.daily_tasks.update(all_daily_tasks)
		self.daily_tasks_manager.load(tasks['daily_tasks'])

		# Проверяем, что ежедневное задание актуально.
		today = str(date.today())
		if self.daily_tasks_manager.date != today:
			complete = self.daily_tasks_manager.update(
				random.sample(list(all_daily_tasks.values()), NUMBER_DAILY_TASKS), today)

			# Если предыдущие задания не были выполнены, то наказываем игрока за это.
			if not complete:
				self.console.title('Наказание за невыполнение заданий, чтобы выйти нажмите enter')
				self.console.print('[dim]Вы не закончили предыдущее ежедневное задание:')

				gold, skills_exp, items = self.awards_manager.get_rewards_daily_tasks(need_items=False)

				self.console.print(f'[yellow]Золото: [red]-{round(gold, 2)}')
				self.console.print_tree_skills('[magenta]Навыки:', skills_exp, minus=True)

				self.player.gold.payment(gold)
				for skill, exp in skills_exp.items():
					skill.reduce_exp(exp)

				self.console.input()

	def save(self):
		""" Сохранение данных. """
		all_save(
			{
				'user_tasks': self.task_manager.save(),
				'daily_tasks': self.daily_tasks_manager.save(),
				'quests': self.quest_manager.save()
			},
			self.player.save(),
			self.inventory.save()
		)
