import pandas as pd
import numpy as np
import os
import sys
import pickle
import argparse
import glob

from write_excel import *
from item_object import *
import write_pdf

PATH_GRAPH = './graph'
PATH_TEMP = './temp'
# OUTPUT_EXCEL = r'c:\\output_excel'
# OUTPUT_PDF = r'c:\\output_pdf'
OUTPUT_EXCEL = r'c:\\Temp\\output_excel'
OUTPUT_PDF = r'c:\\Temp\\output_pdf'
OUTPUT_FINAL = r'c:\\Temp\\output_final'

FIND_OBJ_NAME = 0
SECTION_PROCESSING = 1
SUMMARY_PROCESSING = 2
LOCATE_PROCESSING = 3
SPACE_PROCESSING = 4

TOOLS_AND_INVOCATION = 'Tool and Invocation'
USED_RESOURCES = 'Used Resources'
MEMORY_USAGE_IN_BYTES = 'Memory usage in bytes'
SPACE_USAGET_IN_BYTES = 'Space usage in bytes'
ESTIMATED_STACK_USAGE = 'Estimated stack usage'
PROCESSED_FILES = 'Processed Files'
LINK_RESULT = 'LINK_RESULT'
CROSS_REFERENCE = 'Cross References'
CALL_GRAPH = 'Call Graph'
LOCATE_RESULT = 'Locate Result'
SECTIONS = '* Sections'
LOCATE_RULES = 'Locate Rules'
REMOVE_SECTIONS = 'Removed Sections'
SPACE_LOCATE = '+ Space'
END_SPACE_LOCATE = '* Symbols'

ELEMENT_NAME = 'mpe'
SEPERATORS = ['---', '* Symbols', '* Space usage in bytes']

# Data keyword
keyword_space = ['Chip', 'Group', 'Section',
                 'Size (MAU)', 'Space addr', 'Chip addr', 'Alignment']

# Summary keyword
keyword = ['Memory', 'Code', 'Data']


# section_space_name = {}
section_space_name = []
global_space_name = ''
space_name = []

array_space_names = []
index_array_space_names = -1

# 특수 문자 제거해서 txt 파일로 저장


