from .hero import save_hero_info
from .tasks import save_tasks


def all_save(tasks, hero_info):
	save_tasks(tasks)
	save_hero_info(hero_info)
