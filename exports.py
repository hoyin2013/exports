# coding: utf-8
# __author__ = 'Hoyin'
# __date__ = '2020/05/02'
# __Desc__ = 从数据库中导出数据到excel数据表中

import csv
import os
import glob
import  openpyxl
import chardet
import db
from config import *
from utils import *

# 文件的根目录
BASE_DIR, filename = os.path.split(os.path.abspath(__file__))
# print(__file__)
BASE_DIR = BASE_DIR.replace('\\', '/')

# print(BASE_DIR)

def readfile(filename):
    try:
        f = open(filename, 'rb')
        data = f.read()
        result = chardet.detect(data)
        encoding = result['encoding']
        print("文件：{}，编码为：{}".format(filename ,encoding))
        logging.info("文件：{}，编码为：{}".format(filename ,encoding))
        f.close()
        return data
    except Exception as e:
        logging.error(e)
        if data:
            f.close()
        return False


def export_to_excel(sql, outputpath):
    logging.info("export_to_excel")
    
    results, fields_complex = db.get_data(sql)
    #logging.info(results,fields_complex)

    if not results:
        return False

    wb = openpyxl.Workbook()
    ws = wb.worksheets[0]
    
    # 写上字段信息
    for i in range(len(fields_complex)):
        ws.append(fields_complex[i][0])

        
    i = 1
    for line in results:
        for col in range(1, len(line) + 1):
            ColNum = openpyxl.cell.cell.get_column_letter(col)
            ws.cell('%s%s' % (ColNum, i)).value = line[col - 1]
        i += 1
 

    ws.save(outputpath + '.xlsx')

    return True

def export_to_csv(sql, outputpath):
    if not db.get_data(sql):
        return False
    else:
        results, fields = db.get_data(sql)

    #print(results,fields)
    f = open(outputpath + '.csv', 'w+', newline='', encoding='utf-8')
    write = csv.writer(f)
    
    try:
        head = [ x[0] for x in fields]
        #print(head)
        write.writerow(head)
        #print(results)
        write.writerows(results)
    except Exception as e:
        logging.error("写入数据失败! 原因：{}".format(e))

    f.close()

    return True



# 找到根目录下的所有sql文件
sql_files = glob.glob(BASE_DIR + '/sql/*.*')
sql_files = [f.replace('\\', '/') for f in sql_files]
# print(sql_files)

passwd = gen_pass(6)

for fp in sql_files:

    logging.info("开始解析:{}".format(fp))

    # 解析sql
    sql = readfile(fp)

    # 保存执行结果
    outputpath = BASE_DIR + '/exports/' + os.path.splitext(os.path.basename(fp))[0]

    if export_type == 'excel':
        postfix = 'xls'
        result = export_to_excel(sql, outputpath)
    elif export_type == 'csv':
        postfix = 'csv'
        result = export_to_csv(sql, outputpath)

    if result:
        logging.info("生成文件:{}.{} 成功！".format(outputpath,postfix))
    else:
        logging.error("生成文件:{}.{} 失败！".format(outputpath,postfix))


print(passwd)
logging.info("密码:{}".format(passwd))

    





