from PyQt6.QtCore import QTranslator

class UkrainianTranslator(QTranslator):
    def translate(self, context, sourceText, disambiguation, n=-1):
        translations = {
            "&Print":               "Друкувати",
            "&Options >>":          "Налаштування",
            "&Cancel":              "Відмінити",
            "P&roperties":          "Властивості",
            "&Name:":               "Назва принтера:",
            "Location:":            "Розташування:",
            "Type:":                "Тип:",
            "Output &file:":        "Зберегти файл:",
            "Page":                 "Сторінка",
            "Job Options":          "Налаштування друку",
            "Advanced":             "Додатково",
	        "Paper":                "Папір",
	        "Page size:":           "Розмір сторінки",
	        "Width:":               "Ширина:",
	        "Height:":              "Висота:",
	        "Orientation":          "Орієнтування",
	        "Portrait":             "Портрет",
	        "Landscape":            "Ландшафт",
	        "Margins":              "Поля",
	        "Page Layout":          "Макет сторінки",
	        "Pages per sheet:":     "Сторінок на аркуш:",
	        "Page order:":          "Послідовність сторінок:",
	        "Job Control":          "Керування роботою",
	        "Scheduled printing:":  "Запланований друк:",
            "Billing information:": "Нотатка:",
	        "Job priority:":        "Пріоритет друку:",
	        "Banner Pages":         "Заголовок сторінок:",
	        "Start:":               "Початок:",
	        "End:":                 "Кінець:"
        }
        return translations.get(sourceText, sourceText)