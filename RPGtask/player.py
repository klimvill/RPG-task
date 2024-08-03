from enum import IntEnum


class SkillType(IntEnum):
	""" Типы навыков. """
	INTELLECT = 0
	SCIENCE = 1
	LANGUAGES = 2
	ART = 3
	POWER = 4
	ENDURANCE = 5
	FINANCE = 6
	CRAFT = 7

	@staticmethod
	def description(skill):
		""" Описание навыка """
		return SKILL_DESCRIPTIONS[skill]


SKILL_DESCRIPTIONS = {
	SkillType.INTELLECT: 'Интеллект',
	SkillType.SCIENCE: 'Наука',
	SkillType.LANGUAGES: 'Языки',
	SkillType.ART: 'Искусство',
	SkillType.POWER: 'Сила',
	SkillType.ENDURANCE: 'Выносливость',
	SkillType.FINANCE: 'Финансы',
	SkillType.CRAFT: 'Ремесло'
}


class RankType(IntEnum):
	""" Типы рангов. """
	F = 1
	E = 2
	D = 3
	C = 4
	B = 5
	A = 6
	S = 7

	@staticmethod
	def description(rank):
		""" Описание ранга. """
		return RANK_DESCRIPTIONS[rank]

	@staticmethod
	def experience(rank):
		""" Необходимое количество опыта для получения ранга. """
		return RANK_EXPERIENCE[rank]


RANK_DESCRIPTIONS = {
	RankType.F: 'F',
	RankType.E: 'E',
	RankType.D: 'D',
	RankType.C: 'C',
	RankType.B: 'B',
	RankType.A: 'A',
	RankType.S: 'S',
}
RANK_EXPERIENCE = {
	RankType.F: 15,
	RankType.E: 35,
	RankType.D: 50,
	RankType.C: 70,
	RankType.B: 100,
	RankType.A: 120,
	RankType.S: 200,
}


class Gold:
	"""
	Объект золота игрока.

	Аргументы:
		gold (float): Золото игрока. По умолчанию 0.

	Методы:
		save(): Сохранение информации о количестве денег.
		load(num): Загрузка информации о количестве денег.
		add_money(num): Добавляет деньги на баланс пользователя.
		payment(num): Оплата.
	"""

	def __init__(self):
		self.gold: float = 0

	def save(self) -> float:
		""" Сохранение информации о количестве денег. """
		return self.gold

	def load(self, num: float):
		""" Загрузка информации о количестве денег. """
		self.gold = num

	def add_money(self, num: float):
		"""
		Добавляет деньги на баланс пользователя.

		Аргументы:
			num (float): Сумма, на которую увеличится капитал.
		"""
		self.gold += num

	def payment(self, num: float):
		"""
		Оплата.

		Аргументы:
			num (float): Сумма, на которую уменьшится капитал.
		"""
		if self.gold > num:
			self.gold -= num
		else:
			self.gold = 0


class Skill:
	"""
	Объект навыка.

	Параметры:
		skill_type (SkillType): Тип навыка.

	Атрибуты:
		level (int): Уровень навыка.
		exp (int): Опыт навыка.

	Методы:
		save(): Сохранение навыка.
		load(): Загрузка навыка.
		add_level(): Прибавляет один уровень.
		add_exp(): Прибавляет опыт.
		reduce_exp(): Убавляет опыт.
	"""

	def __init__(self, skill_type: SkillType):
		self.skill_type = skill_type

		self.level: int = 0
		self.exp: float = 0

	def save(self) -> list[int | float]:
		""" Сохранение навыка. """
		return [self.level, self.exp]

	def load(self, data: list[int | float]):
		""" Загрузка навыка. """
		self.level, self.exp = data

	def add_level(self):
		""" Прибавляет один уровень. """
		self.level += 1

	def add_exp(self, num: float):
		""" Прибавляет опыт. """
		self.exp += num

	def reduce_exp(self, num: float):
		""" Убавляет опыт. """
		if self.exp > num:
			self.exp -= num
		else:
			self.exp = 0


class Player:
	"""
	Объект игрока. В этом классе хранится вся информация о деньгах и навыках.

	Аргументы:
		name (str): Имя персонажа. По умолчанию пустая строка.
		rank (RankType): Ранг персонажа. По умолчанию RankType.F
		experience (int): Опыт. По умолчанию 0.
		shops_save (dict[str, str | list[str]]): Сохранения магазина предметов. По умолчанию пустой словарь.

		gold (Gold): объект золота.
		skills (list[Skill]): список навыков.

	Методы:
		save(): Возвращает данные для сохранения.
		load(data): Загружает данные пользователя из сохранения.
		add_experience(): Добавляет опыт за выполнение квеста.
		sum_level(): Считает сумму всех уровней навыков.
	"""

	def __init__(self):
		self.name: str = ''
		self.rank: RankType = RankType.F
		self.experience: int = 0
		self.shops_save: dict[str, str | list[str]] = {}

		self.gold = Gold()

		self.skills: list[Skill] = [
			Skill(SkillType.INTELLECT),
			Skill(SkillType.SCIENCE),
			Skill(SkillType.LANGUAGES),
			Skill(SkillType.ART),
			Skill(SkillType.POWER),
			Skill(SkillType.ENDURANCE),
			Skill(SkillType.FINANCE),
			Skill(SkillType.CRAFT),
		]

	def save(self) -> dict[str, float | list[list[int | float]]]:
		""" Возвращает данные для сохранения. """
		return {'name': self.name, 'rank': self.rank, 'experience': self.experience, 'money': self.gold.save(),
				'shops_save': self.shops_save, 'skills': [skill.save() for skill in self.skills]}

	def load(self, data: dict[str, float | list[list[int | float]]]):
		""" Загружает данные пользователя из сохранения. """
		self.name = data['name']
		self.rank = data['rank']
		self.experience = data['experience']
		self.shops_save = data['shops_save']
		self.gold.load(data['money'])

		for count, skill_data in enumerate(data['skills']):
			self.skills[count].load(skill_data)

	def add_experience(self) -> bool:
		""" Добавляет опыт за выполнение квеста. """
		max_exp_rank = RankType.experience(RankType.S)

		if self.rank == RankType.S and self.experience >= max_exp_rank - 1:
			self.experience = max_exp_rank
			return False

		self.experience += 1

		if self.experience == RankType.experience(self.rank):
			self.rank += 1
			return True
		return False

	def sum_level(self) -> int:
		""" Считает сумму всех уровней навыков. """
		all_level = 0

		for skill in self.skills:
			all_level += skill.level

		return all_level
