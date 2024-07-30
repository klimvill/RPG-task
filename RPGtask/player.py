from enum import IntEnum
from typing import NoReturn


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

	def load(self, num: float) -> NoReturn:
		""" Загрузка информации о количестве денег. """
		self.gold = num

	def add_money(self, num: float) -> NoReturn:
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


class RankType(IntEnum):
	""" Типы рангов. """
	F = 0
	E = 1
	D = 2
	C = 3
	B = 4
	A = 5
	S = 6

	@staticmethod
	def description(rank):
		""" Описание ранга. """
		return RANK_DESCRIPTIONS[rank]


RANK_DESCRIPTIONS = {
	RankType.F: 'F',
	RankType.E: 'E',
	RankType.D: 'D',
	RankType.C: 'C',
	RankType.B: 'B',
	RankType.A: 'A',
	RankType.S: 'S',
}


class Player:
	"""
	Объект игрока. В этом классе хранится вся информация о деньгах и навыках.

	Аргументы:
		gold (Gold): объект золота.
		skills (list[Skill]): список навыков.

	Методы:
		save(): Возвращает данные для сохранения.
		load(data): Загружает данные пользователя из сохранения.
		sum_level(): Считает сумму всех уровней навыков.
	"""

	def __init__(self):
		self.name: str = ''
		self.rang: RankType = RankType.F
		self.experience: int = 0

		self.gold = Gold()

		self.skills: list[Skill] = [
			Skill(SkillType.INTELLECT),
			Skill(SkillType.LANGUAGES),
			Skill(SkillType.SCIENCE),
			Skill(SkillType.ART),
			Skill(SkillType.POWER),
			Skill(SkillType.ENDURANCE),
			Skill(SkillType.FINANCE),
			Skill(SkillType.CRAFT),
		]

	def save(self) -> dict[str, float | list[list[int | float]]]:
		""" Возвращает данные для сохранения. """
		return {'name': self.name, 'money': self.gold.save(), 'skills': [skill.save() for skill in self.skills]}

	def load(self, data: dict[str, float | list[list[int | float]]]) -> NoReturn:
		""" Загружает данные пользователя из сохранения. """
		self.gold.load(data['money'])

		for count, skill_data in enumerate(data['skills']):
			self.skills[count].load(skill_data)

	def sum_level(self) -> int:
		""" Считает сумму всех уровней навыков. """
		all_level = 0

		for skill in self.skills:
			all_level += skill.level

		return all_level

	def set_name(self, name: str) -> NoReturn:
		self.name = name
