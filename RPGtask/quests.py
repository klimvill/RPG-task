from enum import IntEnum
from typing import Any


class QuestLevel(IntEnum):
	EASY = 1
	MEDIUM = 2
	HARD = 3
	LEGENDARY = 4

	@staticmethod
	def description(level):
		"""Describe the item type"""
		return LEVEL_DESCRIPTIONS[level]


LEVEL_DESCRIPTIONS = {
	QuestLevel.EASY: 'Простой',  # ★☆☆☆
	QuestLevel.MEDIUM: 'Средний',  # ★★☆☆
	QuestLevel.HARD: 'Сложный',  # ★★★☆
	QuestLevel.LEGENDARY: 'Легендарный',  # ★★★★
}


class Stage:
	def __init__(self, data: dict[str, Any]):
		self.name: str = data["name"]
		self.goals: list[list[str]] = data["goals"]
		self.rewards: list[str] = data["rewards"]

	def __repr__(self):
		return f"<Stage name={self.name!r} goals={len(self.goals)}>"


class Quest:
	def __init__(self, identifier: str, name: str, level: QuestLevel, description: str, stages: dict[str | int, dict[str, Any]]):
		self.id = identifier
		self.name = name
		self.level = level
		self.description = description
		self.stages: dict[str | int, Stage] = {i: Stage(j) for i, j in stages.items()}

	def __repr__(self):
		return f"<Quest id={self.id!r} name={self.name!r} stages={len(self.stages)}>"


class QuestManager:
	def check(self): ...
