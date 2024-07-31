from ..player import RankType
from ..quests import Quest

forgotten_city = Quest('forgotten_city', 'Забытый город', 'Исследуйте город, познакомитесь с местными', RankType.S,
					   {
						   1: {'name': 'Где я?',
							   'goals': [['Гильдия', 'Дойдите до гильдии'], ['Первое задание', 'Возьмите задание']],
							   'rewards': ['stage', '2']
							   },
						   2: {'name': 'Выполните первое задание',
							   'goals': [['Ох, уж эти гоблины!', 'Победите гоблинов']],
							   'rewards': ['end']
							   },
					   }, {'gold': 12, 'items': ['stahlhelm', 'stahlhelm']})

all_quest = [forgotten_city]
