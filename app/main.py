import os
from sys import platform
from typing import Generator, Optional, Self, Any, Callable

import win32con
import win32api

class EndPoints:
    """Класс, который нацелен на создание названий файлов."""
    def __init__(self, struct: int, expansion: str = '.txt'):
        self.expansion = expansion
        self.struct = struct
        
    def normal_view(self) -> str:
        return str(self.struct) + self.expansion
    
    def __eq__(self, other) -> bool:
        return self.struct == other.struct and self.expansion == other.expansion

    @classmethod
    def end_point_generator(cls, limiter: int = 12, start: int = 1,
                            degree: int = 2) -> Generator[Self, int, None]:
        for i in range(limiter):
            yield cls(start)
            start *= degree

class UseFile:
    def __init__(self, end_point: EndPoints):
        self._path: Optional[str] = None
        self.end_point = end_point
        
    def __str__(self):
        return self.normal_view

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, new_path: str = './.txt_lib/'):
        if self._path is None:
            self._path = new_path
    
    @property
    def normal_view(self):
        """Нормальный вид: строковое представление пути"""
        return self._path + self.end_point.normal_view()
    
    # Методы обработки текста
    def txt_read_and_split(self) -> list[list[str]]:
        """Превращает записи из файлов в списки значений."""
        with open(self.normal_view, 'r', encoding='utf-8') as read_line:
            return [line.rstrip('\n').split('/') for line in  read_line.readlines()]

    def txt_reader(self) -> Generator[dict[str, list], dict, None]:
        """Чтение файлов и распределение по словорям после опроса."""
        max_value: int = self.end_point.struct
        word_dict: dict = {}
        down_dict: dict = {}
        boost_dict: dict = {}

        if os.path.exists(self.normal_view):
            tmp_dict: dict[str, list] = {
                i: [j, int(n)] for i, j, n in self.txt_read_and_split()
                }

            for i in tmp_dict:
                if tmp_dict[i][1] == 0:
                    input_translatte = input(f'Translate {i} is: ').capitalize()
                    if input_translatte == tmp_dict[i][0]:
                        print('Прекрасно!')
                        tmp_dict[i][1] = max_value*2
                    else:
                        print(f'Нет. Правильно: {tmp_dict[i][0]}')
                        tmp_dict[i][1] = None
                else: tmp_dict[i][1] -= 1

            for i in tmp_dict:
                if tmp_dict[i][1] is None:
                    down_dict[i] = [tmp_dict[i][0], 1]
                elif tmp_dict[i][1] > max_value:
                    boost_dict[i] = tmp_dict[i]
                else:
                    word_dict[i] = tmp_dict[i]

            yield from (word_dict, down_dict, boost_dict)
        else: 
            yield from ({}, {}, {})

    def txt_writer(self, inp_dict: dict) -> None:
        """Запись в файл."""
        with open(self.normal_view, 'w', encoding='utf-8') as write_line:
            for item in inp_dict:
                write_line.write(f'{item}/{inp_dict[item][0]}/{inp_dict[item][1]}\n')

    def txt_clear(self) -> None:
        """Очистка файла."""
        with open(self.normal_view, 'w') as write_line:
            write_line.write('')

    def overwriting(self, other) -> None:
        """Переписывание одного файла полностью в другой."""
        with open(self.normal_view, 'r', encoding='utf-8') as read_line, \
                open(other.normal_view, 'a', encoding='utf-8') as write_line:
            write_line.write(read_line.read())
        self.txt_clear()
        
    def new_word_writer(self, word: str) -> None: # В коде не передается нулевой список, но должен!
        """"Функция записи новых ппар слов в словарь."""
        translation: str = input('Перевод: ')
        if translation != '':
            with open(self.normal_view, 'a', encoding='utf-8') as write_line:
                write_line.write(f'{word.capitalize()}/{translation.capitalize()}/1\n')


    # Секция поиска, изменения, удаления слова из словаря
    @staticmethod
    def set_word():
        return input('Введите слово для поиска:\n')
    
    def _word_finder_in_file(self, word: str) -> Optional[tuple[int, list[str]]]:
        spliting_file = self.txt_read_and_split()
        
        for line in spliting_file:
            if line[0] == word or line[1] == word:
                return (
                    spliting_file.index(line), 
                    line,
                    )
            else:
                return None
        else:
            return None

    @classmethod
    def word_finder(cls, word: str) -> Generator[Any, Any, None]: # Optional[tuple[Self, int, list[str]]]:
        """Поиск слова по всем файлам.
        Как само слово, так и перевод.
        """
        word = word.capitalize()
        for i in EndPoints(0), *EndPoints.end_point_generator():
            finder_file = cls(i)._word_finder_in_file(word)
            if finder_file is not None:
                yield from (cls(i), ) + finder_file
        else:
            print(f'{word}: word not exist.')
            return None

    def word_deleter(self, index: int) -> None:
        with open(self.normal_view, 'r', encoding='utf-8') as read_line:
            readlines_for_index = read_line.readlines()
            join_list = ''.join(readlines_for_index[:index]
                            + readlines_for_index[index+1:])
            
            with open(self.normal_view, 'w', encoding='utf-8') as write_line:
                write_line.write(join_list)

    def word_changer(self, index: int, line: list[str]) -> None:
        change_word = input('Измененное написание: ').capitalize()
        change_translate = input('Измененный перевод: ').capitalize()
        
        if change_word != '' and change_translate != '':
            if change_word == '':
                change_word = line[0]
            elif change_translate == '':
                change_translate = line[1]
                
            change_str = f'{change_word}/{change_translate}/{line[-1]}\n'

            with open(self.normal_view, 'r', encoding='utf-8') as read_line:
                readlines_for_index = read_line.readlines()
                join_list = ''.join(readlines_for_index[:index]
                                + [change_str]
                                + readlines_for_index[index+1:])
                with open(self.normal_view, 'w', encoding='utf-8') as write_line:
                    write_line.write(join_list)

    def change_file(self, index: int, line: list[str]) -> None:
        pass

    @classmethod
    def find_engine(cls, func: Callable, key: str):
        word = UseFile.set_word()
        generator_st = UseFile.word_finder(word)
        generator_st.__next__().func(generator_st)

    @classmethod
    def engine(cls) -> None:
        """Это сердце программы.
        Здесь происходит координация циркуляции значений между файлами.
        """
        global_down_dict: dict = {}
        global_boost_dict: dict = {}
        
        for i in EndPoints.end_point_generator():
            word_dict, down_dict, boost_dict = cls(i).txt_reader() # txt_reader(path, i)
            
            if not (word_dict or down_dict or boost_dict):
                pass
            # Здесь разумно бы добавить небольлшую оптимизацию,
            # но я не понимаю, как бы это лучше сделать. При создании
            # ограничения файл не создается и не происходит запись в
            # global_boost_dict, содержимое его исчезает.

            cls(i).txt_clear()

            if i.struct != 1:
                global_down_dict.update(down_dict)
                word_dict.update(global_boost_dict)
                cls(i).txt_writer(word_dict)

                global_boost_dict.clear()
                global_boost_dict.update(boost_dict)

            else:
                global_down_dict.update(down_dict)
                global_down_dict.update(word_dict)
                global_boost_dict.update(boost_dict)
        else:
            cls(EndPoints(1)).txt_writer(global_down_dict)


    @staticmethod
    def call_hub(path: Optional[str], call_type: Optional[Callable]):
        if path is not None:
            UseFile.path = path
        if UseFile.directory_find():
            pass
            
    
    @staticmethod
    def directory_find(path: Callable = path) -> bool:
        """Проверка, что это linux или windows.
        И на присутствие скрытой директории,
        если не найдена -- создание.
        """
        if not os.path.exists(path):
            os.mkdir(path)
            if platform == "win32":
                win32api.SetFileAttributes(path, win32con.FILE_ATTRIBUTE_HIDDEN)
                return True
            elif platform == "linux" or platform == "linux2":
                return  True
            else:
                return False
        else:
            return True


