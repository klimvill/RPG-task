from ..inventory import Item, ItemType
from ..player import SkillType

# Зелья #
# Medicine
...
# Potion
...
# Elixir
...


#################################           Шлемы - 1 уровень           ################################################
ragged_hood = Item('ragged_hood', 'Рванный капюшон', 'кусок ткани, который можно носить на голове.')
ragged_hood.set_type(ItemType.HELMET)
ragged_hood.set_cost(1, 0.5)

old_helmet = Item('old_helmet', 'Старый шлем', 'повидал немало битв, сгодится на металлолом.')
old_helmet.set_type(ItemType.HELMET)
old_helmet.set_effect(SkillType.POWER, 1.03)
old_helmet.set_effect(SkillType.ENDURANCE, 1.03)
old_helmet.set_cost(3, 1)

wooden_circlet = Item('wooden_circlet', 'Деревянный обруч', 'старательно вырезанное украшение.')
wooden_circlet.set_type(ItemType.HELMET)
wooden_circlet.set_effect(SkillType.ART, 1.03)
wooden_circlet.set_effect(SkillType.LANGUAGES, 1.03)
wooden_circlet.set_cost(3, 1)

tin_helmet = Item('tin_helmet', 'Жестяной шлем', 'таким снаряжают городскую стражу.')
tin_helmet.set_type(ItemType.HELMET)
tin_helmet.set_effect(SkillType.POWER, 1.1)
tin_helmet.set_cost(5, 3)


#################################           Шлемы - 2 уровень           ################################################
steel_helmet = Item('steel_helmet', 'Стальной шлем', 'в таких ходят главари разбойников.')
steel_helmet.set_type(ItemType.HELMET)
steel_helmet.set_effect(SkillType.POWER, 1.06)
steel_helmet.set_effect(SkillType.ENDURANCE, 1.06)
steel_helmet.set_cost(20, 10)

brodie_helmet = Item('brodie_helmet', 'Шлем Броди', 'он защищал владельца от падающих болтов.')
brodie_helmet.set_type(ItemType.HELMET)
brodie_helmet.set_effect(SkillType.SCIENCE, 1.1)
brodie_helmet.set_effect(SkillType.LANGUAGES, 1.1)
brodie_helmet.set_effect(SkillType.CRAFT, 1.05)
brodie_helmet.set_cost(75, 35)

pink_ribbon = Item('pink_ribbon', 'Розовая ленточка', 'украшение в форме цветка, хорошо сочетается с голубым.')
pink_ribbon.set_type(ItemType.HELMET)
pink_ribbon.set_effect(SkillType.CRAFT, 1.1)
pink_ribbon.set_effect(SkillType.ART, 1.1)
pink_ribbon.set_effect(SkillType.FINANCE, 1.05)
pink_ribbon.set_cost(50, 25)


#################################           Шлемы - 3 уровень           ################################################
straw_hat = Item('straw_hat', 'Соломенная шляпа', 'шляпа настоящего искателя приключений.')
straw_hat.set_type(ItemType.HELMET)
straw_hat.set_effect(SkillType.POWER, 1.5)
straw_hat.set_effect(SkillType.ENDURANCE, 1.5)
straw_hat.set_effect(SkillType.INTELLECT, 1.4)
straw_hat.set_cost(1000, 500)

stahlhelm = Item('stahlhelm', 'Штальхельм', 'от него веет безнадёгой.')
stahlhelm.set_type(ItemType.HELMET)
stahlhelm.set_effect(SkillType.ART, 1.5)
stahlhelm.set_effect(SkillType.ENDURANCE, 1.2)
stahlhelm.set_effect(SkillType.POWER, 1.2)
stahlhelm.set_cost(500, 250)



#################################           Оружие - 1 уровень           ###############################################
#################################           Оружие - 2 уровень           ###############################################
#################################           Оружие - 3 уровень           ###############################################
arisaka_type_38 = Item('arisaka_type_38', 'Арисака типа 38', 'абсолютно безнадёжная винтовка.')
arisaka_type_38.set_type(ItemType.WEAPON)
arisaka_type_38.set_effect(SkillType.SCIENCE, 1.3)
arisaka_type_38.set_effect(SkillType.ENDURANCE, 1.3)
arisaka_type_38.set_effect(SkillType.CRAFT, 1.3)
arisaka_type_38.set_cost(500, 250)



#################################           Кольца - 1 уровень           ###############################################
silver_ring = Item('silver_ring', 'Серебряное кольцо', 'обычное, ничем не примечательное украшение.')
silver_ring.set_type(ItemType.RING)
silver_ring.set_effect(SkillType.LANGUAGES, 1.03)
silver_ring.set_effect(SkillType.FINANCE, 1.03)
silver_ring.set_cost(10, 5)


#################################           Кольца - 2 уровень           ###############################################
ring_euclase = Item('ring_euclase', 'Кольцо с эвклазом',
					'изысканное украшение с бело-голубой гаммой, выглядит... серьёзно.')
ring_euclase.set_type(ItemType.RING)
ring_euclase.set_effect(SkillType.SCIENCE, 1.2)
ring_euclase.set_effect(SkillType.FINANCE, 1.3)
ring_euclase.set_cost(100, 50)


#################################           Кольца - 3 уровень           ###############################################
phantom_ring = Item('phantom_ring', 'Фантомное кольцо',
					'серебряное украшение с тёмно-синим сапфиром и загадочным рисунком, напоминающим герб.')
phantom_ring.set_type(ItemType.RING)
phantom_ring.set_effect(SkillType.INTELLECT, 1.4)
phantom_ring.set_effect(SkillType.LANGUAGES, 1.3)
phantom_ring.set_effect(SkillType.FINANCE, 1.2)
phantom_ring.set_effect(SkillType.CRAFT, 1.2)
phantom_ring.set_cost(600, 300)



#################################           Амулеты - 1 уровень           ##############################################
#################################           Амулеты - 2 уровень           ##############################################
#################################           Амулеты - 3 уровень           ##############################################
amulet_phosphophyllite = Item('amulet_phosphophyllite', 'Амулет с Фоссфофилитом',
							  'красивое украшение из золота и платины с потрескавшимся камнем.')
amulet_phosphophyllite.set_type(ItemType.AMULET)
amulet_phosphophyllite.set_effect(SkillType.POWER, 1.4)
amulet_phosphophyllite.set_effect(SkillType.ENDURANCE, 1.4)
amulet_phosphophyllite.set_effect(SkillType.ART, 1.2)
amulet_phosphophyllite.set_effect(SkillType.INTELLECT, 0.8)
amulet_phosphophyllite.set_cost(500, 250)



all_items = {
	'one': {
		'ragged_hood': ragged_hood,
		'old_helmet': old_helmet,
		'wooden_circlet': wooden_circlet,
		'tin_helmet': tin_helmet,

		'silver_ring': silver_ring,
	},
	'two': {
		'steel_helmet': steel_helmet,
		'brodie_helmet': brodie_helmet,
		'pink_ribbon': pink_ribbon,

		'ring_euclase': ring_euclase,
	},
	'three': {
		'straw_hat': straw_hat,
		'stahlhelm': stahlhelm,

		'arisaka_type_38': arisaka_type_38,

		'phantom_ring': phantom_ring,

		'amulet_phosphophyllite': amulet_phosphophyllite,
	}
}
