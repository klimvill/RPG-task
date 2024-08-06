from enum import IntEnum
from typing import Any


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
		return RANK_DESCRIPTIONS[rank][0]

	@staticmethod
	def experience(rank):
		""" Необходимое количество опыта для получения ранга. """
		return RANK_DESCRIPTIONS[rank][1]


RANK_DESCRIPTIONS = {
	RankType.F: ('F', 15),
	RankType.E: ('E', 35),
	RankType.D: ('D', 50),
	RankType.C: ('C', 70),
	RankType.B: ('B', 100),
	RankType.A: ('A', 120),
	RankType.S: ('S', 200),
}


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
		""" Описание навыка. """
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


class Gold:
	def __init__(self):
		self.gold: float = 0

	def payment(self, amount: float):
		""" Отнимает деньги.  """
		self.gold -= amount
		self.gold = self.gold if self.gold > 0 else 0

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Gold gold={self.gold}>"


class Skill:
	def __init__(self, skill_type: SkillType):
		self.skill_type = skill_type

		self.level: int = 0
		self.exp: float = 0

	def save(self) -> tuple[int, float]:
		""" Возвращает данные для сохранения навыка. """
		return self.level, self.exp

	def load(self, data: tuple[int, float]):
		""" Загружает данные навыка. """
		self.level, self.exp = data

	def reduce_exp(self, amount: float):
		""" Отнимает опыт. """
		self.exp -= amount
		self.exp = self.exp if self.exp > 0 else 0

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Skill level={self.level} exp={self.exp}>"


class GuildProfile:
	def __init__(self):
		self.name: str = ''
		self.rank: RankType = RankType.F
		self.experience: int = 0

		self.shops: dict[str, list[str] | str] = {}

	def save(self) -> tuple[str, int, int, dict]:
		""" Возвращает данные для сохранения профиля. """
		return self.name, self.rank, self.experience, self.shops

	def load(self, data: tuple[str, int, int, dict]):
		""" Загружает данные профиля. """
		self.name, self.rank, self.experience, self.shops = data

	def add_experience(self) -> bool:
		""" Прибавляет опыт, изменяет ранг. """
		self.experience += 1

		if self.experience >= RankType.experience(self.rank):
			if RankType.S == self.rank:
				self.experience = RankType.experience(RankType.S)
			else:
				self.experience = 0
				self.rank += 1

		return not self.experience

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<GuildProfile name={self.name} rank={self.rank} experience={self.experience}>"


class Player:
	def __init__(self):
		self.gold = Gold()
		self.profile = GuildProfile()

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

	def save(self) -> dict[str, Any]:
		""" Возвращает данные для сохранения игрока. """
		return {'money': self.gold.gold, 'skills': [s.save() for s in self.skills], 'profile': self.profile.save()}

	def load(self, data: dict[str, Any]):
		""" Загружает данные игрока. """
		self.gold.gold = data['money']
		self.profile.load(data['profile'])

		for count, skill_data in enumerate(data['skills']):
			self.skills[count].load(skill_data)

	def sum_level(self) -> int:
		""" Считает сумму всех уровней навыков. """
		return sum(skill.level for skill in self.skills)

	def __repr__(self):
		""" Возвращает строковое представление объекта. """
		return f"<Player gold={self.gold.gold} rank={self.profile.rank} experience={self.profile.experience}>"
