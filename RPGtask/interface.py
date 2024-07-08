import random
import re
import sys
from datetime import date

from .awards import AwardsManager
from .console import MyConsole
from .database import read_tasks, read_hero_info, get_information_about_task, all_save, get_task_text, read_inventory
from .inventory import Inventory, Item
from .utils import skill_check, get_item, calculate
from .data.daily_tasks import options_daily_tasks
from .data.items import *


class Interface:
	def __init__(self):
		self.console = MyConsole(self)
		self.inventory = Inventory()
		self.awards = AwardsManager(self.inventory)

		self.tasks: dict[str, list | dict] = read_tasks()
		self.hero_info: dict[str: int, str: list[int, int]] = read_hero_info()

		self.update()
		self.main()

	def main(self):
		while True:
			try:
				# self.inventory.take(shabby_hood, 1)
				# self.inventory.take(wooden_circlet, 1)
				self.main_menu()


			except KeyboardInterrupt:
				all_save(self.tasks, self.hero_info, self.inventory.save())
				break

	def main_menu(self):
		variants = [
			'Посмотреть задания',
			'Добавить задания',
			'Выполнить задания',
			'Удалить задание',
			'Характеристики',
			'Лавка навыков',
			'Инвентарь',
			'Выход'
		]

		command = self.console.menu('Введите команду', variants, 'Меню')

		if command == '1':
			self.view_tasks()
		elif command == '2':
			self.add_tasks()
		elif command == '3':
			self.mark_completion_tasks()
		elif command == '4':
			self.delete_tasks()
		elif command == '5':
			self.characteristics()
		elif command == '6':
			self.skill_shop()
		elif command == '7':
			self.view_inventory()
		elif command == '8':
			all_save(self.tasks, self.hero_info, self.inventory.save())
			sys.exit()

	def view_tasks(self):
		self.console.title('Просмотр заданий, чтобы выйти нажмите enter')
		self.console.print_task_tree()

	def add_tasks(self):
		"""
		Формат добавления заданий - task1 [навыки] (тип)
		"""
		_ = list(self.hero_info['skills'].keys())
		self.console.title(f'Добавление заданий, чтобы выйти нажмите enter\n[dim]{", ".join(_).title()}[/dim]')

		while (line := self.console.input('[bold cyan]Введите задание: [/bold cyan]')) != '':
			# Разделение задания на компоненты #
			task = re.sub(r'\[.*?]', '', line)
			task = re.sub(r'\(.*?\)', '', task).rstrip()
			skills = re.findall(r'\[([^]]*)]', line)

			# Определение навыков #
			skills_result = []
			if skills and skills[0] != '':
				skills = [i.strip() for i in skills[0].split(',')]
				skills_result = set([result for i in skills if (result := skill_check(i, self.hero_info)) is not None])
				skills_result = list(skills_result)[:3]

			# Добавление задачи в список #
			if skills_result:
				self.tasks['user_tasks'].append([task, skills_result])
			else:
				self.tasks['user_tasks'].append([task, None])

	def mark_completion_tasks(self):
		user_tasks = self.tasks['user_tasks']
		daily_tasks = self.tasks['daily_tasks']['tasks']
		quests = self.tasks['quests']

		count = len(user_tasks) + len(daily_tasks) + len(quests)

		# Отметка выполненных заданий #
		self.console.title('Отметить выполнение заданий, чтобы выйти нажмите enter')
		self.console.print_all_task()
		command = self.console.input('Какие задания вы выполнили: ')

		if command == '': return
		nums = set([int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= count])
		if not nums: return

		# Выдача наград #
		gold, skills_, items_ = self.awards.get_rewards_user_tasks(nums, self.tasks, self.hero_info['skills'])

		if [gold, skills_, items_] != [0, {}, '']:
			self.console.title('Награды, чтобы выйти нажмите enter')

			for num in nums:
				task_info = get_information_about_task(num, self.tasks)
				if task_info is None: continue
				where = task_info[0]
				text = task_info[1]

				if where == 'daily_tasks' and daily_tasks[num - len(user_tasks) - 1][2]: continue
				self.console.print(f'- [green]{text}')

			if gold:
				self.console.print(f'\n[yellow]Золото: [green]+{round(gold, 2)}')
			if skills_:
				self.console.print_tree_skills('[magenta]Навыки:', skills_)
			if items_:
				self.console.print_item_tree(items_)

		# Сохранение #
		self.hero_info['money'] += gold

		for num in sorted(nums, reverse=True):
			if (task_info := get_information_about_task(num, self.tasks)) is None: continue
			where, text, skills = task_info

			if where == 'user_tasks':
				del user_tasks[num - 1]

			elif where == 'daily_tasks':
				done = self.tasks['daily_tasks']['done']
				daily_tasks[num - len(user_tasks) - 1][2] = True

				# Если все подзадачи выполнены, а награды не выданы
				if all((daily_tasks[i][2] for i in range(len(daily_tasks)))) and not done:
					self.tasks['daily_tasks']['done'] = True

					self.console.print('\n[dim]Вы выполнили все ежедневные задания, вот ваша награда:')
					gold, skills, items = self.awards.get_rewards_daily_tasks(daily_tasks, self.hero_info['skills'])

					self.hero_info['money'] += gold
					self.console.print(f'[yellow]Золото: [green]+{round(gold, 2)}')
					self.console.print_tree_skills('[magenta]Навыки:', skills)
					if items:
						self.console.print_item_tree(items)
						items_.extend(items)

					for skill, exp in skills.items():
						if skill in skills_:
							skills_[skill] += exp
						else:
							skills_[skill] = exp


		for skill, exp in skills_.items():
			self.hero_info['skills'][skill][1] += exp

		_ = False
		for item in items_:
			amount = self.inventory.take(item, 1)

			if amount > 0:
				if not _:
					_ = True
					self.console.print(f'\n[red]В вашем инвентаре закончилось место, лишние предметы будут проданы автоматически.')
				self.console.print(f'- {item.name} [green]+{item.sell}')
				self.hero_info['money'] += item.sell

		input()

	def delete_tasks(self):
		# Поскольку мы не можем удалить ежедневные задания или квесты, то печатать их необязательно.
		user_tasks = self.tasks['user_tasks']

		self.console.title('Удаление заданий, чтобы выйти нажмите enter')
		self.console.print_user_tasks()
		command = self.console.input('\nКакие задания вы хотите удалить: ')

		if command == '': return
		nums = [int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= len(user_tasks)]
		if not nums: return

		# todo: Сделать наказание за удаление задач
		# Вывод удалённых задач #
		self.console.title('Удалённые задачи, чтобы выйти нажмите enter')

		for num in nums:
			self.console.print(f'- [red]{get_task_text(num, self.tasks)}')

		# Удаление задач #
		for num in sorted(nums, reverse=True):
			del user_tasks[num - 1]

		input()

	def characteristics(self):
		gold = self.hero_info['money']
		skills = self.hero_info['skills']

		self.console.title('Характеристики персонажа, чтобы выйти нажмите enter')
		self.console.print_table_characteristics(skills)
		self.console.print(f'[yellow]Золото: {round(gold, 2)}')

		input()

	def skill_shop(self):
		while True:
			gold = float(self.hero_info['money'])
			skills = self.hero_info['skills']

			self.console.title('Лавка навыков, чтобы выйти нажмите enter')
			self.console.print_table_price()
			self.console.print(f'[yellow]Золото: {round(gold, 2)}\n')

			command = self.console.input('Какие навыки хотите прокачать: ')

			if command == '': return
			nums = [int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= len(skills)]
			if not nums: return

			for num in nums:
				# todo: Делаю два раза то, что достаточно сделать единожды (self.console.print_table_price())

				skill = list(skills.keys())[num - 1]
				skill_lvl, skill_exp = skills[skill]

				demand_exp, demand_gold = self.awards.get_price_skill(skill_lvl)

				if skill_lvl == 0:
					demand_exp, demand_gold = 0.25, 0.1
				elif skill_lvl == 1:
					demand_exp, demand_gold = 0.5, 0.25

				if demand_exp > skill_exp: continue
				if gold - demand_gold < 0: break

				gold = gold - demand_gold
				skills[skill][0] += 1

			self.hero_info['money'] = gold

	def view_inventory(self):
		while True:
			self.console.title('Инвентарь, чтобы выйти нажмите enter\n')
			self.console.show_inventory()
			slot_ = self.console.input('\nВведите номер слота для управления им: ')

			if slot_ == '': break

			if slot_.isnumeric() and 0 < int(slot_) <= len(self.inventory.slots):
				slot = self.inventory.slots[int(slot_) - 1]
				self.console.clear_console()
			else:
				continue
			# slot = self.console.menu('Введите номер слота для управления им: ', self.inventory.slots, '2')

			if not slot:
				break
			if slot.empty:
				self.console.print("Слот пуст!")
				input()
				continue
			print()
			self.console.print(
				f"[bold green]Управление предметом: {self.console.show_item(slot, False)}[/]\n"
				"  [green]i[white] - информация[/]\n"
				"  [green]w[white] - надеть/снять[/]\n"
				"  [green]u[white] - использовать[/]\n"
				"  [green]s[white] - продать[/]\n"
				"  [green]e[white] - отмена[/]"
			)
			item = get_item(slot.id)
			command = self.console.input('Что вы хотите сделать с предметом: ')

			if command == "e":
				continue
			if command == "i":
				print()
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
					# todo: Применение эффектов
					# game.player.apply(item)
					slot.amount -= 1
				else:
					self.console.print("[red]Вы не можете это использовать")
			elif command == "s":
				if item.possible_sell:
					self.hero_info['money'] += item.sell
					slot.clear()
					self.console.print(f"[green]Предмет успешно продан за {item.sell} монеты[/]")
				else:
					self.console.print("[red]Вы не можете это продать")
			input()



	def update(self):
		# Выдача ежедневных заданий #
		daily_tasks = self.tasks['daily_tasks']['tasks']
		date_task = self.tasks['daily_tasks']['date']
		today = str(date.today())

		if date_task == '' or date_task != today:
			self.tasks['daily_tasks']['date'] = today
			self.tasks['daily_tasks']['done'] = False
			# todo: Выдача дневных задач

			tasks = random.sample(options_daily_tasks, len(daily_tasks))

			for i, j in enumerate(tasks):
				self.tasks['daily_tasks']['tasks'][i] = j

		# Загрузка инвентаря #
		self.inventory.load(read_inventory())
