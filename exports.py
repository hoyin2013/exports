# coding: utf-8
#!/usr/bin/env python3
# __author__ = 'Hoyin'
# __date__ = '2020/05/02'
# __Desc__ = 从数据库中导出数据到excel数据表中

import csv
import os
import glob
import openpyxl
import chardet
import db
from config import *
from utils import *
from SendEmail import *



# 文件的根目录
BASE_DIR, filename = os.path.split(os.path.abspath(__file__))
# print(__file__)
BASE_DIR = BASE_DIR.replace('\\', '/')

# print(BASE_DIR)

send_to_email = False

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
    
    results, fields = db.get_data(sql)
    #logging.info(results,fields)

    if not results:
        return False

    wb = openpyxl.Workbook()
    ws = wb.active

    # 写上字段信息
    # for field in range(0,len(fields)):
    #     ws.append(fields[field][0])
    
    fields = [f[0] for f in fields]

    # print(fields)
    ws.append(fields)

    for res in results:
        ws.append(res)

    wb.save(outputpath + '.xlsx')
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


print(gen_pass())

# 发送邮件
def sendmail(subject, attachs, receivers):
    # 邮件内容存放路径 
    content_path = BASE_DIR + '/mail.txt'
    
    # 传递邮件发送参数
    argvs = {
        'smtp_server': '10.83.1.19',
        'port': 25,
        'user': 'operation@xdjk.com',
        'passwd': 'xdjk2019',
        'ssl': False,
        'sender': 'operation@xdjk.com',
        'receivers': receivers,
        'subject': subject,
        'content_path': content_path,
        'attach_files': attachs,
        'attach_title': ''
    }
    # 发送邮件
    sendemail = SendEmail(**argvs)
    sendemail.send()
    


if send_to_email: 
    # 邮件主题日期
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d') 
    subject = '[' + nowDate + ']' + '新增非标商户数据'
    # 附件路径
    attachs = glob.glob(BASE_DIR + '/exports/*.xlsx')

    # 接收邮件列表
    #receivers = ['yinhb@mfhcd.com', ]
    receivers = ['yinhb@mfhcd.com', 'liutao-yunwei@mfhcd.com','shangxy@mfhcd.com', 'humiao@mfhcd.com']
    sendmail(subject, attachs, receivers)
     
    # 如果定期跑批,则需要清理文件
    try:
        for i in os.listdir(BASE_DIR + '/exports/'):
            print(BASE_DIR + '/exports/' + i)
            os.remove(BASE_DIR + '/exports/' + i)
            logging.info("删除导出文件:%{}".format(BASE_DIR + '/exports/' + i)) 
    except:
        print("删除导出文件失败")  
        logging.error("删除导出文件失败")      






