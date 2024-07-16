from ..player import SkillType
from ..daily_tasks import DailyTask


reader_1 = DailyTask('reader_1', 'Прочитать 10 страниц', [SkillType.INTELLECT, SkillType.SCIENCE])
reader_2 = DailyTask('reader_2', 'Прочитать короткий фантастический рассказ', [SkillType.INTELLECT, SkillType.SCIENCE])

power_1 = DailyTask('power_1', 'Отжаться 10 раз', [SkillType.POWER])



all_daily_tasks = {
	'reader_1': reader_1,
	'reader_2': reader_2,

	'power_1': power_1
}