class Map:
    f_name = ''
    input_ext = '.map'
    output_ext = '.txt'
    input_file = f_name
    output_file = f_name
    start_FIRST = False
    start_obs_name_section = False
    section_pos = [0, 0]
    summary_pos = [0, 0]
    locate_pos = [0, 0]
    obj_name = []
    section_area = []
    summary_area = []
    locate_area = []
    space_area = []
    space_area_index = []
    item_list = []
    space_header_list = []

    def __init__(self, filename):

        self.f_name = ''
        self.input_ext = '.map'
        self.output_ext = '.txt'
        self.input_file = self.f_name
        self.output_file = self.f_name
        self.start_FIRST = False
        self.start_obs_name_section = False
        self.section_pos = [0, 0]
        self.summary_pos = [0, 0]
        self.locate_pos = [0, 0]
        self.obj_name = []
        self.section_area = []
        self.summary_area = []
        self.locate_area = []
        self.space_area = []
        self.space_area_index = []
        self.item_list = []
        self.space_header_list = []
        self.tool_name = ''

        self.f_name = os.path.splitext(filename)[0]
        self.input_file = self.f_name + self.input_ext
        self.output_file = self.f_name + self.output_ext
        try:
            if not os.path.exists(PATH_TEMP):
                os.makedirs(PATH_TEMP)
            if not os.path.exists(PATH_GRAPH):
                os.makedirs(PATH_GRAPH)
        except OSError:
            print('Error : Failed to create GRAPH directory')
        # print(f'input_file :{self.input_file}')
        # print(f'output_file :{self.output_file}')

    def _select_tool_name(self):
        try:
            f = open(self.input_file, 'r')
        except Exception as e:
            print(f'{self.input_file} is NOT exist')
        else:
            lines = f.readlines()
            max_line = len(lines)

        temp_tool_names = []
        index_line = 0
        while index_line < max_line:
            line = lines[index_line]
            if line.find('| tool') >= 0:
                temp_tool_names = line.split('|')
                break
            index_line += 1
        self.tool_name = temp_tool_names[2].lstrip().rstrip()
        # print(f'[12/22] self.tool_name : {self.tool_name}')

    def _select_section(self, action):
        global section_space_name
        global global_space_name
        global space_name

        section_start = False

        try:
            f = open(self.input_file, 'r')
        except Exception as e:
            print(f'{self.input_file} is NOT exist')
        else:

            lines = f.readlines()
            max_line = len(lines)
            done = False
            section_start_pos_enable = False
            section_pos = [0, 0]
            index_line = 0
            if action == SECTION_PROCESSING:
                search_start_point = SECTIONS
                seperator = SEPERATORS[1]
            elif action == SUMMARY_PROCESSING:
                search_start_point = MEMORY_USAGE_IN_BYTES
                seperator = SEPERATORS[2]
            elif action == LOCATE_PROCESSING:
                search_start_point = LOCATE_RESULT
                seperator = SEPERATORS[1]
            elif action == SPACE_PROCESSING:
                search_start_point = SPACE_LOCATE
                seperator = SEPERATORS[1]

            while index_line < max_line:

                index_space_name = 0
                line = lines[index_line]
                if line.find(search_start_point) >= 0 and section_start == False:
                    section_start = True
                    # if action == SPACE_PROCESSING:
                    # space_header = line.split(' ')[2]
                    # self.space_header_list.append(space_header)
                    #print(f'[space_header] : {space_header}')

                elif section_start == True:
                    # print(f'[{index_line}] : {line}')

                    if self._check_special_char(line) == False:
                        # print(f'line[0] : {line[0]}')

                        while not done and index_line < max_line - 1 and section_start == True:
                            index_line += 1
                            line = lines[index_line]
                            # or line.find(END_SPACE_LOCATE) < 0:
                            if line.find(search_start_point) < 0:
                                if line.find('+ Space') >= 0:
                                    space_list = line.split()
                                    space_name_data = [
                                        index_line, space_list[2]]
                                    # print(
                                    #     f'[12-07] space_name_data : {space_name_data[1]}')
                                    if space_name_data not in space_name:
                                        space_name.append(space_name_data)
                                        # print(f'space_name :{space_name}')
                                        #global_space_name = space_name[1]
                                        index_space_name += 1
                                    continue
                                if self._check_special_char(line) == False:

                                    # if line.find('+ Space') >= 0:
                                    #     space_list = line.split()
                                    #     space_name_data =  [index_line, space_list[2]]
                                    #     if space_name_data not in space_name:
                                    #         space_name.append(space_name_data)
                                    #         #print(f'space_name :{space_name}')
                                    #         #global_space_name = space_name[1]
                                    #         index_space_name += 1
                                    #     continue
                                    if line.find(ELEMENT_NAME + ':') >= 0 and done == False:
                                        #print(f'[{index_line}] : {line}')
                                        if section_start_pos_enable == False:
                                            #print('section_start_pos_enable = True')
                                            section_pos[0] = index_line
                                            section_start_pos_enable = True
                                            #print(f'section start pos : {section_pos[0]}')
                                        line = line.strip(' ')
                                        line = line.strip('\n')
                                        if action == SECTION_PROCESSING:
                                            self.section_area.append(
                                                line.replace(' ', '').split('|'))
                                        elif action == SUMMARY_PROCESSING:
                                            self.summary_area.append(
                                                line.replace(' ', '').split('|'))
                                        elif action == LOCATE_PROCESSING:
                                            check_num_elem = line.split(
                                                '|')
                                            print(
                                                f'[03/18] check_num_elem : {len(check_num_elem)}')
                                            if len(check_num_elem) >= 6:
                                                #self.locate_area.append(line.replace(' ', '').split('|'))
                                                next_line = lines[index_line + 1]
                                                if next_line.find('mpe:') < 0 and self._check_special_char(next_line) == False:
                                                    # print(f'LOCATE_PROCESSING [ w/o mpe: ] line : {line}')
                                                    # print(f'LOCATE_PROCESSING [ w/o mpe: ] next line : {next_line}')
                                                    line_data = self.make_double_lines(
                                                        line, next_line)

                                                    # self.space_area.append(line_data)
                                                    # self.space_area_index[line_data] = index_line
                                                    index_line += 1
                                                elif next_line.find('mpe:') > 0 and self._check_special_char(next_line) == False and self.is_size_mau(next_line) == False:
                                                    # print(f'LOCATE_PROCESSING [ DOULBE_LINE ] line : {line}')
                                                    # print(f'LOCATE_PROCESSING [ DOULBE_LINE ] next line : {next_line}')
                                                    line_data = self.make_double_lines(
                                                        line, next_line)

                                                    # self.space_area.append(line_data)
                                                    # self.space_area_index[line_data] = index_line
                                                    index_line += 1
                                                elif next_line.find('mpe:') > 0 and self.is_double_chip(next_line) == True:
                                                    # print(f'LOCATE_PROCESSING [ DOULBE_CHIP ] line : {line}')
                                                    # print(f'LOCATE_PROCESSING [ DOULBE_CHIP ] next line : {next_line}')
                                                    line_data = self.make_double_chip(
                                                        line, next_line)
                                                    # print(f'double line_data : {line_data}')
                                                    index_line += 1
                                                elif next_line.find('mpe:') > 0 and self._check_special_char(next_line) == False and self.is_size_mau(next_line) == True:
                                                    # print(f'LOCATE_PROCESSING line : {line}')
                                                    # print(f'LOCATE_PROCESSING next line : {next_line}')
                                                    line_data = self.make_one_line(
                                                        line)

                                                    # self.space_area.append(line_data)
                                                    # self.space_area_index[line_data] = index_line

                                                else:
                                                    line_data = self.make_one_line(
                                                        line)

                                                #converted_data = self.abnormal_addr_convert(line_data)
                                                self.locate_area.append(
                                                    line_data)

                                                # next_line_index = space_name[1][0]
                                                i = 0
                                                while i < (len(space_name) - 1):

                                                    if space_name[i][0] <= index_line and space_name[i+1][0] > index_line:
                                                        section_space_name.append(
                                                            [index_line, space_name[i][1], line])
                                                        self.space_area_index.append(
                                                            [index_line, space_name[i][1], line_data])
                                                        break
                                                    i += 1
                                                    # elif space_name[i+1][0] < index_line:
                                                    #     continue
                                                if i == len(space_name) - 1:
                                                    section_space_name.append(
                                                        [index_line, space_name[i][1], line])
                                                    self.space_area_index.append(
                                                        [index_line, space_name[i][1], line_data])
                                                # print(
                                                    # f'[12/07] size of space name : {len(section_space_name)}')
                                        elif action == SPACE_PROCESSING:

                                            # if index_line + 1 < max_line - 1:
                                            next_line = lines[index_line + 1]
                                            # if "APP_ISR_RAMCODE_group" in line:
                                            #     print(line)
                                            if next_line.find('mpe:') < 0 and self._check_special_char(next_line) == False:
                                                line_data = self.make_double_lines(
                                                    line, next_line)
                                                # print(f'[12/24 (mpe:) < 0] double line :{line_data}')
                                                # print(concat_line_list)
                                                # self.space_area.append(line_data)
                                                # self.space_area_index[line_data] = index_line
                                                index_line += 1
                                            elif next_line.find('mpe:') > 0 and self.is_double_chip(next_line) == True:
                                                line_data = self.make_double_chip(
                                                    line, next_line)
                                                # print(f'[12/24 (mpe:) > 0] double line :{line_data}')
                                                index_line += 1
                                            elif next_line.find('mpe:') > 0 and self._check_special_char(next_line) == False and self.is_size_mau(next_line) == False:
                                                line_data = self.make_double_lines(
                                                    line, next_line)
                                                # print(f'[12/24 _check_special_char(next_line) == False and self.is_size_mau(next_line) == False ] double line :{line_data}')
                                                # print(concat_line_list)
                                                # self.space_area.append(line_data)
                                                # self.space_area_index[line_data] = index_line
                                                index_line += 1

                                            elif next_line.find('mpe:') > 0 and self._check_special_char(next_line) == False and self.is_size_mau(next_line) == True:
                                                # print(f'SPACE_PROCESSING line : {line}')
                                                # print(f'SPACE_PROCESSING next line : {next_line}')
                                                line_data = self.make_one_line(
                                                    line)
                                                # print(f'[12/24 _check_special_char(next_line) == False and self.is_size_mau(next_line) == True ] double line :{line_data}')
                                                # self.space_area.append(line_data)
                                                # self.space_area_index[line_data] = index_line

                                            else:
                                                line_data = self.make_one_line(
                                                    line)

                                            self.space_area.append(line_data)

                                            # if "APP_ISR_RAMCODE_group" in line_data:
                                            #     print(self.space_area)

                            if line.find(seperator) >= 0 and section_start_pos_enable == True:
                                #print(f'end pos line : {index_line}')
                                section_pos[1] = index_line
                                #print(f'section end pos : {section_pos[1]}')
                                section_start_pos_enable == False
                                done = True
                                # print(f'SPACE_NAME : {space_name}')
                                # if action == LOCATE_PROCESSING:
                                #     print(f'CURRENT INDEX_LINE : {index_line}')
                                #     print(f'self.space_area_index : {self.space_area_index[len(self.space_area_index) - 1]}')
                                #print('section_start_pos_enable = False')
                index_line += 1
            df = pd.DataFrame(data=section_space_name, columns=[
                              'index', 'space_name', 'line'])
            df.to_csv(PATH_TEMP + '/global_space.csv')
            # space_area_df = pd.DataFrame(data = self.space_area )
            # space_area_df.to_csv('./space_area.csv')
            return section_pos

    def is_size_mau(self, line_2):
        str_line_2 = line_2.replace(' ', '')
        list_line_2 = str_line_2.split('|')
        if list_line_2[4] == '':
            return False
        else:
            return True

    # modified by 25_step.py
    def make_double_lines(self, line_1, line_2):

        str_line_1 = line_1.replace(' ', '')
        str_line_2 = line_2.replace(' ', '')

        print(f'[03/18] str_line_1 : {str_line_1}')
        print(f'[03/18] str_line_2 : {str_line_2}')

        list_line_1 = str_line_1.split('|')
        list_line_2 = str_line_2.split('|')
        # print(f'line_1 : {list_line_1}')
        # print(f'line_2 : {list_line_2}')
        # if len(list_line_1) < 4 or len(list_line_2) < 4:
        #     print(f'list_1 : {line_1}')
        #     print(f'list_2 : {line_2}')
        if list_line_2[1] != '' and list_line_2[1] != '':
            list_line_1[1] = list_line_1[1] + list_line_2[1]
            # list_line_1[1] = list_line_1[1] + list_line_2[1]
        if list_line_1[2] != '' and list_line_2[2] != '':
            list_line_1[2] = list_line_1[2] + list_line_2[2]

        if list_line_1[3] != '' and list_line_2[3] != '':
            list_line_1[3] = list_line_1[3] + list_line_2[3]

        convert_data = list_line_1[3].split('(')
        list_line_1[3] = convert_data[0]
        print(f'[03/18] len list_line_1 : {len(list_line_1)}')
        print(f'[03/18] len list_line_2 : {len(list_line_2)}')
        if len(list_line_2[6]) >= 0:
            chip_addr = list_line_1[6].split('+')
            list_line_1[6] = chip_addr[0]
            # print(f'double_lines_1[1] : {list_line_1[1]}')
            # print(f'double_lines_1[2] : {list_line_1[2]}')
            # print(f'double_lines_1[3] : {list_line_2[3]}')
            # print(f'double_lines_1[4] : {list_line_1[4]}')
            # print(f'double_lines_1[5] : {list_line_1[5]}')
            # print(f'double_lines_1[6] : {list_line_1[6]}')
        # print(f'[12/24 make_double_lines] : {list_line_1}')
        return list_line_1

    def is_double_chip(self, line_2):
        str_line_2 = line_2.replace(' ', '')
        list_line_2 = str_line_2.split('|')

        if list_line_2[3] == '' and list_line_2[6] != '':
            return True
        else:
            return False

    def make_double_chip(self, line_1, line_2):
        # print(f'[12/24] make_double_chip')
        concat_str = ''
        str_line_1 = line_1.replace(' ', '')
        str_line_2 = line_2.replace(' ', '')

        list_line_1 = str_line_1.split('|')
        list_line_2 = str_line_2.split('|')
        # if list_line_1[4] == '':
        #     print(f'doule chip line_1[1] : {list_line_1[0]}')
        #     print(f'doule chip line_1[3] : {list_line_1[3]}')
        #     print(f'doule chip line_1[4] : {list_line_1[4]}')
        #     print(f'doule chip line_1[5] : {list_line_1[5]}')
        #     print(f'doule chip line_1[6] : {list_line_1[6]}')
        if list_line_2[4] == '':
            # print()
            if len(list_line_2[6]) >= 0:
                chip_addr = list_line_1[6].split('+')
                list_line_1[6] = chip_addr[0]
            # print(f'doule chip line_1[6] : {list_line_1[6]}')
            # print(f'doule chip line_2[6] : {list_line_2[6]}')

            # if len(list_line_1) < 4 or len(list_line_2) < 4:
            #     print(f'list_1 : {line_1}')
            #     print(f'list_2 : {line_2}')

            # list_line_1[1] = list_line_1[1] + '+' + list_line_2[1]
            list_line_1[1] = list_line_1[1] + list_line_2[1]
            list_line_1[3] = list_line_1[3] + list_line_2[3]
            convert_data = list_line_1[3].split('(')
            list_line_1[3] = convert_data[0]
            # chip_addr = list_line_1[6].split('+')
            # list_line_1[6] = chip_addr[0]
            # print(f'doule chip line_1[1] : {list_line_1[1]}')
            # print(f'doule chip line_1[2] : {list_line_1[2]}')
            # print(f'doule chip line_1[3] : {list_line_2[3]}')
            # print(f'doule chip line_1[4] : {list_line_1[4]}')
            # print(f'doule chip line_1[5] : {list_line_1[5]}')
            # print(f'doule chip line_1[6] : {list_line_1[6]}')
        # print(f'[make_double_CHIP] : {list_line_1}')
        return list_line_1

    # modified by 25_step.py
    def make_one_line(self, line_1):
        # if line_1.find('dflash0') != -1:
        #     print(line_1)
        str_line = line_1.replace(' ', '')
        # str_line = str_line.replace('[', '')
        # str_line = str_line.replace(']', '')
        #print(f'[make_ONE_LINE] : {str_line}')
        list_line = str_line.split('|')
        # if str_line.find('.bss.IFX_ILLD') >= 0:
        #     print(f'[make_one_line] : {list_line}')
        convert_data = list_line[3].split('(')
        list_line[3] = convert_data[0]

        # for item in list_line:
        #     convert_data += item

        # print(str_line_1)
        # print(concat_str)
        # if list_line[3] == '.bss.IFX_ILLD':
        # if list_line[3].find('.bss.IFX_ILLD') >= 0:
        #     print(f'[make_one_line] : {list_line}')
        return list_line

    def _check_special_char(self, line_str):
        if line_str.find('+ Space') >= 0:
            return False
        else:
            if line_str[0] == ' ' or line_str[0] == '+' or line_str[0] == '=' or line_str[0] == '*' or line_str.find('===') >= 0:
                return True
            else:
                return False

    def _check_space_line(self, line_str, spacename):
        if line_str.find(spacename) >= 0:
            return False
        else:
            return True

    def _find_obj_name(self):
        ongoing = True
        try:
            f = open(self.input_file, 'r')
        except Exception as e:
            print(f'{self.input_file} is NOT exist')
        else:
            lines = f.readlines()
            max_lines = len(lines)
            #print(f'max_lines {max_lines}')

            index_line = 0
            while ongoing and index_line < max_lines:
                line = lines[index_line]

                if line.find(TOOLS_AND_INVOCATION) >= 0:
                    self.start_FIRST = True
                else:
                    sep_position = line.find(SEPERATORS[0])
                    obj_position = line.find('.o')
                    if sep_position >= 0 and self.start_FIRST == True and self.start_obs_name_section == False:
                        self.start_obs_name_section = True
                    elif sep_position >= 0 and self.start_FIRST == True and self.start_obs_name_section == True:
                        ongoing = False
                    elif sep_position < 0 and self.start_FIRST == True and self.start_obs_name_section == True:
                        if line.find('.o') < 0:
                            pass
                        else:
                            obj_name = self._get_obj_name_section(line)
                            self.obj_name.append(obj_name + '.o')

                index_line += 1

    def _get_obj_name_section(self, line_str):
        characters = "*-=+|"
        obj_name = ''
        for x in range(len(characters)):
            path_str = line_str.replace(characters[x], "")
            basename = os.path.basename(path_str)
            obj_name = os.path.splitext(basename)[0]

        return obj_name

    def _str_to_hex(self, hex_str):
        a = int(hex_str, 16)
        hex_n = hex(a)
        return a

    def run(self, action):
        global space_area_index
        # global section_space_name
        # global global_space_name
        # global space_name

        # section_space_name = []
        # global_space_name = ''
        # space_name = []
        # space_area_index = []
        # self._find_obj_name()

        if action == FIND_OBJ_NAME:
            self._find_obj_name()
            # print()
            # print(f'obj_name : {self.obj_name}')
        elif action == SECTION_PROCESSING:
            self.section_pos = self._select_section(action)
            # df = pd.DataFrame(data=self.section_area, columns=[
            #   'WS_1', 'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Chip addr', 'Alignment', 'WS_2'])
            # print()
            # print(TOOLS_AND_INVOCATION)
            # print(df)
        elif action == SUMMARY_PROCESSING:
            self.summary_pos = self._select_section(action)
            self.summary_df = pd.DataFrame(data=self.summary_area, columns=[
                                           'WS_1', 'Memory', 'Code', 'Data', 'Reserved', 'Free', 'Total', 'WS_2'])
            for i in range(self.summary_df.shape[0]):
                if self.summary_df.iloc[i]['Memory'] == 'mpe:brom':
                    pass
                else:
                    self.item_list.append(self.summary_df.iloc[i]['Memory'])

            print()
            # print(MEMORY_USAGE_IN_BYTES)
            # print(self.item_list)
            # self.summary_df.to_csv('1213.csv')

        elif action == LOCATE_PROCESSING:
            self.locate_pos = self._select_section(action)
            self.locate_df = pd.DataFrame(data=self.locate_area, columns=[
                                          'WS_1', 'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Chip addr', 'Alignment', 'WS_2'])
            sorted_locate_df = self.locate_df.sort_values(
                by=["Space addr"], ascending=[True])
            opt_locate_df = sorted_locate_df.loc[:, [
                'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Chip addr', 'Alignment']]
            opt_locate_df.reset_index(inplace=True, drop=True)
            opt_locate_df.to_csv(PATH_TEMP + '/locate.csv', mode='w')
            space_area_index = self.space_area_index
            # print(f'space_are_index size : {len(space_area_index)}')
            self.preprocess_abnormal_addr()
            # print()
            # print(LOCATE_RULES)
            # print(self.locate_df)
        elif action == SPACE_PROCESSING:
            self.space_pos = self._select_section(action)
            self.space_df = pd.DataFrame(data=self.space_area, columns=[
                                         'WS_1', 'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Chip addr', 'Alignment', 'WS_2'])
            # self.space_df.to_csv('self_space_df.csv')
            # space_area_index = self.space_area_index
            # print(f'space_are_index size : {len(space_area_index)}')
            #self.space_index_df = pd.DataFrame(data = self.space_area_index, columns=['WS_1','line','index', 'WS_2'])
            # print()
            # print(SPACE_LOCATE)
            # print(self.space_df)

    def preprocess_abnormal_addr(self):
        new_data = []
        converted_data_list = []
        file_name = PATH_TEMP + '/locate.csv'
        locate_df = pd.read_csv(file_name)
        locate_list = locate_df.values.tolist()
        for i in range(len(locate_list)):
            new_data = locate_list[i]
            #print(f'[Excel] : {new_data}')
            new_data.append(abnormal_addr_convert(locate_list[i][5]))
            converted_data_list.append(new_data)
            #print(f'[Excel] : {new_data}')
        #print(f'converted_data_list : {converted_data_list[0]}')
        converted_df = pd.DataFrame(data=converted_data_list, columns=[
                                    'WS_1', 'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Chap addr', 'Alignment', 'converted'])
        converted_df = converted_df.sort_values(
            by=["converted"], ascending=[True])
        converted_df.reset_index(inplace=True, drop=True)
        converted_df.to_csv(PATH_TEMP + '/locate2.csv', mode='w')


