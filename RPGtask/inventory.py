from enum import IntEnum
from typing import NoReturn, Self


class ItemType(IntEnum):
	""" Типы предметов. """
	ITEM = 0  # Предмет

	# Если потребуется изменить, то надо также поменять is_wearable в Item
	HELMET = 1  # Шлем
	BREASTPLATE = 2  # Нагрудник
	LEGGINGS = 3  # Поножи
	BOOTS = 4  # Ботинки
	WEAPON = 5  # Оружие
	RING = 6  # Кольцо
	AMULET = 7  # Амулет

	@staticmethod
	def description(item_type) -> str:
		""" Описание типа предмета """
		return ITEM_DESCRIPTIONS[item_type]


ITEM_DESCRIPTIONS = {
	ItemType.ITEM: 'Предмет',
	ItemType.HELMET: 'Шлем',
	ItemType.BREASTPLATE: 'Нагрудник',
	ItemType.LEGGINGS: 'Поножи',
	ItemType.BOOTS: 'Ботинки',
	ItemType.WEAPON: 'Оружие',
	ItemType.RING: 'Кольцо',
	ItemType.AMULET: 'Амулет',
}


class Item:
	"""
	Объект предмета.

	Параметры:
		id (str): Уникальный идентификатор объекта.
		name (str): Имя предмета.
		description (str): Описание предмета.

	Атрибуты:
		stack (int): Количество предметов в стеке. По умолчанию 1.
		type (ItemType): Тип объекта. По умолчанию ItemType.ITEM.
		effects (dict[действие: str, величина: int]): Эффекты предмета. По умолчанию пустой словарь.
		sell (int): Цена продажи. По умолчанию 0.
		cost (int): Цена покупки. По умолчанию 0.
		possible_sell (bool): Можно ли продать? По умолчанию True

	Методы:
		set_stack(amount): Задаёт количество предметов в стеке.
		set_type(item_type): Задаёт тип объекта.
		set_effect(action, amount): Задаёт эффект от использования предмета.
		set_cost(cost, sell): Задаёт стоимость продажи и покупки.

		is_wearable() -> bool: Можно ли носить предмет.
		is_usable() -> bool: Можно ли использовать предмет.
	"""

	def __init__(self, identifier: str, name: str, description: str):
		self.id = identifier
		self.name = name
		self.description = description

		self.stack: int = 1
		self.type: ItemType = ItemType.ITEM
		self.effects: dict[str | int, str | float] = {}
		self.sell: float = 0
		self.cost: float = 0
		self.possible_sell: bool = True

	def set_stack(self, amount: int) -> NoReturn:
		"""
		Задаёт количество предметов в стеке.

		Аргументы:
			amount (int): количество предметов в стеке.
		"""
		self.stack = amount

	def set_type(self, item_type: ItemType) -> NoReturn:
		"""
		Задаёт тип предмета.

		Аргументы:
			item_type (ItemType): Тип объекта
		"""
		self.type = item_type

	def set_effect(self, action: str | int, amount: str | float) -> NoReturn:
		"""
		Задаёт эффект от использования предмета.

		Аргументы:
			action (str | int): Действие, выполняемое при использовании предмета.
			amount (int): Величина эффекта.
		"""
		self.effects[action] = amount

	def set_cost(self, cost: float, sell: float = -1) -> NoReturn:
		"""
		Задаёт стоимость продажи и покупки.

		Аргументы:
			cost (int): Цена покупки.
			sell (int): Цена продажи. Если равняется -1, то предмет нельзя продать. По умолчанию -1.
		"""
		self.cost = cost

		if sell != -1:
			self.sell = sell
		else:
			self.possible_sell = False

	@property
	def is_wearable(self) -> bool:
		"""
		Можно ли носить предмет.

		Возвращается:
			bool: True если предмет можно носить, иначе False
		"""
		return 0 < self.type

	@property
	def is_usable(self) -> bool:
		"""
		Можно ли использовать предмет.

		Возвращается:
			bool: True если предмет можно использовать, иначе False.
		"""
		return bool(self.effects)

	def __repr__(self):
		""" Возвращает строковое представление объекта Item. """
		return f"<Item {self.id!r}>"


