class WordDatabase:
    def __init__(self, database_name):
        from pathlib import Path

        self.database_path = Path(database_name)
        self.backup_path = Path(f'{database_name}.wdb')

    def create_database(self):
        if self.database_path.is_dir():
            print('Database already exist!')
        else:
            self.database_path.mkdir()

    @property
    def words_dir_path(self):
        words_path = {}
        for path_object in self.database_path.iterdir():
            if path_object.is_dir():
                word_str = path_object.parts[-1][6:]
                if word_str in words_path:
                    raise FileExistsError(
                        f'Multiple Instances of "{word_str}" found')
                words_path[word_str] = path_object
        return words_path

    @property
    def words(self):
        return list(self.words_dir_path.keys())

    @property
    def words_frequency(self):
        words_dict = {}
        for word in self.words_dir_path:
            word_path = self.words_dir_path[word]
            word_dir = word_path.parts[-1]
            words_dict[word_dir[6:]] = int(word_dir[:3])
        return words_dict

    @property
    def words_content_path(self):
        from pathlib import Path
        contents_dict = {}
        for word in self.words_dir_path:
            word_dir_path = self.words_dir_path[word]
            contents_dict[word] = Path.joinpath(word_dir_path,
                                                Path(word + '.txt'))
        return contents_dict

    def has_content(self, word):
        if word in self.words:
            return self.words_content_path[word].is_file()
        else:
            raise ValueError(f'{word} not found in database')

    def read_word_content(self, word):
        return self.words_content_path[word].read_text(encoding='utf-8')

    def create_word_dir(self, word):
        from pathlib import Path
        if word in self.words_dir_path:
            raise FileExistsError('Word already exist in database')
        else:
            frequency = 1
            word_dir_path = Path.joinpath(self.database_path,
                                          Path(f'{frequency:0>3} - {word}'))
            word_dir_path.mkdir()

    def increase_word_frequency(self, word, frequency_increase=1):
        from pathlib import Path
        if word not in self.words_dir_path:
            raise FileNotFoundError('Word not found in database')
        else:
            current_path = self.words_dir_path[word]
            current_freq = self.words_frequency[word]
            new_freq = current_freq + frequency_increase
            new_path = Path.joinpath(self.database_path,
                                     Path(f'{new_freq:0>3} - {word}'))
            current_path.rename(new_path)

    def write_word_content(self, word, content):
        self.words_content_path[word].write_text(content, encoding='utf-8')

    def backup(self):
        import pickle
        backup_dict = {}
        for word in self.words_content_path:
            content_path = self.words_content_path[word]
            try:
                backup_dict[content_path] = content_path.read_text(
                    encoding='utf-8')
            except FileNotFoundError:
                backup_dict[content_path] = f'There is not any data for {word}'
        with open(self.backup_path, mode='wb') as file:
            pickle.dump(backup_dict, file)

    def read_backup(self):
        import pickle
        with open(self.backup_path, mode='rb') as file:
            backup_data = pickle.load(file)
        return backup_data

    def recover_database(self):
        backup_data = self.read_backup()
        for content_path in backup_data:
            content_path.parents[0].mkdir(parents=True, exist_ok=True)
            content_path.write_text(backup_data[content_path],
                                    encoding='utf-8')