def cmd_runner(path: Optional[str]) -> None:
    """
    Запускает нечто вроде командной строки.
    Временный интерфейс."""
    print("""berber learn v.t0.1.2
Список используемых команд:
- s_w: stop work;
- c_w: change word;
- d_w: delete word;
- c_p: control point.
""")
    
    cmd_dict: dict[str, Optional[Callable]] = {
        's_w': None,
        'c_w': UseFile.word_changer,
        'd_w': UseFile.word_deleter,
        'c_p': UseFile.engine,
    }

    count = 1
    while True:
        cmd_status = input('> ')
        
        if cmd_status in cmd_dict:
            if cmd_status is None:
                print('Завершение.')
                break
            else:
                UseFile.call_hub(path, cmd_dict[cmd_status])
                
    #     if cmd_status == '':
    #         if count > 0:
    #             engine(path)
    #             count -= 1
    #     elif (cmd_status.split()[0] == 'change_word' or cmd_status.split()[0] == 'c_w'):
    #         try:
    #             word_finder_ = word_finder(path, cmd_status.split()[1])
    #             if word_finder_ is not None:
    #                 word_changer(*word_finder_)
    #         except IndexError:
    #             print('Правильно испольлзовать так: c_w <изменяемое_слово>.')

    #     elif cmd_status == 'stop_work' or cmd_status == 's_w':
    #         break
    #     else:
    #         new_word_writer(path, cmd_status)
    # overwriting(path, EndPoints(0), EndPoints(1))

def main(path: str = './.txt_lib/') -> None:
    cmd_runner(path)

if __name__ == '__main__':
    path = './.txt_lib/'
    main()