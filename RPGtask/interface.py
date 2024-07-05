import random
import re
import sys
from datetime import date

from .config import *
from .console import GameConsole
from .data.daily_tasks import *
from .database import read_tasks, read_hero_info, all_save, get_task_text, get_information_about_task
from .utils import skill_check, receiving_awards, get_rewards_daily_tasks


class Interface:
	tasks = read_tasks()
	hero_info = read_hero_info()

	def __init__(self):
		self.console = GameConsole()

		self.update()
		self.main()

	def main(self):
		while True:
			try:
				self.main_menu()
				# todo: Вернуть except

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
		self.console.print_all_task(user_tasks, daily_tasks, quests)
		command = self.console.input('Какие задания вы выполнили: ')

		if command == '': return
		nums = set([int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= count])
		if not nums: return


		# Выдача наград #
		gold, skills_, items = receiving_awards(nums, self.tasks, self.hero_info)

		if [gold, skills_, items] != [0, {}, []]:
			self.console.title('Награды, чтобы выйти нажмите enter')

			for num in nums:
				task_info = get_information_about_task(num, self.tasks)
				if task_info is None: continue
				where = task_info[0]
				text = task_info[1]

				if where == 'daily_tasks' and daily_tasks[num - len(user_tasks) - 1][2]: continue
				self.console.print(f'- [green]{text}')


			self.console.print(f'\n[yellow]Золото: [green]+{round(gold, 2)}')
			self.console.print_tree_skills('[magenta]Навыки:', skills_)


		# Сохранение #
		self.hero_info['money'] += gold


		for num in sorted(nums, reverse=True):
			if (task_info := get_information_about_task(num, self.tasks)) is None: continue
			where, text, skills = task_info

			if where == 'user_tasks': del user_tasks[num - 1]
			elif where == 'daily_tasks':
				done = self.tasks['daily_tasks']['done']
				daily_tasks[num - len(user_tasks) - 1][2] = True

				# Если все подзадачи выполнены, а награды не выданы
				if all((daily_tasks[i][2] for i in range(len(daily_tasks)))) and not done:
					self.tasks['daily_tasks']['done'] = True

					self.console.print('\n[dim]Вы выполнили все ежедневные задания, вот ваша награда:')
					gold, skills, item = get_rewards_daily_tasks(daily_tasks, self.hero_info)

					self.hero_info['money'] += gold
					self.console.print(f'[yellow]Золото: [green]+{round(gold, 2)}')
					self.console.print_tree_skills('[magenta]Навыки:', skills)

					for skill, exp in skills.items():
						if skill in skills_:
							skills_[skill] += exp
						else:
							skills_[skill] = exp


		for skill, exp in skills_.items():
			self.hero_info['skills'][skill][1] += exp

		input()

	def delete_tasks(self):
		# Поскольку мы не можем удалить ежедневные задания или квест, то печатать их необязательно.
		user_tasks = self.tasks['user_tasks']

		self.console.title('Удаление заданий, чтобы выйти нажмите enter')
		self.console.print('[green]Пользовательские задания')
		if len(user_tasks) == 0: print('Вы не добавили задания')

		for _ in range(len(user_tasks)):
			text, skills = user_tasks[_]

			if skills is None:
				self.console.print(f'[white]({_ + 1}) {text}')
			else:
				self.console.print(f'[white]({_ + 1}) {text}  [dim cyan]Навыки: {", ".join(skills)}')

		command = self.console.input('\nКакие задания вы выполнили: ')


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
			del self.tasks['user_tasks'][num - 1]

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
			data = self.console.print_table_price(skills, self.hero_info)
			self.console.print(f'[yellow]Золото: {round(gold, 2)}\n')

			command = self.console.input('Какие навыки хотите прокачать: ')

			if command == '': return
			nums = [int(i) for i in re.findall(r'\d+', command) if 0 <= int(i) <= len(skills)]
			if not nums: return

			for num in nums:
				skill = data[num - 1]
				skill_lvl, skill_exp = skills[skill]
				demand_exp = CONSTANT_SKILL * skill_lvl ** MULTIPLIER_SKILL
				demand_gold = CONSTANT_GOLD * skill_lvl ** MULTIPLIER_GOLD

				if skill_lvl == 0:
					demand_exp, demand_gold = 0.25, 0.1
				elif skill_lvl == 1:
					demand_exp, demand_gold = 0.5, 0.25

				if demand_exp > skill_exp: continue
				if gold - demand_gold < 0: break

				gold = gold - demand_gold
				skills[skill][0] += 1

			self.hero_info['money'] = gold

	def update(self):
		daily_tasks = self.tasks['daily_tasks']['tasks']
		date_task = self.tasks['daily_tasks']['date']
		today = str(date.today())

		if date_task == '' or date_task != today:
			self.tasks['daily_tasks']['date'] = today
			self.tasks['daily_tasks']['done'] = False
			# todo: Выдача дневных задач

			tasks = random.sample(daily_tasks_, len(daily_tasks))

			for i, j in enumerate(tasks):
				self.tasks['daily_tasks']['tasks'][i] = j
