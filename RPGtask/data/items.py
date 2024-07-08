from ..inventory import ItemType, Item

# Зелья #
# Medicine
...
# Potion
...
# Elixir
...


# Снаряжение #
# Шлемы - 1 уровень
ragged_hood = Item('ragged_hood', 'Рванный капюшон', 'кусок ткани, который можно носить на голове.')
ragged_hood.set_type(ItemType.HELMET)
ragged_hood.set_cost(1, 0.5)

old_helmet = Item('old_helmet', 'Старый шлем', 'повидал немало битв, сгодится на металлолом.')
old_helmet.set_type(ItemType.HELMET)
old_helmet.set_effect('сила', 1.03)
old_helmet.set_effect('бой', 1.03)
old_helmet.set_cost(3, 1)

wooden_circlet = Item('wooden_circlet', 'Деревянный обруч', 'старательно вырезанное украшение.')
wooden_circlet.set_type(ItemType.HELMET)
wooden_circlet.set_effect('искусство', 1.03)
wooden_circlet.set_effect('красноречие', 1.03)
wooden_circlet.set_cost(3, 1)

tin_helmet = Item('tin_helmet', 'Жестяной шлем', 'таким обычно снаряжают городскую стражу.')
tin_helmet.set_type(ItemType.HELMET)
tin_helmet.set_effect('сила', 1.1)
tin_helmet.set_cost(5, 3)

# 2 уровень
steel_helmet = Item('steel_helmet', 'Стальной шлем', 'популярен среди разбойников.')
steel_helmet.set_type(ItemType.HELMET)
steel_helmet.set_effect('сила', 1.06)
steel_helmet.set_effect('скорость', 1.06)
steel_helmet.set_effect('выносливость', 1.06)

# 3 уровень
straw_hat = Item('straw_hat', 'Соломенная шляпа', 'шляпа настоящего искателя приключений!')
straw_hat.set_type(ItemType.HELMET)
straw_hat.set_effect('бой', 1.5)
straw_hat.set_effect('сила', 1.5)
straw_hat.set_effect('скорость', 1.4)
straw_hat.set_effect('выносливость', 1.4)
straw_hat.set_cost(1000, 500)
# Кольцо фантомхайтов  3 уровень
# Кольцо с Эвклазом - Наука - 1,2, Красноречие - 1,3      2 уровень



# Амулет
# 3 уровень
amulet_phosphophyllite = Item('amulet_phosphophyllite', 'Амулет с Фоссфофилитом', 'красивый амулет из золота и платины с потрескавшимся камнем.')
amulet_phosphophyllite.set_type(ItemType.AMULET)
amulet_phosphophyllite.set_effect('бой', 1.3)
amulet_phosphophyllite.set_effect('красноречие', 1.3)
amulet_phosphophyllite.set_effect('искусство', 1.25)
straw_hat.set_cost(400, 200)


all_items = {
	'one': {
		'ragged_hood': ragged_hood,
		'old_helmet': old_helmet,
		'wooden_circlet': wooden_circlet,
		'tin_helmet': tin_helmet,
	},
	'two': {
		'steel_helmet': steel_helmet,
	},
	'three': {
		'straw_hat': straw_hat,

		'amulet_phosphophyllite': amulet_phosphophyllite,
	}
}
