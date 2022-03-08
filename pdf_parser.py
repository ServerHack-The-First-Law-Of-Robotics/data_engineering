# pip install PyMuPDF
import fitz
import re
from tqdm.auto import tqdm


class ParsePDF:
    def __init__(self, pdf_path):
        # print("path", pdf_path)
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                # print("page", page, dir(page))
                text += page.getText()
        self.text = text

    def get_name(self):
        regex_res = re.search(r'Сокращенное наименование на русском\n[\S\s]*?языке', self.text)
        if regex_res is None:
            return None
        end = regex_res.end() + 1

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
        end = re.search(r'УСТАВНЫЙ КАПИТАЛ\n[\S\s]*?\nРазмер \(в рублях\)\n', self.text)
        # print("text", self.text)
        # print("end", end)
        if end is None:
            return None
        start = self.text[end.end():]
        return start[:start.find('\n')]

    def get_place(self):
        end = re.search(r'Место нахождения юридического лица\n((.|\n)*?)\d+', self.text)
        if end is None:
            return None
        string = end.group().replace('Место нахождения юридического лица\n', '')
        nums = re.search(f'\d+', string).group()
        return string.replace(nums, '').strip()

    def get_egrul_date(self):
        res = re.search(r'ГРН и дата внесения записи в ЕГРЮЛ\n\d+', self.text)
        if res is None:
            return None
        end = res.end()
        tail = self.text[end+1:]
        enter = tail.find('\n')
        return tail[:enter]


if __name__ == "__main__":
    from glob import glob
    from json import dump

    parsed = []

    pdf_paths = glob("data/egrul_pdf/*")
    for pth in tqdm(pdf_paths):
        inn = pth.split("_")[-1].split(".")[0]

        parser = ParsePDF(pth)

        sample_data = {
            "inn": inn,
            "name": parser.get_name(),
            "okveds": parser.get_okved(),
            "ustavnoi_capital": parser.get_oklad(),
            "location": parser.get_place(),
            "egrul_registration_date": parser.get_egrul_date()
        }
        parsed.append(sample_data)

    with open("data/egrul/parsed.json", "w") as f:
        dump(parsed, f)
