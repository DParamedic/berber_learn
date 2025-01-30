import os
import win32con, win32api
from sys import platform

class EndPoints:
    def __init__(self, struct: int, expansion='.txt'):
        self.expansion = expansion
        self.struct = struct
        self = struct, expansion
    def normal_view(self):
        return str(self.struct) + self.expansion
    
def directory_find(path):
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
    
def txt_reader(path, end_point):
    max_value = end_point.struct
    word_dict = {}
    down_dict = {}
    boost_dict = {}
    new_path = path + end_point.normal_view()
    
    with open(new_path, 'r') as read_line:
        word_dict = {i:[j, n] for i, j, n in [line.split('/') for line in read_line]}
        
        for i in word_dict:
            word_dict_i = word_dict[i]
            if word_dict_i[1] == 0:
                input_translatte = input(f'Translate {i} is: ')
                if input_translatte == word_dict_i[0]:
                    print('Прекрасно!')
                    word_dict_i[1] = max_value*2
                else:
                    print(f'Нет. Правильно: {word_dict_i[0]}')
                    word_dict_i[1] = None
            else: word_dict_i[1] -= 1
            
        for i in word_dict:
            word_dict_i = word_dict[i]
            if word_dict_i[1] is None:
                down_dict[i] = word_dict_i[1], 1
                del word_dict_i
            elif word_dict_i[1] > max_value:
                boost_dict[i] = word_dict_i
                del word_dict_i
                
    return word_dict, down_dict, boost_dict

def end_point_generator(limiter: int=12, start: int=1, degree: int=2):
    for i in range(limiter):
        yield EndPoints(start)
        start *= degree
            
def txt_clear(path, end_point):
    new_path = path + end_point.normal_view()
    
    with open(new_path, 'w') as write_line:
        write_line.write('')

def txt_writer(path, end_point, inp_dict):
    pass

def engine():
    f_end_point = "./.txt_lib/"
    if directory_find(f_end_point):
        global_down_dict, global_boost_dict = {}, {}
        
        for i in end_point_generator():
            word_dict, down_dict, boost_dict = txt_reader(f_end_point, i)
            txt_clear(f_end_point, i)
            
            if i.struct != 1:
                global_down_dict.update(down_dict)
                txt_writer(f_end_point, i, word_dict.update(global_boost_dict))
                
                # word_dict.clear()
                global_boost_dict.clear()
                # down_dict.clear()
                
                global_boost_dict.update(boost_dict)
                
            else:
                global_down_dict.update(down_dict)
                global_down_dict.update(word_dict)
                global_boost_dict.update(boost_dict)
        else:
            txt_writer(f_end_point, EndPoints(1), global_down_dict)
            