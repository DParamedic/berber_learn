import os
from sys import platform
from typing import TypeVar, Union, Generator

import win32con, win32api

path_to_file = TypeVar('pathlib.Path')
end_point_type = TypeVar('EndPoints')

def main() -> None:
    f_end_point = "./.txt_lib/"
    if directory_find(f_end_point):
        cmd_runner(f_end_point)

def directory_find(path: Union[str, path_to_file]) -> bool:
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
    
def cmd_runner(path: Union[str, path_to_file]) -> None:
    while True:
        cmd_status = input('> ')
        if cmd_status == '':
            engine(path)
        elif cmd_status == 'stop_work':
            break
        else:
            new_word_writer(path, cmd_status)
    overwriting(path)
    
def engine(path: Union[str, path_to_file]) -> None:
    global_down_dict, global_boost_dict = {}, {}
    
    for i in end_point_generator():
        word_dict, down_dict, boost_dict = txt_reader(path, i)
        if not (word_dict or down_dict or boost_dict):
            pass
        # It would be correct to introduce micro-optimization, but it is still difficult to figure out how to do it correctly, because when creating a restriction, the file is not created for writing and the contents of the global_boost_dict disappear.
        
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


def txt_reader(path: Union[str, path_to_file], end_point: end_point_type) -> tuple[dict]:
    max_value = end_point.struct
    word_dict = {}
    down_dict = {}
    boost_dict = {}
    new_path = path + end_point.normal_view()
    
    if os.path.exists(new_path):
        with open(new_path, 'r', encoding='utf-8') as read_line:
            tmp_dict = {i:[j, int(n)] for i, j, n in [line.split('/') for line in read_line]}
            
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
                    down_dict[i] = tmp_dict[i][0], 1
                elif tmp_dict[i][1] > max_value:
                    boost_dict[i] = tmp_dict[i]
                else:
                    word_dict[i] = tmp_dict[i]
                    
        return word_dict, down_dict, boost_dict
    else: 
        return {}, {}, {}

def txt_writer(path: Union[str, path_to_file], end_point: end_point_type, inp_dict: dict) -> None:
    new_path = path + end_point.normal_view()
    with open(new_path, 'w', encoding='utf-8') as read_line:
        for item in inp_dict:
            read_line.write(f'{item}/{inp_dict[item][0]}/{inp_dict[item][1]}\n')

def txt_clear(path: Union[str, path_to_file], end_point: end_point_type) -> None:
    new_path = path + end_point.normal_view()
    
    with open(new_path, 'w') as write_line:
        write_line.write('')

def overwriting(path: Union[str, path_to_file], end_point_1: end_point_type=EndPoints(0), end_point_2: end_point_type=EndPoints(1)) -> None:
    new_path_1 = path + end_point_1.normal_view()
    new_path_2 = path + end_point_2.normal_view()
    with open(new_path_1, 'r', encoding='utf-8') as read_line, \
            open(new_path_2, 'a', encoding='utf-8') as write_line:
        for line in read_line:
            write_line.write(line)
    txt_clear(path, end_point_1)

def new_word_writer(path: Union[str, path_to_file], word: str) -> None:
    new_path = path + EndPoints(0).normal_view()
    translation = input('Перевод: ')
    if translation != '':
        with open(new_path, 'a', encoding='utf-8') as write_line:
            write_line.write(f'{word.capitalize()}/{translation.capitalize()}/1\n')


class EndPoints:
    def __init__(self, struct: int, expansion='.txt'):
        self.expansion = expansion
        self.struct = struct
        self = struct, expansion
    def normal_view(self) -> str:
        return str(self.struct) + self.expansion
    def __eq__(self, other):
        return self.struct == other.struct and self.expansion == other.expansion
    
def end_point_generator(limiter: int=12, start: int=1, degree: int=2) -> Generator:
    for i in range(limiter):
        yield EndPoints(start)
        start *= degree
            
if __name__ == '__main__':
    main()