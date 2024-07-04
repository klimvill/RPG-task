import re
import sys

from .console import GameConsole
from .database import read_tasks, read_hero_info, all_save
from .utils import skill_check, receiving_awards, get_task_text
from .config import *


class Interface:
	tasks = read_tasks()
	hero_info = read_hero_info()

	def __init__(self):
		self.console = GameConsole()

		self.main()

	def main(self):
		while True:
			try:
				self.main_menu()
			except Exception as e:
				# todo: Добавить логирование
				try:
					print(e)
					if input('Возникла ошибка. Перезагрузить? [Y/n]: ') == 'n':
						all_save(self.tasks, self.hero_info)
						break
				except KeyboardInterrupt:
					all_save(self.tasks, self.hero_info)
					break
			except KeyboardInterrupt:
				all_save(self.tasks, self.hero_info)
				break

	def main_menu(self):
		variants = [
			'Посмотреть задания',
			'Добавить задания',
			'Выполнить задания',
			'Удалить задание',
			'Характеристики',
			'Лавка навыков',
			'Магазин предметов',
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
			self.item_store()
		elif command == '8':
			all_save(self.tasks, self.hero_info)
			sys.exit()

	def view_tasks(self):
		self.console.title('Просмотр заданий, чтобы выйти нажмите enter')

		user_tasks = self.tasks['user_tasks']
		daily_tasks = self.tasks['daily_tasks']
		quests = self.tasks['quests']

		self.console.print_task_tree(user_tasks, daily_tasks, quests)

	def add_tasks(self):
		"""
		Формат добавления заданий - task1 [навыки] (время конца задания)
		:return:
		"""
		_ = list(self.hero_info['skills'].keys())
		self.console.title(f'Добавление заданий, чтобы выйти нажмите enter\n[dim]{", ".join(_).title()}[/dim]')

		while (line := self.console.input('[bold cyan]Введите задание: [/bold cyan]')) != '':
			# Разделение задания на компоненты #
			task = re.sub(r'\[.*?]', '', line)
			task = re.sub(r'\(.*?\)', '', task).rstrip()

			skills = re.findall(r'\[([^]]*)]', line)
			time = re.findall(r'\(([^]]*)\)', line)

			if time == 'today': ...  # datatime.datatime()
			elif time == 'tomorrow': ...
			elif time == 'рандомная дата в формате дд.мм.гггг': ...

			# Определение навыков #
			skills_result = []
			if skills and skills[0] != '':
				skills = [i.strip() for i in skills[0].split(',')]
				skills_result = set([result for i in skills if (result := skill_check(i, self.hero_info)) is not None])

			# Добавление задачи в список #
			if skills_result and (time and time[0] != ''):
				self.tasks['user_tasks'].append([task, skills_result, time[0]])
			elif skills_result:
				self.tasks['user_tasks'].append([task, skills_result, None])
			elif time and time[0] != '':
				self.tasks['user_tasks'].append([task, None, time[0]])
			else:
				self.tasks['user_tasks'].append([task, None, None])

	def mark_completion_tasks(self):
		user_tasks = self.tasks['user_tasks']
		daily_tasks = self.tasks['daily_tasks']
		quests = self.tasks['quests']

		count = len(user_tasks) + len(daily_tasks) + len(quests)

		self.console.title('Отметить выполнение заданий, чтобы выйти нажмите enter')
		self.console.print_all_task(user_tasks, daily_tasks, quests)
		command = self.console.input('Какие задания вы выполнили: ')

		if command == '': return
		nums = [int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= count]
		if not nums: return

		# Выдача наград #
		self.console.title('Награды, чтобы выйти нажмите enter')
		data = receiving_awards(nums, self.tasks, self.hero_info)

		for num in set(nums):
			self.console.print(f'- [green]{get_task_text(num, self.tasks)}[/green]')

		self.console.print(f'\n[yellow]Золото: [green]+{round(data[0], 2)}[/green][/yellow]')
		if data[1]: self.console.print_tree_skills('[magenta]Навыки:[/magenta]', data[1])

		# Сохранение #
		self.hero_info['money'] += data[0]

		for num in sorted(set(nums), reverse=True):
			del self.tasks['user_tasks'][num - 1]

		for key, value in data[1].items():
			self.hero_info['skills'][key][1] += value

		input()

	def delete_tasks(self):
		user_tasks = self.tasks['user_tasks']
		daily_tasks = self.tasks['daily_tasks']
		quests = self.tasks['quests']
		count = len(user_tasks) + len(daily_tasks) + len(quests)

		self.console.title('Удаление заданий, чтобы выйти нажмите enter')
		self.console.print_all_task(user_tasks, daily_tasks, quests)
		command = self.console.input('Какие задания вы выполнили: ')

		if command == '': return
		nums = [int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= count]
		if not nums: return

		# todo: Сделать наказание за удаление задач
		# Вывод удалённых задач #
		self.console.title('Удалённые задачи, чтобы выйти нажмите enter')

		for num in nums:
			self.console.print(f'- [red]{get_task_text(num, self.tasks)}[/red]')

		# Удаление задач #
		for num in sorted(nums, reverse=True):
			del self.tasks['user_tasks'][num - 1]

		input()

	def characteristics(self):
		gold = self.hero_info['money']
		skills = self.hero_info['skills']

		self.console.title('Характеристики персонажа, чтобы выйти нажмите enter')
		self.console.print_table_characteristics(skills)
		self.console.print(f'[yellow]Золото: {round(gold, 2)}[/yellow]')

		input()

	def skill_shop(self):
		while True:
			gold = float(self.hero_info['money'])
			skills = self.hero_info['skills']

			self.console.title('Лавка навыков, чтобы выйти нажмите enter')
			data = self.console.print_table_price(skills, self.hero_info)
			self.console.print(f'[yellow]Золото: {round(gold, 2)}[/yellow]\n')

			command = self.console.input('Какие навыки хотите прокачать: ')
			if command == '': return
			nums = [int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= len(skills)]
			if not nums: return

			for num in nums:
				skill = data[num - 1]
				skill_lvl = skills[skill][0]
				skill_exp = skills[skill][1]
				demand_exp = CONSTANT_SKILL * skill_lvl ** MULTIPLIER_SKILL
				demand_gold = CONSTANT_GOLD * skill_lvl ** MULTIPLIER_GOLD

				if skill_lvl == 0:
					demand_exp, demand_gold = 0.25, 0.1
				elif skill_lvl == 1:
					demand_exp, demand_gold = 0.5, 0.25

				if demand_exp > skill_exp: continue
				if gold - demand_gold < 0: break
				gold = gold - demand_gold
				self.hero_info['skills'][skill][0] += 1

			self.hero_info['money'] = gold


	def item_store(self):
		self.console.title('Магазин предметов, чтобы выйти нажмите enter')



		input()