def abnormal_addr_convert(data):
    convert_str = ''
    if type(data) == str:
        data_1 = int(data, 16)
    else:
        temp_data = str(data)
        data_1 = int(temp_data, 16)
    mask = int('0x7FFFFFFF', 16)
    data_2 = int('0x70000000', 16)
    data_3 = (data_1 & mask) | data_2

    #convert_str += str(data_3)

    return hex(data_3)


def gap_calculattion(test_map, index_item, name, mem_size, mem_addr, free):

    sum_gap = min_gap = max_gap = 0

    # if (name == 'dspr0'):
    locate_df = pd.read_csv(PATH_TEMP + '/locate2.csv')
    df = locate_df.loc[locate_df['Chip'].str.contains(name)]
    df.reset_index(inplace=True, drop=True)
    searched_df = df.loc[:, ['Group', 'Section',
                             'Size (MAU)', 'Space addr', 'Alignment', 'converted']]
    mem_size_list = mem_size
    mem_addr_list = mem_addr

    leng_df = searched_df.shape[0]
    gap_list = [0 for i in range(leng_df)]
    gap_list_hex = [0 for i in range(leng_df)]
    # print('--------------- gap_2 cal ------------------')
    # print()
    index = 0
    # for i in range(searched_df.shape[0] - 1):
    while index < (leng_df - 1):
        # if i > 6:
        #     break;
        mem_addr_1st = mem_addr_2nd = mem_addr_3rd = []

        mem_addr_1st = searched_df.loc[index, ['Size (MAU)']].tolist()
        mem_addr_2nd = searched_df.loc[index, ['converted']].tolist()
        mem_addr_3rd = searched_df.loc[index+1, ['converted']].tolist()
        section = searched_df.loc[index, ['Section']].tolist()

        value_1 = int(mem_addr_1st[0], 16)
        value_2 = int(mem_addr_2nd[0], 16)
        value_3 = int(mem_addr_3rd[0], 16)

        value = value_3 - (value_2 + value_1)
        if value < 20000 and value > 0:

            # print(f'value_3 - value_2 + value_1 =  : {mem_addr_3rd[0]} -{mem_addr_2nd[0]} + {mem_addr_1st[0]} = {value} ')
            # print(f'value_3 - value_2 + value_1 =  : {value_3} -{value_2} + {value_1} = {value} ')

            # if i % 10 == 0:
            # if value != 0:
            #     str = '1st, 2nd, 3rd, 3rd-(1st + 2nd) : {0:x}, {1:x}, {2:x},{3:x}'.format(value_1, value_2, value_3, value )
            #     f = open('gap.txt','a')
            #     f.write(str + '\n')
            #     f.close()
            # gap_list.append(value)
            gap_list[index] = value
            value_16 = hex(value)
            gap_list_hex[index] = value_16.replace('0x', '')

        index += 1

    #print(f'gap size : {len(gap_list)}')
    min_gap = min(gap_list)
    # if min_gap == 0:
    #     min_gap = 1
    sum_gap = sum(gap_list)
    #print(f'sum_gap : {sum_gap}')

    free = int(test_map.summary_df.iloc[index_item+1]['Free'], 16)
    #print(f'free : {free}')

    max_gap = max(gap_list)
    # print(f'max_gap : {max_gap}')
    free_sum_gap = free - sum_gap
    # print(f'free_sum_gap : {free_sum_gap}')
    max_free = max(max_gap, free_sum_gap)
    # print(f'max_free : {max_free}')
    # print(f'max_gap , min_gap : {max_gap}, {min_gap}')
    # print('gap_list')
    # #print(gap_list)
    # print('--------------- gap_2 cal ------------------')
    # print()

    # free_list = np.array([free, sum_gap, min_gap, max_gap])
    # print(free_list)
    # free_df = pd.DataFrame(free_list, columns= ['free','sum_gap','min_gap','max_gap'])
    # free_df.to_csv('free.csv')
    gap_df = pd.DataFrame(gap_list_hex)
    gap_df.columns = ['Gap']
    calculated_df = pd.concat([searched_df, gap_df], axis=1)
    calculated_df.to_csv(PATH_TEMP + '/' + name + '_locate.csv')
    return free, sum_gap, min_gap, max_free
    # else:
    #     return 0,0,0,0