class Slot:
	"""
	Объект слота в инвентаре.

	Параметры:
		type (ItemType): Тип слота в инвентаре. По умолчанию ItemType.ITEM.

	Атрибуты:
		id (str): Идентификатор объекта, находящегося внутри. По умолчанию пустая строка.
		amount (int): Количество объектов внутри ячейки. По умолчанию 0.

	Методы:
		set(identifier: str, amount: int = 1) -> Self: Задаёт id и amount.
		save() -> tuple[str, int] | None: Возвращает данные для сохранения слота.
		load(data: tuple[str, int] | None): Загружает данные слота. Если данных нет, то очищает слот.
		clear(): Очищает слот.
		optimize(): Оптимизирует слот, удаляя ненужные данные.
		swap(slot: Slot): Меняет местами содержимое двух слотов.
		empty() -> bool: Проверяет слот на пустоту.
	"""

	def __init__(self, item_type: ItemType = ItemType.ITEM):
		self.type = item_type
		self.id: str = ""
		self.amount: int = 0

	def set(self, identifier: str, amount: int = 1) -> Self:
		"""
		Задаёт id и amount.

		Аргументы:
			identifier (str): Идентификатор предмета, находящегося внутри.
			amount (int, optional): Количество предметов, находящихся внутри.

		Возвращается:
			self: Ссылка на экземпляр объекта.
		"""
		self.id = identifier
		self.amount = amount

		return self

	def save(self) -> list[str, int] | None:
		"""
		Возвращает данные для сохранения слота.

		Возвращается:
			tuple: Кортеж, содержащий идентификатор и количество ячеек, или None, если ячейка пуста.
		"""
		return None if self.empty else [self.id, self.amount]

	def load(self, data: list[str, int] | None) -> NoReturn:
		"""
		Загружает данные слота. Если данных нет, то очищает слот.

		Аргументы:
			data (tuple[str, int] | None): Кортеж, состоящий из идентификатора и количества ячеек, или None.
		"""
		if data is not None:
			self.id = data[0]
			self.amount = data[1]
		else:
			self.clear()

	def clear(self) -> NoReturn:
		""" Очищает слот. """
		self.id = ""
		self.amount = 0

	def optimize(self) -> NoReturn:
		""" Оптимизирует слот, удаляя ненужные данные. """
		if not self.amount:
			self.id = ""
		if not self.id:
			self.amount = 0

	def swap(self, slot) -> NoReturn:
		"""
		Меняет местами содержимое двух слотов.

		Аргументы:
			slot (Slot): Слот для обмена.
		"""
		slot.id, self.id = self.id, slot.id
		slot.amount, self.amount = self.amount, slot.amount

	@property
	def empty(self) -> bool:
		"""
		Проверяет слот на пустоту.

		Возвращается:
			bool: True если слот пустой, иначе False.
		"""
		self.optimize()
		return not self.amount

	def __repr__(self) -> str:
		""" Возвращает строковое представление объекта Slot. """
		return f"<Slot {self.amount}x{self.id!r}>"


class Inventory:
	"""
	Представляет собой инвентарь.

	Параметры:
		is_carrier (bool, optional): Указывает на тип инвентаря. True - инвентарь игрока, False - хранилища. По умолчанию True.
		size (int, optional): Размер инвентаря. По умолчанию 10.

	Атрибуты:
		slots (list[Slot]): Слоты инвентаря.

	Методы:
		save() -> list[tuple[str, int]]: Возвращает данные для сохранения инвентаря.
		load(data: list[tuple[str, int]]): Загружает инвентарь из сохранения.

		take(item: Item, amount: int) -> int: Добавляет предмет в инвентарь.
		get(): Извлекает из инвентаря слоты определенного типа предметов.

		count_item( item: Item | str) -> int: Считает количество определённых предметов в инвентаре.
		count_all() -> int: Возвращает количество всех предметов в инвентаре.
	"""

	def __init__(self, is_carrier: bool = True, size: int = 10):
		self.is_carrier = is_carrier
		self.size = size

		self.slots: list[Slot] = [Slot(ItemType.ITEM) for _ in range(size)]
		if is_carrier:
			self.slots.extend([
				Slot(ItemType.HELMET),
				Slot(ItemType.BREASTPLATE),
				Slot(ItemType.LEGGINGS),
				Slot(ItemType.BOOTS),
				Slot(ItemType.WEAPON),
				Slot(ItemType.RING),
				Slot(ItemType.RING),
				Slot(ItemType.AMULET),
			])

	def save(self) -> list[list[str, int]]:
		""" Возвращает данные для сохранения инвентаря. """
		return [slot.save() for slot in self.slots]

	def load(self, data):
		""" Загружает инвентарь из сохранения. """
		for count, slot_data in enumerate(data):
			self.slots[count].load(slot_data)

	def take(self, item: Item, amount: int) -> int:
		"""
		Добавляет предмет в инвентарь.

		Аргументы:
			item (Item): Предмет, который нужно взять.
			amount (int): Количество предметов.

		Возвращается:
			int: Количество предметов, которые не удалось забрать.
		"""
		for slot in self.slots:
			if slot.type == ItemType.ITEM:
				if slot.empty:
					slot_amount = min(item.stack, amount)
					amount -= slot_amount
					slot.id = item.id
					slot.amount = slot_amount
				elif slot.id == item.id:
					slot_amount = min(item.stack - slot.amount, amount)
					amount -= slot_amount
					slot.amount += slot_amount
			if amount == 0:
				break
		return amount

	def get(self, item_type: ItemType, inverse: bool = False, only_empty: bool = False) -> list[tuple[int, Slot]]:
		"""
		Извлекает из инвентаря слоты определенного типа предметов.

		Аргументы:
			item_type (ItemType): Тип предмета, для которого нужно получить слоты.
			inverse (bool, optional): Возвращает все ячейки других типов. По умолчанию False.
			only_empty (bool, optional): Возвращает только пустые ячейки. По умолчанию False.

		Возвращается:
			list: Список кортежей, содержащих индекс и слот соответствующих слотов.
		"""
		res: list[tuple[int, Slot]] = []
		for i, slot in enumerate(self.slots):
			if not inverse and slot.type == item_type:
				res.append((i, slot))
			elif inverse and slot.type != item_type:
				res.append((i, slot))
		if only_empty:
			res = [(i, slot) for i, slot in res if slot.empty]
		return res

	def count_item(self, item: Item | str) -> int:
		"""
		Считает количество определённых предметов в инвентаре.

		Аргументы:
			item (Item | str): Предмет, который надо посчитать.

		Возвращается:
			int: Количество определённых предметов в инвентаре.
		"""
		item = item.id if isinstance(item, Item) else item
		return sum(slot.amount for slot in self.slots if slot.id == item)

	def count_all(self) -> int:
		""" Возвращает количество всех предметов в инвентаре. """
		return sum(slot.amount for slot in self.slots)

	def __repl__(self):
		""" Возвращает строковое представление инвентаря. """
		return f"<Inventory {[s.id for s in self.slots]}>"
