import os
import win32con, win32api
from sys import platform


file_name = "./.txt_lib/"

def directory_find(path):
    if not os.path.exists(path):
        os.mkdir(path)
        if platform == "win32":
            win32api.SetFileAttributes(path, win32con.FILE_ATTRIBUTE_HIDDEN)
        elif platform == "linux" or platform == "linux2":
            continue
        else:
            exit(1)

def txt_reader(path):
    max_value = int(path.split('/')[-1].split('.')[0])
    word_dict = {}
    down_dict = {}
    boost_dict = {}
    
    with open(path, 'r') as read_line:
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

def enine():
    end_point_list = ["./.txt_lib/", "1.txt", '2.txt', '4.txt', '8.txt', '16.txt', '32.txt', '64.txt', '128.txt', '256.txt', '512.txt', '1024.txt', '2048.txt']
    for i in end_point_list[1:]:
        word_dict, down_dict, boost_dict = txt_reader(end_point_list[0]+i)
        # writer