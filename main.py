import os
from sys import platform
from typing import Generator, Optional, Self, Any

import win32con, win32api

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


def main() -> None:
    f_end_point: str = "./.txt_lib/"
    if directory_find(f_end_point):
        cmd_runner(f_end_point)

def directory_find(path: str) -> bool:
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

def cmd_runner(path: str) -> None:
    """Запускает нечто вроде командной строки.
    Временный интерфейс."""
    print("""berber learn v.0.1.1
Список используемых команд:
    - change_word(c_w) -- Изменяет или удаляет слово. Сразу через
пробел указывается изменяемое слово.
    - stop_work(s_w) -- Останавливает работу программы. Важно
останавливать программу именно так, иначе сохранятся не все данные!
    Чтобы добавить новое слово просто напиши его в командную строку.
Имей в виду, что при проверке первым выбирается именно слово, которое
было внесено в строку первым, не перевод. И кстати.
Счетчик сработывает при каждом запуске программы, поэтому советую
запускать не слишком часто.""")
    count = 1
    while True:
        cmd_status = input('> ')
        if cmd_status == '':
            if count > 0:
                engine(path)
                count -= 1
        elif (cmd_status.split()[0] == 'change_word' or cmd_status.split()[0] == 'c_w'):
            try:
                word_finder_ = word_finder(path, cmd_status.split()[1])
                if word_finder_ is not None:
                    word_changer(*word_finder_)
            except IndexError:
                print('Правильно испольлзовать так: c_w <изменяемое_слово>.')

        elif cmd_status == 'stop_work' or cmd_status == 's_w':
            break
        else:
            new_word_writer(path, cmd_status)
    overwriting(path, EndPoints(0), EndPoints(1))

def engine(path: str) -> None:
    """Это сердце программы.
    Здесь происходит координация циркуляции значений между файлами 
    """
    global_down_dict: dict = {}
    global_boost_dict: dict = {}
    
    for i in EndPoints.end_point_generator():
        word_dict, down_dict, boost_dict = txt_reader(path, i)
        if not (word_dict or down_dict or boost_dict):
            pass
        # Здесь разумно бы добавить небольлшую оптимизацию,
        # но я не понимаю, как бы это лучше сделать. При создании
        # ограничения файл не создается и не происходит запись в
        # global_boost_dict, содержимое его исчезает.

        txt_clear(path, i)

        if i.struct != 1:
            global_down_dict.update(down_dict)
            word_dict.update(global_boost_dict)
            txt_writer(path, i, word_dict)

            global_boost_dict.clear()
            global_boost_dict.update(boost_dict)

        else:
            global_down_dict.update(down_dict)
            global_down_dict.update(word_dict)
            global_boost_dict.update(boost_dict)
    else:
        txt_writer(path, EndPoints(1), global_down_dict)


def txt_read_and_split(path: str) -> list[list[str]]:
    """Превращает записи из файлов в списки значений."""
    with open(path, 'r', encoding='utf-8') as read_line:
        return [line.rstrip('\n').split('/') for line in  read_line.readlines()]

def txt_reader(path: str, end_point: EndPoints) -> Generator[dict[str, list], dict, None]:
    """Из названия функции не очень ясно, но она так же важна,
    как и engine. Здесь происходит чтение данных, 
    сортровка, отправка в engine.
    """
    max_value: int = end_point.struct
    word_dict: dict = {}
    down_dict: dict = {}
    boost_dict: dict = {}
    new_path: str = path + end_point.normal_view()

    if os.path.exists(new_path):
        tmp_dict: dict[str, list] = {i:[j, int(n)] for i, j, n in txt_read_and_split(new_path)}

        for i in tmp_dict:
            if tmp_dict[i][1] == 0:
                input_translatte = input(f'Translate {i} is: ')
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

def txt_writer(path: str, end_point: EndPoints, inp_dict: dict) -> None:
    """Запись в файл."""
    new_path: str = path + end_point.normal_view()
    with open(new_path, 'w', encoding='utf-8') as write_line:
        for item in inp_dict:
            write_line.write(f'{item}/{inp_dict[item][0]}/{inp_dict[item][1]}\n')

def txt_clear(path: str, end_point: EndPoints) -> None:
    """Очистка файла."""
    new_path: str = path + end_point.normal_view()

    with open(new_path, 'w') as write_line:
        write_line.write('')

def overwriting(path: str, end_point_1: EndPoints, end_point_2: EndPoints) -> None:
    """Переписывание одного файла полностью в другой."""
    new_path_1: str = path + end_point_1.normal_view()
    new_path_2: str = path + end_point_2.normal_view()
    with open(new_path_1, 'r', encoding='utf-8') as read_line, \
            open(new_path_2, 'a', encoding='utf-8') as write_line:
        write_line.write(read_line.read())
    txt_clear(path, end_point_1)

def new_word_writer(path: str, word: str) -> None:
    """"Функция записи новых ппар слов в словарь."""
    new_path: str = path + EndPoints(0).normal_view()
    translation: str = input('Перевод: ')
    if translation != '':
        with open(new_path, 'a', encoding='utf-8') as write_line:
            write_line.write(f'{word.capitalize()}/{translation.capitalize()}/1\n')

def word_changer(path: str, index: int, count: Optional[int] = None) -> None:
    """Функции изменения вынесены на особицу,
    они не вызываются из engine.
    Данная функция изменяет или удаляет значение из словаря."""
    cmd_status: str = input('What you do with this word? [del/change] ')

    if cmd_status == 'del' or cmd_status == 'd':
        with open(path, 'r', encoding='utf-8') as read_line:
            readlines_for_index = read_line.readlines()
            join_list = ''.join(readlines_for_index[:index]
                            + readlines_for_index[index+1:])
            with open(path, 'w', encoding='utf-8') as write_line:
                write_line.write(join_list)

    elif cmd_status == 'change' or cmd_status == 'c':
        c_word = input('Измененное написание: ').capitalize()
        c_translate = input('Измененный перевод: ').capitalize()
        if c_word != '' and c_translate != '':
            change_str = f'{c_word}/{c_translate}/{count}\n'

            with open(path, 'r', encoding='utf-8') as read_line:
                readlines_for_index = read_line.readlines()
                join_list = ''.join(readlines_for_index[:index]
                                + [change_str]
                                + readlines_for_index[index+1:])
                with open(path, 'w', encoding='utf-8') as write_line:
                    write_line.write(join_list)
    else:
        print(f'The flag {cmd_status} not exsist.')
            
def word_finder(path: str, word: str) -> Generator[Any, Any, None]:
    """Поиск слова по всем файлам.
    Как само слово, так и перевод.
    """
    word = word.capitalize()
    for i in EndPoints(0), *EndPoints.end_point_generator():
        new_path: str = path + i.normal_view()
        spliting_file = txt_read_and_split(new_path)
        
        for line in spliting_file:
            if line[0] == word or line[1] == word:
                yield from (
                    new_path,
                    spliting_file.index(line), 
                    int(line[2]),
                    )
            else:
                return
    else:
        print(f'{word} word not exist.')

if __name__ == '__main__':
    main()