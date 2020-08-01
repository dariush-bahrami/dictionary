import argparse
from word_database import WordDatabase
import json
import random
from longman_dictionary_module import *

# CLI Configuration
parser = argparse.ArgumentParser(prog='Longman Dictionary',
                                 description='Longman Dictionary Scraper',
                                 epilog='coded by dAriush & Mantis')
parser.add_argument('word', metavar='Word', type=str, help='The word')
parser.add_argument('-c',
                    '--collocation',
                    action='store_true',
                    help='Print Collocations')
parser.add_argument('-e',
                    '--etymology',
                    action='store_true',
                    help='Print Etymology')
parser.add_argument('-d',
                    '--definition',
                    action='store_false',
                    help='Do Not Print Definitions')

parser.add_argument('-s',
                    '--save',
                    action='store_true',
                    help='Save Results to Database')

parser.add_argument('-o',
                    '--offline',
                    action='store_true',
                    help='Search in Database')
args = parser.parse_args()

with open('dictionary_configs.json') as config_file:
    config_data = json.load(config_file)

database = WordDatabase(config_data["Database Name"])

if not args.offline:
    # Creating LongmanDictionary Object
    word_result = LongmanDictionary(args.word)
    def_box = word_result.definition_box
    colloc_box = word_result.collocation_box
    etym_box = word_result.etymology_box
else:
    if args.word in database.words:
        boxes = database.read_word_content(args.word).split('\n\n')
        def_box, colloc_box, etym_box = boxes
        database.increase_word_frequency(args.word)
    else:
        print('{0} does not exist in database {1}'.format(
            args.word, random.choice(LongmanDictionary.emojis)))
        exit()

# Showing Outputs
if args.definition:
    print_definitions(def_box)

if args.collocation:
    print()
    print_collocations(colloc_box)

if args.etymology:
    print()
    print_etymology(etym_box)

# Saving Result
if args.save and (not args.offline):
    add_word_2_database(database, word_result)