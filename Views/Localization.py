# import json
# from pathlib import Path

class Translator:
	def __init__(self):
		self.translations = {
			'en': {
				'app.title': 'Product manager',

				'btn.ok': 'OK',
				'btn.save': 'Save',
				'btn.cancel': 'Cancel',
				'btn.delete': 'Delete',

				'dialog.name': 'Product name:',
				'dialog.weight': 'Weight (kg):',
				'dialog.note': 'Note:',

				'menu.file': 'File',
				'menu.view': 'View',
				'menu.export': 'Export to excell',
				'menu.print': 'Print logs',
				'menu.theme': 'Theme',
				'menu.default': 'Default',
				'menu.dark': 'Dark',
				'menu.products': 'Products',
				'menu.report': 'Reports',

				'msg.missing': 'Missing product, check the leftovers!',
				'msg.nochanges': 'No parameter has been changed!\nChange the value, or click "{txt}"',

				'lbl.logs': 'Logs:',

				'table.name': 'Name',
				'table.left': 'Left (kg)',
				'table.weight': 'weight (kg)',
				'table.date': 'date',
				'table.note': 'note',

				'test.message': 'Hello, {txt}!',

				'title.edit': 'Editing a recording',
				'title.delete': 'Deleting an entry',
				'title.receipt': 'Product receipt',
				'title.submit': 'Submit the product to work',

				'tooltip.submit': 'Submit the product to work',
				'tooltip.add': 'Add product',
				'tooltip.pickup': 'Pick up product',
				'tooltip.edit': 'Edit moves',
				'tooltip.del': 'Delete moves',
			},
			'uk': {
				'app.title': 'Облік продукту',

				'btn.ok': 'ОК',
				'btn.save': 'Зберегти',
				'btn.cancel': 'Відмінити',

				'dialog.name': 'Найменування продукту:',
				'dialog.weight': 'Вага (кг):',
				'dialog.note': 'Примітка:',

				'menu.file': 'Файл',
				'menu.view': 'Вид',
				'menu.export': 'Експорт в ексель',
				'menu.print': 'Друкувати журнал',
				'menu.theme': 'Тема',
				'menu.default': 'Звичайна',
				'menu.dark': 'Темна',
				'menu.products': 'Продукти',
				'menu.report': 'Звіт',

				'msg.missing': 'Не вистачає продукту, перевірте залишки!',
				'msg.nochanges': 'Жоден параметр не змінено!\nЗмініть значення, або натисніть "{txt}"',

				'lbl.logs': 'Журнал подій:',

				'table.name': 'Найменування',
				'table.left': 'Залишок (кг)',
				'table.weight': 'Вага (кг)',
				'table.date': 'Дата',
				'table.note': 'Примітка',

				'test.message': 'Привіт, {name}!',

				'title.edit': 'Редагування запису',
				'title.delete': 'Видалення запису',
				'title.receipt': 'Отримання продукту',
				'title.submit': 'Віддати продукт в роботу',

				'tooltip.submit': 'Віддати продукт в роботу',
				'tooltip.add': 'Добавити продукт',
				'tooltip.pickup': 'Забрати продукт',
				'tooltip.edit': 'Редагувати переміщення',
				'tooltip.del': 'Видалити переміщення',
			}
		}
		self.current_language = 'uk'

	def t(self, key, **kwargs):
		lang_dict = self.translations.get(self.current_language, {})
		text = lang_dict.get(key, key)

		if kwargs:
			try:
				return text.format(**kwargs)
			except Exception:
				return text
		return text

	def set_language(self, lang):
		if lang in self.translations:
			self.current_language = lang
			return True
		return False

	def get_languages(self):
		return list(self.translations.keys())

def _(key, **kwargs) -> str:
	translator = Translator()
	translator.set_language('uk')
	return 	translator.t(key, **kwargs)
