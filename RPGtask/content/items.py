from ..inventory import Item, ItemType
from ..player import SkillType

######################################           Квесты           ###############№######################################
# Квесты, которые находятся здесь не должны встречаться в гильдии.

lost_pet = Item('lost_pet', 'Квест "Потерявшийся питомец"', 'Мой питомец пропал и не возвращается домой. Я потратила все деньги на его поиски, пожалуйста, помогите.')
lost_pet.set_type(ItemType.ITEM)
lost_pet.set_effect('quest', 'lost_pet')
lost_pet.set_cost(25)


#####################################           Учебники           #####################################################
test_textbook = Item('test_textbook', 'Тестовый учебник', 'описание')
test_textbook.set_type(ItemType.ITEM)
test_textbook.set_effect('textbook', {SkillType.INTELLECT: 10})
test_textbook.set_effect('text', '{SkillType.INTELLECT: 10}')
test_textbook.set_cost(10, 10)


#######################################           Книги           ######################################################
test_book = Item('test_book', 'Тестовая книга', 'описание')
test_book.set_type(ItemType.ITEM)
test_book.set_effect('text', 'Умный текст')
test_book.set_cost(10, 10)



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
tin_helmet.set_cost(10, 5)

#################################           Шлемы - 2 уровень           ################################################
steel_helmet = Item('steel_helmet', 'Стальной шлем', 'в таких ходят главари разбойников.')
steel_helmet.set_type(ItemType.HELMET)
steel_helmet.set_effect(SkillType.POWER, 1.06)
steel_helmet.set_effect(SkillType.ENDURANCE, 1.06)
steel_helmet.set_cost(20, 10)

brodie_helmet = Item('brodie_helmet', 'Шлем Броди', 'защищал владельца от падающих болтов.')
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
pink_ribbon.set_cost(60, 30)

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


################################           Нагрудник - 1 уровень           #############################################
battered_quilted_armor = Item('battered_quilted_armor', 'Потрёпанная стёганка', 'вероятно, снята с погибшего бандита.')
battered_quilted_armor.set_type(ItemType.BREASTPLATE)
battered_quilted_armor.set_effect(SkillType.ENDURANCE, 1.02)
battered_quilted_armor.set_effect(SkillType.POWER, 1.02)
battered_quilted_armor.set_cost(3, 1.5)

chain_mail = Item('chain_mail', 'Кольчуга', 'металлические кольца поверх стёганой ткани неплохо защищают от острых лезвий.')
chain_mail.set_type(ItemType.BREASTPLATE)
chain_mail.set_effect(SkillType.POWER, 1.05)
chain_mail.set_effect(SkillType.CRAFT, 1.05)
chain_mail.set_cost(10, 5)

grey_mantle = Item('grey_mantle', 'Серая мантия', 'мантия тёмно-серого цвета, сшитая из шкуры крысы Макки.')
grey_mantle.set_type(ItemType.BREASTPLATE)
grey_mantle.set_effect(SkillType.ENDURANCE, 1.08)
grey_mantle.set_effect(SkillType.LANGUAGES, 1.05)
grey_mantle.set_cost(12, 6)

################################           Нагрудник - 2 уровень           #############################################
quilted_armor = Item('quilted_armor', 'Стёганка', 'несколько слоёв ткани, крепко соединённых между собой.')
quilted_armor.set_type(ItemType.BREASTPLATE)
quilted_armor.set_effect(SkillType.POWER, 1.1)
quilted_armor.set_effect(SkillType.ART, 1.1)
quilted_armor.set_cost(40, 20)


#################################           Оружие - 1 уровень           ###############################################
#################################           Оружие - 2 уровень           ###############################################
shorty = Item('shorty', 'Коротыш', 'мощный одноручный дробовик.')
shorty.set_type(ItemType.WEAPON)
shorty.set_effect(SkillType.ENDURANCE, 1.1)
shorty.set_effect(SkillType.POWER, 1.1)
shorty.set_cost(50, 25)

beretta_70 = Item('beretta_70', 'Беретта 70', 'итальянский самозарядный пистолет.')
beretta_70.set_type(ItemType.WEAPON)
beretta_70.set_effect(SkillType.SCIENCE, 1.2)
beretta_70.set_effect(SkillType.CRAFT, 1.15)
beretta_70.set_effect(SkillType.ART, 1.15)
beretta_70.set_cost(60, 30)

#################################           Оружие - 3 уровень           ###############################################
arisaka_type_38 = Item('arisaka_type_38', 'Арисака типа 38', 'абсолютно безнадёжная винтовка.')
arisaka_type_38.set_type(ItemType.WEAPON)
arisaka_type_38.set_effect(SkillType.SCIENCE, 1.3)
arisaka_type_38.set_effect(SkillType.CRAFT, 1.3)
arisaka_type_38.set_effect(SkillType.ENDURANCE, 1.2)
arisaka_type_38.set_cost(300, 150)

aqua_heartia = Item('aqua_heartia', 'Аква Хартия', 'магический посох, изготовленный лучшим мастером королевства.')
aqua_heartia.set_type(ItemType.WEAPON)
aqua_heartia.set_effect(SkillType.INTELLECT, 1.4)
aqua_heartia.set_effect(SkillType.LANGUAGES, 1.4)
aqua_heartia.set_effect(SkillType.FINANCE, 1.25)
aqua_heartia.set_effect(SkillType.CRAFT, 1.25)
aqua_heartia.set_cost(600, 300)


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
		'ragged_hood': ragged_hood, 'old_helmet': old_helmet, 'wooden_circlet': wooden_circlet,
		'tin_helmet': tin_helmet,

		'chain_mail': chain_mail, 'battered_quilted_armor': battered_quilted_armor, 'grey_mantle': grey_mantle,

		'silver_ring': silver_ring,


		'lost_pet': lost_pet, 'test_book': test_book, 'test_textbook': test_textbook
	},
	'two': {
		'steel_helmet': steel_helmet, 'brodie_helmet': brodie_helmet, 'pink_ribbon': pink_ribbon,

		'quilted_armor': quilted_armor,

		'shorty': shorty, 'beretta_70': beretta_70,

		'ring_euclase': ring_euclase,
	},
	'three': {
		'straw_hat': straw_hat, 'stahlhelm': stahlhelm,

		'arisaka_type_38': arisaka_type_38, 'aqua_heartia': aqua_heartia,

		'phantom_ring': phantom_ring,

		'amulet_phosphophyllite': amulet_phosphophyllite,
	}
}
