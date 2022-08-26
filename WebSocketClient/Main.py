#!/usr/bin/python3
#coding=utf-8
#author: libiqi


import importlib
import os
from prettytable import PrettyTable
import time
# url = 'ws://localhost:8765/'
url = 'ws://10.96.0.54:9000/conn'
def run_case():
    current_path = os.path.dirname(os.path.abspath(__file__))
    case_path = os.path.join(current_path, "Cases/")
    categorys = [d for d in os.listdir(case_path) if d.find("__") < 0 and d.find(".") < 0]
    fail_sum = 0
    success_sum = 0
    table_list = [] # 画表格中的数据
    for category in categorys:
        case_list = [c[:-3] for c in os.listdir(os.path.join(case_path, category)) if c.find("Case") >=0]
        for case in case_list:
            clss = case
            try:
                print("Cases.{}.{}".format(category, clss))
                module = importlib.import_module("Cases.{}.{}".format(category, clss))
            except Exception as e:
                break
            instance = module.__dict__[clss](url)
            instance.run()
            if not instance.is_success:
                table_detail = add_case_name(clss,instance.error_detail)
                table_list.extend(table_detail)
            fail_sum = fail_sum + instance.error_cnt
            success_sum = success_sum + instance.correct_cnt
    print('本次共执行{0}条接口检查，通过{1}条，失败{2}条'.format(fail_sum+success_sum,success_sum,fail_sum))
    if fail_sum != 0:
        print('执行失败如下：')
        print(drow_table(table_list))

def add_case_name(name,error_detail):
    result_list = []
    for i in error_detail:
        i[0] = name+'-' + str(i[0])
        result_list.append(i)
    return result_list


def drow_table(table_list):
    table = PrettyTable(['Case-check_id','预计值','实际值'])
    table.align['check_id'] = 'l'
    table.padding_width = 1
    table.add_rows(table_list)
    return table
def main():
    start_time = time.time()
    run_case()
    cost_time = time.time() - start_time
    print('用时',cost_time,'秒')




if __name__ == '__main__':
    main()