def search_item(full_list, search_name):
    if search_name == full_list[0]:
        return True
    else:
        return False

# modified by 27_step.py


def selected_match_space_df(space_df, item_name):
    match_list = []
    # chip_str = locate_df.iloc[0]['Chip']#.split(':')[1]
    # # chip_str = locate_df.iloc[1,[2]]
    # print(f'chip_str : {chip_str}')
    if space_df.shape[0] > 0:
        # print(f'[12/07] item_name : {item_name}')
        # print(f'[12/07] space_df : {space_df}')

        for i in range(space_df.shape[0]):
            # chip_str = space_df.iloc[i]['Chip'].split(':')[1]
            chip_str = space_df.iloc[i]['Chip']
            if item_name in chip_str:
                # print(f'chip_str : {chip_str}')
                # match_list.append(space_df.iloc[i])
                match_list.append([space_df.iloc[i]['Chip'],  space_df.iloc[i]['Group'], space_df.iloc[i]
                                  ['Section'], space_df.iloc[i]['Size (MAU)'], space_df.iloc[i]['Space addr'], space_df.iloc[i]['Alignment']])
                # print(f'[12/07] match_list[0] : {match_list[0]}')
        # if space_df.shape[0] > 0:
        #     print(f'[12/07] match_list length: {len(match_list)}')

    selected_space_df = pd.DataFrame(data=match_list, columns=[
                                     'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Alignment'])

    # selected_locate_df.to_csv(
    #         PATH_TEMP + '/' + item_name + '_temp_selected_locate.csv')
    # locate_df.to_csv(
    #         PATH_TEMP + '/' + item_name + '_temp_selected_locate.csv')
    # for i in range(locate_df.shape[0]):
    #     WS_1_str = locate_df.iloc[i]['WS_1']
    #     chip_str = locate_df.iloc[i]['Chip']
    #     group_str = locate_df.iloc[i]['Group']
    #     size_str = locate_df.iloc[i]['Size (MAU)']
    #     space_addr_str = locate_df.iloc[i]['Space addr']
    #     chip_addr_str = locate_df.iloc[i]['Chip addr']
    #     alignment_str = locate_df.iloc[i]['Alignment']
    #     WS_2_str = locate_df.iloc[i]['WS_2']
    #     print(f'[match_locate_df] chip_str : item_name -> {chip_str}:{item_name}')
    #     if chip_str == item_name:
    #         match_list.append([WS_1_str, chip_str, group_str, size_str, space_addr_str, chip_addr_str, alignment_str, WS_2_str])

    # match_return_df = pd.DataFrame(match_list, columns = ['WS_1','Chip','Group','Size (MAU)','Space addr','Chip addr','Alignment','WS_2'])
    # if space_df.shape[0] > 0:
    #     print(f'[12/07] : selected_space_df.shape : {selected_space_df.shape}')
    #     print(f'[12/07] : selected_space_df : {selected_space_df}')
    return selected_space_df

# modified by 27_step.py


