from mantis_textbox import mantis_textbox
from word_database import WordDatabase
import json


def replace_chars(string: str, chars_table: dict) -> str:
    for char in chars_table:
        string = string.replace(char, chars_table[char])
    return string


class LongmanDictionary:
    url = 'https://www.ldoceonline.com/dictionary/'
    emojis = [
        '\m/_(>_<)_\m/',
        '\m/ (>.<) \m/',
        '\,,/(^_^)\,,/',
        '\(^-^)/',
        '( 0 _ 0 )',
        'd[-_-]b',
        '<(^_^)>',
        '¯\(°_o)/¯',
        '[¬º-°]¬',
    ]

    def __init__(self, word):
        import requests
        from bs4 import BeautifulSoup

        self.word = word.lower()
        self.response = requests.get(LongmanDictionary.url +
                                     self.word.replace(' ', '-'))
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

        self.box_margin_char = '#'
        self.box_width = 60

    @property
    def definitions(self) -> list:
        definition_tags = self.soup.find_all('span', attrs={'class': 'DEF'})
        definitions_results = []
        for meaning in definition_tags:
            definitions_results.append(''.join(list(meaning.strings)).strip())
        return definitions_results

    @property
    def definition_box(self):
        import random
        if len(self.parts_of_speech) != 0:
            parts_of_speech_str = '(' + ', '.join(self.parts_of_speech) + ') '
        else:
            parts_of_speech_str = ''

        box = mantis_textbox(
            self.definitions,
            title='Definitions of {0} {1}{2}'.format(
                self.word, parts_of_speech_str, random.choice(self.emojis)),
            margin_char=self.box_margin_char,
            width=self.box_width,
        )
        return box

    @property
    def collocations(self):
        collocation_tags = self.soup.find_all('span',
                                              attrs={'class': 'Collocate'})
        colloc_replacements = {'=; ': '= ', '; )': ')', '  ': ' '}
        collocations_results = []
        for example in collocation_tags:
            colloc_string = '; '.join(list(example.strings)).strip()
            new_colloc_str = replace_chars(colloc_string, colloc_replacements)
            collocations_results.append(new_colloc_str)
        return collocations_results

    @property
    def collocation_box(self):
        import random
        box = mantis_textbox(
            self.collocations,
            title=f'Collocations for {self.word} {random.choice(self.emojis)}',
            margin_char=self.box_margin_char,
            width=self.box_width,
        )
        return box

    @property
    def etymology(self):
        etymology_tags = self.soup.find_all('span', attrs={'class': 'etym'})

        etym_replacements = {
            '   ': ' ',
            '( ': '(',
            ' )': ')',
            ' ,': ',',
            '“ ': '“',
            ' ”': '”'
        }
        etymology_results = []
        for origin in etymology_tags:

            # Removing Superscripts
            superscript_tags = origin.find_all('span',
                                               attrs={'class': 'HOMNUM'})
            for st in superscript_tags:
                st.decompose()

            etym_string = ' '.join(list(origin.strings)).strip()
            new_etym_str = replace_chars(etym_string, etym_replacements)
            etymology_results.append(new_etym_str)
        return etymology_results

    @property
    def etymology_box(self):
        import random
        box = mantis_textbox(
            self.etymology,
            title=f'Etymology of {self.word} {random.choice(self.emojis)}',
            margin_char=self.box_margin_char,
            width=self.box_width,
        )
        return box

    @property
    def parts_of_speech(self):
        parts_of_speech_list = []
        for part in self.soup.find_all('span', attrs={'class': 'POS'}):
            parts_of_speech_list.append(''.join(list(part.strings)).strip())
        parts_of_speech_list = list(set(parts_of_speech_list))
        return parts_of_speech_list


def colored(fg_color, bold=False, underline=False, reversed_=False):
    import os, sys

    colors = {
        'BLACK': '\033[30m',
        'RED': '\033[31m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'BLUE': '\033[34m',
        'MAGENTA': '\033[35m',
        'CYAN': '\033[36m',
        'WHITE': '\033[37m',
        'RESET': '\033[0m'
    }

    bold_code = '\u001b[1m'
    underline_code = '\u001b[4m'
    reversed_code = '\u001b[7m'

    def decorator(func):
        def wraper(*args, **kwargs):
            os.system("")  # allows you to print ANSI codes in the windows CMD
            print(colors[fg_color.upper()], end='', flush=True)

            if bold:
                print(bold_code, end='', flush=True)

            if underline:
                print(underline_code, end='', flush=True)

            if reversed_:
                print(reversed_code, end='', flush=True)

            func(*args, **kwargs)

            print(colors['RESET'], end='', flush=True)

        return wraper

    return decorator


with open('dictionary_configs.json') as config_file:
    config_data = json.load(config_file)


@colored(config_data["Definition Box Color"])
def print_definitions(definition_box):
    print(definition_box)


@colored(config_data["Collocation Box Color"])
def print_collocations(collocation_box):
    print(collocation_box)


@colored(config_data["Etymology Box Color"])
def print_etymology(etymology_box):
    print(etymology_box)


def add_word_2_database(database: WordDatabase,
                        word_result: LongmanDictionary):
    word = word_result.word
    content_string = '\n\n'.join([
        word_result.definition_box, word_result.collocation_box,
        word_result.etymology_box
    ])

    if database.database_path.is_dir():
        if word in database.words:
            database.increase_word_frequency(word)
        else:
            database.create_word_dir(word)
        database.write_word_content(word, content_string)
        database.backup()
    else:
        database.create_database()
        add_word_2_database(database, word_result)


if __name__ == '__main__':
    word = 'dog'
    word_result = LongmanDictionary(word)

    print_definitions(word_result)

    print_collocations(word_result)

    print_etymology(word_result)