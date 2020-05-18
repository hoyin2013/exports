# coding: utf-8

from SendEmail import *

def sendmail(subject, attachs, receivers):
    # 邮件内容存放路径 
    content_path = BASE_DIR + '/mail.txt'
    
    # 传递邮件发送参数
    argvs = {
        'smtp_server': 'mail01.xdjk.com',
        'port': 25,
        'user': 'operation@xdjk.com',
        'passwd': 'xdjk2019',
        'ssl': False,
        'sender': 'operation@xdjk.com',
        'receivers': receivers,
        'subject': subject,
        'content_path': content_path,
        'attach_files': attachs,
        'attach_title': os.path.basename(attachs[0])
    }
    # 发送邮件
    sendemail = SendEmail(**argvs)
    sendemail.send()

# 邮件主题日期
nowDate = datetime.datetime.now().strftime('%Y-%m-%d') 
subject = '[' + nowDate + ']' + ''

# 附件路径
attachs = ['C:\Users\yinhb\Desktop\exports\exports\',]
# 接收邮件列表
#receivers = ['yinhb@mfhcd.com', ]
receivers = receivers = ['yinhb@mfhcd.com',]
sendmail(subject, attachs, receivers)


