from ..quests import QuestLevel, Quest

forgotten_city = Quest('forgotten_city', 'Забытый город', 'Исследуйте город, познакомитесь с местными', QuestLevel.EASY, {
	1: {'name': 'Где я?',
		'goals': [['Гильдия', 'Дойдите до гильдии'], ['Первое задание', 'Возьмите задание']],
		'rewards': ['stage', '2']
	},
	2: {'name': 'Выполните первое задание',
		'goals': [['Ох, уж эти гоблины!', 'Победите гоблинов']],
		'rewards': ['end']
	},
})

all_quest = [forgotten_city]
