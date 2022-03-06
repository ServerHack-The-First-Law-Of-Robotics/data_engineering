# pip install PyMuPDF
import fitz
import re


class ParsePDF:
    def __init__(self, pdf_path):
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
        self.text = text

    def get_name(self):
        end = re.search(r'Сокращенное наименование на русском\nязыке', self.text).end() + 1
        tail = self.text[end:]
        space = tail.find(' ')
        return tail[:space]

    def get_soz(self):
        return 'Фонда социального страхования' in self.text

    def get_okved(self):
        finds = [m.end() for m in re.finditer(r'Код и наименование вида деятельности\n', self.text)]
        lst = []
        for i in finds:
            start = self.text[i:]
            space = start.find(' ')
            number = start[:space]
            lst.append(number)
        return lst

    def get_oklad(self):
        end = re.search(r'УСТАВНЫЙ КАПИТАЛ\n\d+\nРазмер \(в рублях\)\n', self.text)
        start = self.text[end.end():]
        return start[:start.find('\n')]

    def get_place(self):
        end = re.search(r'Место нахождения юридического лица\n((.|\n)*?)\d+', self.text)
        string = end.group().replace('Место нахождения юридического лица\n', '')
        nums = re.search(f'\d+', string).group()
        return string.replace(nums, '').strip()

    def get_egrul_date(self):
        end = re.search(r'ГРН и дата внесения записи в ЕГРЮЛ\n\d+', self.text).end()
        tail = self.text[end+1:]
        enter = tail.find('\n')
        return tail[:enter]