def selected_match_locate_df(locate_df, item_name):
    match_list = []
    # chip_str = locate_df.iloc[0]['Chip']#.split(':')[1]
    # # chip_str = locate_df.iloc[1,[2]]
    # print(f'chip_str : {chip_str}')

    for i in range(locate_df.shape[0]):
        chip_str = locate_df.iloc[i]['Chip'].split(':')[1]
        if chip_str == item_name:
            # print(f'chip_str : {chip_str}')
            match_list.append(locate_df.iloc[i])

    selected_locate_df = pd.DataFrame(data=match_list, columns=[
                                      'WS_1', 'Chip', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Chip addr', 'Alignment', 'WS_2'])
    selected_locate_df.to_csv(
        PATH_TEMP + '/' + item_name + '_temp_selected_locate.csv')
    # locate_df.to_csv(
    #         PATH_TEMP + '/' + item_name + '_temp_selected_locate.csv')
    # for i in range(locate_df.shape[0]):
    #     WS_1_str = locate_df.iloc[i]['WS_1']
    #     chip_str = locate_df.iloc[i]['Chip']
    #     group_str = locate_df.iloc[i]['Group']
    #     size_str = locate_df.iloc[i]['Size (MAU)']
    #     space_addr_str = locate_df.iloc[i]['Space addr']
    #     chip_addr_str = locate_df.iloc[i]['Chip addr']
    #     alignment_str = locate_df.iloc[i]['Alignment']
    #     WS_2_str = locate_df.iloc[i]['WS_2']
    #     print(f'[match_locate_df] chip_str : item_name -> {chip_str}:{item_name}')
    #     if chip_str == item_name:
    #         match_list.append([WS_1_str, chip_str, group_str, size_str, space_addr_str, chip_addr_str, alignment_str, WS_2_str])

    # match_return_df = pd.DataFrame(match_list, columns = ['WS_1','Chip','Group','Size (MAU)','Space addr','Chip addr','Alignment','WS_2'])
    # return match_return_df


def main(map_file):
    # initialize global vars by Ryan @@2021.11.13
    global section_space_name
    global global_space_name
    global space_name

    global array_space_names
    global index_array_space_names

    section_space_name = []
    global_space_name = ''
    space_name = []

    array_space_names = []
    index_array_space_names = -1

    processing_file = map_file

    # print(f'[12/13] processing_file : {processing_file}')
    if not os.path.isfile(map_file):
        return False

    test_map = Map(processing_file)
    test_map._select_tool_name()
    test_map.run(SECTION_PROCESSING)
    test_map.run(LOCATE_PROCESSING)
    test_map.run(SUMMARY_PROCESSING)
    test_map.run(SPACE_PROCESSING)
    # print(test_map.space_header_list)

    with open('profile.pkl', 'rb') as profile_file:
        profile = pickle.load(profile_file)

    # print(f'[12/22] map_parser : profile : {profile}')
    company_name = profile['company_name'].lstrip().rstrip()
    # Processing with Excel
    myExcel = Excel(processing_file)
    myExcel.makeTitle(
        'Summary', test_map.summary_df.shape[0], test_map.tool_name, company_name)
    myExcel.make_summary(test_map.summary_df)
    item_obj_list = []

    array_space_names = []
    index_array_space_names = -1
    flag_index_array_space_names = False
    head_str = ''
    read_index_array_space_names = -1
    SIZE_data_space_name = 0
    data_space_names = []

    # 12/10 by Ryan
    prefix_local_space_name_list = []
    prefix_local_space_name = ''

    # print(f'[01/17] len(test_map.item_list) : {len(test_map.item_list)}')
    # f_txt = open(PATH_TEMP + '/item_list.txt', 'w')
    # for item_data in test_map.item_list:
    #     print(f'[12/24] {item_data} : {len(item_data.group_list)}')
    #     f_txt.write(item_data + '\n')
    # f_txt.close()
    # ---------
    for index_item in range(len(test_map.item_list)):
        # print(f'[01/17] index_item : {index_item}')
        space_list = []
        array_space_names = []
        index_array_space_names += 1
        read_index_array_space_names += 1

        item_obj = itemObj(test_map.item_list[index_item].split(':')[1])

        if item_obj.item_name == "RegionBlock_Startup":
            # print(f'item_obj.item_name : {item_obj.item_name}')
            break
        if index_item + 1 >= len(test_map.item_list):
            break

        code = test_map.summary_df.iloc[index_item+1]['Code']
        data = test_map.summary_df.iloc[index_item+1]['Data']
        reserved = test_map.summary_df.iloc[index_item+1]['Reserved']
        free = test_map.summary_df.iloc[index_item+1]['Free']
        total = test_map.summary_df.iloc[index_item+1]['Total']
        item_obj._insert_summary(code, data, reserved, free, total)

        # modified by 27_step.py

        selected_locate_df = test_map.locate_df.loc[test_map.locate_df['Chip'].str.contains(
            item_obj.item_name)]

        if not selected_locate_df.empty:
            selected_chip_name = selected_locate_df.iloc[0]['Chip']
            selected_locate_df_chip_name = selected_chip_name.split(':')[1]
            if selected_locate_df_chip_name == item_obj.item_name:
                selected_match_locate_df(
                    selected_locate_df, item_obj.item_name)

                # print('selected_locate_df')
                # print(selected_locate_df)
                # selected_locate_df.to_csv(
                #     PATH_TEMP + '/' + item_obj.item_name + '_selected_locate.csv')
                temp_selected_space_df = test_map.space_df.loc[test_map.space_df['Chip'].str.contains(
                    item_obj.item_name)]

                # temp_selected_space_df.to_csv('./' + item_obj.item_name + '___selected_space.csv')
                # print(f'[12/07] temp_selected_space_df : {temp_selected_space_df}')

                # *************** IMPORTANT
                selected_space_df = selected_match_space_df(
                    temp_selected_space_df, item_obj.item_name)
                # **************************

                # if selected_space_df.shape[0] > 0:
                #     print(
                #         f'[12/07] [item_name] selected_space_df shape : {[item_obj.item_name]} {selected_space_df.shape}')
                # print(f' selected_space_df shape : {selected_space_df.shape}')
                if selected_locate_df.shape[0] > 0:
                    mem_size_df = selected_space_df.loc[:, ['Size (MAU)']]
                    mem_addr_df = selected_space_df.loc[:, ['Space addr']]
                    mem_size_list = mem_size_df.values.tolist()
                    mem_addr_list = mem_addr_df.values.tolist()
                    # print(f'len(mem_size_list) : {len(mem_size_list)}')
                    # print(f'len(mem_addr_list) : {len(mem_addr_list)}')
                    free, sum_gap, min_gap, max_gap = gap_calculattion(
                        test_map, index_item, item_obj.item_name, mem_size_list, mem_addr_list, item_obj.addr_free)
                    item_obj._insert_gap_info(free, sum_gap, min_gap, max_gap)

                size = 0
                len_selected_space_df_shape_0 = selected_space_df.shape[0]
                reserved_selected_space_df = selected_space_df
                # if selected_space_df.shape[0] > 0:
                #     print(
                #         f'[12/07] [item_name] len_selected_space_df_shape_0 shape : {[item_obj.item_name]} : {len_selected_space_df_shape_0}')

                for i in range(selected_locate_df.shape[0]):
                    if selected_locate_df.iloc[i]['Group'] != '':
                        group = selected_locate_df.iloc[i]['Group']

                        if item_obj.exist_group_info(group):
                            add_size = selected_locate_df.iloc[i]['Size (MAU)']
                            size = item_obj.group_size[group]
                            item_obj.total_size += int(size, 16)
                            item_obj.group_size[group] = item_obj.add_size(
                                size, add_size)
                        else:
                            section = selected_locate_df.iloc[i]['Section']
                            size = selected_locate_df.iloc[i]['Size (MAU)']
                            item_obj.group_size[group] = size
                            space_addr = selected_locate_df.iloc[i]['Space addr']
                            chip_addr = selected_locate_df.iloc[i]['Chip addr']
                            alignment = selected_locate_df.iloc[i]['Alignment']
                            item_obj._insert_group_info(
                                group, section, size, space_addr, chip_addr, alignment)
                            item_obj_list.append(item_obj)

                    else:
                        group = '[None]'
                        if item_obj.exist_group_info(group):
                            add_size = selected_locate_df.iloc[i]['Size (MAU)']
                            size = item_obj.group_size[group]
                            item_obj.total_size += int(size, 16)
                            item_obj.group_size[group] = item_obj.add_size(
                                size, add_size)
                        else:
                            section = selected_locate_df.iloc[i]['Section']
                            size = selected_locate_df.iloc[i]['Size (MAU)']
                            item_obj.group_size[group] = size
                            space_addr = selected_locate_df.iloc[i]['Space addr']
                            chip_addr = selected_locate_df.iloc[i]['Chip addr']
                            alignment = selected_locate_df.iloc[i]['Alignment']
                            item_obj._insert_group_info(
                                group, section, size, space_addr, chip_addr, alignment)
                            item_obj_list.append(item_obj)

                # print(f'{item_obj.item_name} : {len(item_obj.group_list)}')
                space_name_index = 0
                # if selected_space_df.shape[0] > 0:
                #     print(
                #         f'[12/07] [item_name] len_selected_space_df_shape_0 shape : {[item_obj.item_name]} : {len_selected_space_df_shape_0}')
                global_space_df = pd.read_csv(PATH_TEMP + '/global_space.csv')
                global_space_list = space_area_index  # global_space_df.values.tolist()
                # 12/09 by Ryan
                # print(f'[12/09] Saved global_space list_df')
                global_space_list_df = pd.DataFrame(global_space_list)
                # global_space_list_df.to_csv('global_space_list_df.csv')
                # selected_space_df.to_csv('selected_space_df.csv')
                local_chip_name = test_map.item_list[index_item]
                # print(f' LAST global_space_list [ 0 ] -> {global_space_list[0]}')
                # print(f' LAST global_space_list [ {len(global_space_list)} ] -> {global_space_list[len(global_space_list) - 1]}')
                # print(f' local_chip_name -> { local_chip_name} ')
                # print(f'global_space_df : {global_space_df.loc[10]}')
                # if selected_space_df.shape[0] > 0:
                #     print(
                #         f'[12/07] [item_name] len_selected_space_df_shape_0 shape : {[item_obj.item_name]} : {len_selected_space_df_shape_0}')
                if len_selected_space_df_shape_0 > 0:

                    for index_select in range(selected_space_df.shape[0]):

                        chip_name = selected_space_df.iloc[index_select]['Chip']
                        group_name = selected_space_df.iloc[index_select]['Group']
                        # print(f'[12/07] local_chip_name :{local_chip_name}')

                        if local_chip_name in chip_name and '+' in chip_name:
                            # if section_space_name[space_name_index][1].find(chip_name):
                            #     space_name = section_space_name[space_name_index][0]
                            group = selected_space_df.iloc[index_select]['Group']
                            section = selected_space_df.iloc[index_select]['Section']
                            size = selected_space_df.iloc[index_select]['Size (MAU)']
                            space_addr = selected_space_df.iloc[index_select]['Space addr']
                            converted_space_addr = abnormal_addr_convert(
                                space_addr)
                            found_index = 0

                            # if 'bmhd0' in group:
                            #     print(f'[12/10] local_chip_name : {local_chip_name}')
                            #     print(f'[12/10] chip_name : {chip_name}')

                            size_array_space_names = 0
                            flag_multi_item_process = True
                            for i in range(len(global_space_list)):
                                # 12/09 by Ryan
                                global_space_index = 0
                                global_space_addr = global_space_list[i][2][5]
                                if section == global_space_list[i][2][3]:
                                    if 'alignment' in section:
                                        j = 0
                                        while space_addr != global_space_addr and j < len(global_space_list):
                                            j += 1
                                            global_space_addr = global_space_list[j][2][5]
                                            global_space_index = j

                                        # print(f'[12/10] alignment section: {section}')
                                        # print(f'[12/10] local_space_name -> {local_space_name}')
                                        # print(f'[12/10] section -> {section}')
                                        # print(f'[12/10] space_addr -> {space_addr}')
                                        # print(f'[12/10] global_space_addr -> {global_space_addr}')
                                        # print()
                                    if global_space_index == 0:
                                        global_space_index = i
                                    multi_items = global_space_list[global_space_index][2][1]
                                    # print(f'[12/09] Mutli-items :{multi_items}')
                                    if '+' in multi_items and flag_multi_item_process and space_addr == global_space_addr:  # 12/10 by Ryan
                                        # # print(f'[12/09] Mutli-items exist')
                                        # # global_space_addr = global_space_list[i][2][5]
                                        # # global_space_index = 0
                                        # if 'alignment' in section:
                                        #     print(f'[12/10] space_addr -> {space_addr}')
                                        #     print(f'[12/10] global_space_addr -> {global_space_addr}')
                                        #     if space_addr != global_space_addr:
                                        #         for j in range(len(global_space_list)):
                                        #             global_space_addr = global_space_list[j][2][5]
                                        #             if space_addr == global_space_addr :
                                        #                 global_space_index = j
                                        #                 break
                                        #     print(f'[12/10] alignment section: {section}')
                                        #     print(f'[12/10] local_space_name -> {local_space_name}')
                                        #     print(f'[12/10] section -> {section}')
                                        #     print(f'[12/10] space_addr -> {space_addr}')
                                        #     print(f'[12/10] global_space_addr -> {global_space_addr}')
                                        #     print(f'[12/10] global_space_list[j][2][5] -> {global_space_list[global_space_index][2][5]}')
                                        #     print(f'[12/10] multi_space -> {multi_space}')
                                        #     print()
                                        # else:
                                        #     global_space_index = i
                                        # if global_space_index == 0:
                                        #    global_space_index = i

                                        multi_items_temp_list = multi_items.split(
                                            '+')
                                        multi_items_list = []
                                        for multi_items_data in multi_items_temp_list:
                                            if multi_items_data != '':
                                                multi_items_list.append(
                                                    multi_items_data)
                                        multi_items_list.sort(reverse=False)

                                        multi_space = global_space_list[global_space_index][1]

                                        multi_space_list = multi_space.split(
                                            '|')
                                        if local_chip_name not in multi_items_list:
                                            flag_multi_item_process = False
                                        else:

                                            local_chip_name_index = multi_items_list.index(
                                                local_chip_name)

                                            local_space_name = multi_space_list[local_chip_name_index]

                                            # 12/13 by Ryan
                                            # f = open('multi-item.txt','a')
                                            # f.write(f'local_chip_name , local_chip_name_index, local_space_name, section => {local_chip_name},{local_chip_name_index},{local_space_name}, {section}')
                                            # f.write('\n')
                                            # f.close()

                                            if local_chip_name_index == 0:
                                                prefix_local_space_name_list = local_space_name.split(
                                                    ':')
                                                prefix_local_space_name = prefix_local_space_name_list[
                                                    0] + ":" + prefix_local_space_name_list[1]
                                                if ':' not in local_space_name:
                                                    local_space_name = prefix_local_space_name + \
                                                        ":" + \
                                                        prefix_local_space_name_list[2]
                                                # print(f'[12/10] prefix_local_space_name -> {prefix_local_space_name}')
                                            else:
                                                local_space_name = prefix_local_space_name + ":" + local_space_name
                                                # print(f'[12/10] local_space_name -> {local_space_name}')
                                    elif flag_multi_item_process == False or '+' not in multi_items:
                                        # if read_index_array_space_names >= 0 and read_index_array_space_names < SIZE_data_space_name:
                                        #     with open('data_space_name.pkl', 'rb') as f:
                                        #         data = pickle.load(f)
                                        #     print(f'[ DATA ] -> {data}')
                                        #     print(f'read_index_array_space_names : {read_index_array_space_names}')
                                        #     local_space_name = data[read_index_array_space_names]
                                        # else:
                                        # print(f'[12/09] Mutli-items NOT exist')
                                        local_space_name = global_space_list[i][1]

                                        # if '|' in local_space_name and 'dspr' in local_chip_name and flag_index_array_space_names == False:
                                        if '|' in local_space_name and flag_index_array_space_names == False:
                                            # data_space_names = []
                                            array_space_names += local_space_name.split(
                                                '|')
                                            size_array_space_names = len(
                                                array_space_names)
                                            head_lists = array_space_names[0].split(
                                                ':')

                                            data_space_names.append(
                                                array_space_names[0])
                                            j = 1
                                            while j < size_array_space_names:
                                                head_str = head_lists[0] + \
                                                    ':' + head_lists[1] + ':'
                                                append_str = head_str + \
                                                    array_space_names[j]
                                                # print(f'[ APPEND_STR ] : {append_str}')
                                                data_space_names.append(
                                                    append_str)
                                                j += 1
                                            # 12/09 by Ryan
                                            # with open(PATH_TEMP + '/data_space_name.pkl', 'wb') as f:
                                            #     pickle.dump(data_space_names, f)
                                            data_space_names_df = pd.DataFrame(
                                                data_space_names)
                                            data_space_names_df.to_csv(
                                                'data_space_names.csv')

                                            flag_index_array_space_names = True
                                            read_index_array_space_names = 0
                                            SIZE_data_space_name = len(
                                                data_space_names)
                                            # print(f'SIZE_data_space_name :{SIZE_data_space_name}')
                                        else:
                                            global_chip_name = global_space_list[i][2][1]
                                            if local_chip_name != global_chip_name:
                                                # print(f'[12/10] local_chip_name ->{local_chip_name}')
                                                # print(f'[12/10] global_chip_name ->{global_chip_name}')
                                                # print(f'[12/10] group :{group}')
                                                local_chip_name = global_chip_name
                                                continue
                                        # if '|' in local_space_name and 'dspr' in local_chip_name and read_index_array_space_names < SIZE_data_space_name:
                                        if '|' in local_space_name and read_index_array_space_names < SIZE_data_space_name:
                                            # print(f'local_chip_name : {local_chip_name}')
                                            # print(f'read_index_array_space_names : {read_index_array_space_names}')
                                            # print(f'data_space_names : {data_space_names}')
                                            local_space_name = data_space_names[read_index_array_space_names]
                                            # read_index_array_space_names +=1
                                            # print(f'array_space_names -> {array_space_names}')
                                        # if local_space_name != 'mpe:vtc:linear':
                                        #     print(f'[index_select : {index_select}] local_space_name : {local_space_name}, section : {section}')
                                        break

                            # if index_array_space_names >= 0:

                            # if flag_index_array_space_names == True and read_index_array_space_names >= 0:
                            #     with open('data_space_name.pkl', 'rb') as f:
                            #         data = pickle.load(f)
                            #     print(f'[ DATA ] -> {data}')
                            #     print(f'read_index_array_space_names : {read_index_array_space_names}')
                            #     local_space_name = data[read_index_array_space_names]
                            #     if read_index_array_space_names >= len(data) - 1 :
                            #         flag_index_array_space_names = False
                            #         read_index_array_space_names = -1

                                #read_index_array_space_names += 1

                            alignment = selected_space_df.iloc[index_select]['Alignment']
                            gap = '0'
                            #add_space = [chip_name, test_map.space_header_list[0], group, section, size, space_addr, alignment, gap]

                            add_space = [local_chip_name, local_space_name, group,
                                         section, size, space_addr, alignment, converted_space_addr]
                            space_list.append(add_space)
                        elif local_chip_name == chip_name:
                            # if section_space_name[space_name_index][1].find(chip_name):
                            #     space_name = section_space_name[space_name_index][0]
                            group = selected_space_df.iloc[index_select]['Group']
                            section = selected_space_df.iloc[index_select]['Section']
                            size = selected_space_df.iloc[index_select]['Size (MAU)']
                            space_addr = selected_space_df.iloc[index_select]['Space addr']
                            converted_space_addr = abnormal_addr_convert(
                                space_addr)
                            found_index = 0

                            # if 'bmhd0' in group:
                            #     print(f'[12/10] local_chip_name : {local_chip_name}')
                            #     print(f'[12/10] chip_name : {chip_name}')

                            size_array_space_names = 0
                            flag_multi_item_process = True
                            for i in range(len(global_space_list)):
                                # 12/09 by Ryan
                                global_space_index = 0
                                global_space_addr = global_space_list[i][2][5]
                                if section == global_space_list[i][2][3]:
                                    if 'alignment' in section:
                                        j = 0
                                        while space_addr != global_space_addr and j < len(global_space_list):
                                            j += 1
                                            global_space_addr = global_space_list[j][2][5]
                                            global_space_index = j

                                        # print(f'[12/10] alignment section: {section}')
                                        # print(f'[12/10] local_space_name -> {local_space_name}')
                                        # print(f'[12/10] section -> {section}')
                                        # print(f'[12/10] space_addr -> {space_addr}')
                                        # print(f'[12/10] global_space_addr -> {global_space_addr}')
                                        # print()
                                    if global_space_index == 0:
                                        global_space_index = i
                                    multi_items = global_space_list[global_space_index][2][1]
                                    # print(f'[12/09] Mutli-items :{multi_items}')
                                    if '+' in multi_items and flag_multi_item_process and space_addr == global_space_addr:  # 12/10 by Ryan
                                        # # print(f'[12/09] Mutli-items exist')
                                        # # global_space_addr = global_space_list[i][2][5]
                                        # # global_space_index = 0
                                        # if 'alignment' in section:
                                        #     print(f'[12/10] space_addr -> {space_addr}')
                                        #     print(f'[12/10] global_space_addr -> {global_space_addr}')
                                        #     if space_addr != global_space_addr:
                                        #         for j in range(len(global_space_list)):
                                        #             global_space_addr = global_space_list[j][2][5]
                                        #             if space_addr == global_space_addr :
                                        #                 global_space_index = j
                                        #                 break
                                        #     print(f'[12/10] alignment section: {section}')
                                        #     print(f'[12/10] local_space_name -> {local_space_name}')
                                        #     print(f'[12/10] section -> {section}')
                                        #     print(f'[12/10] space_addr -> {space_addr}')
                                        #     print(f'[12/10] global_space_addr -> {global_space_addr}')
                                        #     print(f'[12/10] global_space_list[j][2][5] -> {global_space_list[global_space_index][2][5]}')
                                        #     print(f'[12/10] multi_space -> {multi_space}')
                                        #     print()
                                        # else:
                                        #     global_space_index = i
                                        # if global_space_index == 0:
                                        #    global_space_index = i

                                        multi_items_temp_list = multi_items.split(
                                            '+')
                                        multi_items_list = []
                                        for multi_items_data in multi_items_temp_list:
                                            if multi_items_data != '':
                                                multi_items_list.append(
                                                    multi_items_data)
                                        multi_items_list.sort(reverse=False)
                                        multi_space = global_space_list[global_space_index][1]

                                        multi_space_list = multi_space.split(
                                            '|')
                                        if local_chip_name not in multi_items_list:
                                            flag_multi_item_process = False
                                        else:

                                            local_chip_name_index = multi_items_list.index(
                                                local_chip_name)

                                            local_space_name = multi_space_list[local_chip_name_index]

                                            if local_chip_name_index == 0:
                                                prefix_local_space_name_list = local_space_name.split(
                                                    ':')
                                                prefix_local_space_name = prefix_local_space_name_list[
                                                    0] + ":" + prefix_local_space_name_list[1]
                                                if ':' not in local_space_name:
                                                    local_space_name = prefix_local_space_name + \
                                                        ":" + \
                                                        prefix_local_space_name_list[2]
                                                # print(f'[12/10] prefix_local_space_name -> {prefix_local_space_name}')
                                            else:
                                                local_space_name = prefix_local_space_name + ":" + local_space_name
                                                # print(f'[12/10] local_space_name -> {local_space_name}')
                                    elif flag_multi_item_process == False or '+' not in multi_items:
                                        # if read_index_array_space_names >= 0 and read_index_array_space_names < SIZE_data_space_name:
                                        #     with open('data_space_name.pkl', 'rb') as f:
                                        #         data = pickle.load(f)
                                        #     print(f'[ DATA ] -> {data}')
                                        #     print(f'read_index_array_space_names : {read_index_array_space_names}')
                                        #     local_space_name = data[read_index_array_space_names]
                                        # else:
                                        # print(f'[12/09] Mutli-items NOT exist')
                                        local_space_name = global_space_list[i][1]

                                        # if '|' in local_space_name and 'dspr' in local_chip_name and flag_index_array_space_names == False:
                                        if '|' in local_space_name and flag_index_array_space_names == False:
                                            # data_space_names = []
                                            array_space_names += local_space_name.split(
                                                '|')
                                            size_array_space_names = len(
                                                array_space_names)
                                            head_lists = array_space_names[0].split(
                                                ':')

                                            data_space_names.append(
                                                array_space_names[0])
                                            j = 1
                                            while j < size_array_space_names:
                                                head_str = head_lists[0] + \
                                                    ':' + head_lists[1] + ':'
                                                append_str = head_str + \
                                                    array_space_names[j]
                                                # print(f'[ APPEND_STR ] : {append_str}')
                                                data_space_names.append(
                                                    append_str)
                                                j += 1
                                            # 12/09 by Ryan
                                            # with open(PATH_TEMP + '/data_space_name.pkl', 'wb') as f:
                                            #     pickle.dump(data_space_names, f)
                                            data_space_names_df = pd.DataFrame(
                                                data_space_names)
                                            data_space_names_df.to_csv(
                                                'data_space_names.csv')

                                            flag_index_array_space_names = True
                                            read_index_array_space_names = 0
                                            SIZE_data_space_name = len(
                                                data_space_names)
                                            # print(f'SIZE_data_space_name :{SIZE_data_space_name}')
                                        else:
                                            global_chip_name = global_space_list[i][2][1]
                                            if local_chip_name != global_chip_name:
                                                # print(f'[12/10] local_chip_name ->{local_chip_name}')
                                                # print(f'[12/10] global_chip_name ->{global_chip_name}')
                                                # print(f'[12/10] group :{group}')
                                                local_chip_name = global_chip_name
                                                continue
                                        # if '|' in local_space_name and 'dspr' in local_chip_name and read_index_array_space_names < SIZE_data_space_name:
                                        if '|' in local_space_name and read_index_array_space_names < SIZE_data_space_name:
                                            # print(f'local_chip_name : {local_chip_name}')
                                            # print(f'read_index_array_space_names : {read_index_array_space_names}')
                                            # print(f'data_space_names : {data_space_names}')
                                            local_space_name = data_space_names[read_index_array_space_names]
                                            # read_index_array_space_names +=1
                                            # print(f'array_space_names -> {array_space_names}')
                                        # if local_space_name != 'mpe:vtc:linear':
                                        #     print(f'[index_select : {index_select}] local_space_name : {local_space_name}, section : {section}')
                                        break

                            # if index_array_space_names >= 0:

                            # if flag_index_array_space_names == True and read_index_array_space_names >= 0:
                            #     with open('data_space_name.pkl', 'rb') as f:
                            #         data = pickle.load(f)
                            #     print(f'[ DATA ] -> {data}')
                            #     print(f'read_index_array_space_names : {read_index_array_space_names}')
                            #     local_space_name = data[read_index_array_space_names]
                            #     if read_index_array_space_names >= len(data) - 1 :
                            #         flag_index_array_space_names = False
                            #         read_index_array_space_names = -1

                                #read_index_array_space_names += 1

                            alignment = selected_space_df.iloc[index_select]['Alignment']
                            gap = '0'
                            #add_space = [chip_name, test_map.space_header_list[0], group, section, size, space_addr, alignment, gap]

                            add_space = [local_chip_name, local_space_name, group,
                                         section, size, space_addr, alignment, converted_space_addr]
                            space_list.append(add_space)
                        space_name_index += 1
                        # else:
                        #     print(f'chip_name : {chip_name}')
                # print(f'[before/before] spaceList size : {len(space_list)}')
                # print(f'[12/07] space_list :{space_list}')
                converted_space_df = pd.DataFrame(data=space_list, columns=[
                    'Chip', 'space_name', 'Group', 'Section', 'Size (MAU)', 'Space addr', 'Alignment', 'converted'])
                converted_space_df = converted_space_df.sort_values(
                    by=["converted"], ascending=[True])
                converted_space_df.reset_index(inplace=True, drop=True)
                converted_space_df.to_csv(
                    PATH_TEMP + '/' + item_obj.item_name + '_space.csv')
                # if read_index_array_space_names >= 0 and read_index_array_space_names < SIZE_data_space_name:
                #     read_index_array_space_names += 1
                # elif read_index_array_space_names >= SIZE_data_space_name:
                #     read_index_array_space_names = -1

    with open(PATH_TEMP + '/section_space_name.pkl', 'wb') as tf:
        pickle.dump(section_space_name, tf)

    name_list = []
    for i in range(len(test_map.item_list)):
        name_str = test_map.item_list[i].split(':')
        name_list.append(name_str[1])
    # print(name_list)
    # Generating Excel

    search_item_list = []
    for j in range(len(name_list)):
        search_item_list = []
        for i in range(len(space_list)):
            if search_item(space_list[i], name_list[j]) == True:
                #print(f'..... Searched for {test_map.item_list[j]}')
                search_item_list.append(space_list[i])
                # print(f'search_item_list size : {len(search_item_list)}')
        item_name = name_list[j]
        for item_obj in item_obj_list:
            if item_obj.item_name == item_name:
                #print(f'item_obj.item_name : {item_obj.item_name}')
                ws = myExcel.make_item(item_obj)  # mpe:dspr0
                myExcel.save()
                # print(f'saved Excel file')
                break
            # else:
            #     print(f'..... Not searched for {item_obj.item_name}')

    return True


def init_dir():
    temp_dir = r'.\\temp'

    if not os.path.isdir(OUTPUT_EXCEL):
        os.makedirs(OUTPUT_EXCEL)
    else:
        [os.remove(f) for f in glob.glob(OUTPUT_EXCEL + '/' + '*.xlsx')]

    if not os.path.isdir(OUTPUT_PDF):
        os.makedirs(OUTPUT_PDF)
    else:
        [os.remove(f) for f in glob.glob(OUTPUT_PDF + '/' + '*.pdf')]

    if not os.path.isdir(OUTPUT_FINAL):
        os.makedirs(OUTPUT_FINAL)

    if not os.path.isdir(resource_path(temp_dir)):
        os.makedirs(resource_path(temp_dir))
    # else:
        # csv_file_list = glob.glob('temp/' + '*.csv')
        # print(f'[12/13] csv_file_list : {csv_file_list}')

        # [os.remove(f)
        #  for f in glob.glob(resource_path(temp_dir) + '/' + '*.csv')]
        # [os.remove(f)
        #  for f in glob.glob(resource_path(temp_dir) + '/' + '*.pkl')]


def parser_main(map_file):
    init_dir()

    # print(f'[12/16] map_file : {map_file}')
    exec_file_path = getattr(
        sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    status = main(map_file)
    # print("Mapfile parsing is in progress… ")
    # print("Please wait ... ")
    # status = True
    if status:

        abs_excel_file_path = os.path.abspath(OUTPUT_EXCEL)
        # print(f'[12/16] abs_excel_file_path {abs_excel_file_path}')
        excelinfo = write_pdf.excelInfo(abs_excel_file_path)
        # print(f'[12/16] excelinfo')
        # print(f'{excelinfo}')
        abs_pdf_file_path = os.path.abspath(OUTPUT_PDF)
        exec_file_path = os.path.abspath(map_file)
        print('Parsing is Success!!!')
        # exec_file_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        # print(f'[12/16] abs_pdf_file_path {abs_pdf_file_path}')
        # print(f'[12/16] exec_file_path {exec_file_path}')

        # write_pdf.transPDF(excelinfo, abs_pdf_file_path)
        # print('PDF generated successfully')
        # write_pdf.integrated_one_file(exec_file_path, abs_pdf_file_path, map_file)
    else:
        print('File is NOT exist or')
        print('Parsing is failed')


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    map_file = "TRICORE_TC39XX_VOYAH_ADCU.map"
    parser_main(map_file)
