# coding: utf-8

import imapclient,re
import pyzmail


#提取邮件里面的链接
def getDowmlodUrl():
    url = None
    #这里是腾讯企业邮箱，其他的自行百度
    imapObj = imapclient.IMAPClient('imap.exmail.qq.com',ssl=True)
    #邮箱和密码
    imapObj.login('yinhb@mfhcd.com','Hoyin@2020!')
    #默认收件箱
    imapObj.select_folder('INBOX',readonly=True)
    #搜索未读邮件，打印未读邮件的UID
    UIDS = imapObj.search('UNSEEN')
    print(UIDS)
    #UIDS = imapObj.search('ALL')#搜索全部的邮件
    if len(UIDS) >= 1:#存在未读邮件
        #获得邮件内容
        rawMessage = imapObj.fetch(UIDS[0],[b'BODY[]'])
        #选择第一封未读邮件
        messageObj = pyzmail.PyzMessage.factory(rawMessage[UIDS[0]][b'BODY[]'])
        #打印邮件信息，可以根据这些信息进行筛选
        print(messageObj.get_subject())#邮件主题
        print(messageObj.get_addresses('from'))#发件人
        print(messageObj.get_addresses('to'))#收件人
        print(messageObj.get_addresses('cc'))
        print(messageObj.get_addresses('bcc'))

        #邮件内容不为空时
        if messageObj.html_part != None:
            messageContent = messageObj.html_part.get_payload().decode(messageObj.html_part.charset)
            #打印邮件内容
            print(type(messageContent),messageContent)
            #提取邮件内容里面的链接
            pattern = re.compile(r'//[0-9A-Za-z./\\?\\=\\:]+')
            m = re.search(pattern,messageContent)
            print('m',m)
            if m is not None:
                print('http:' + m.group(0))
                url = 'http:' + m.group(0)
            #如果没有则取提起邮件的附件
            else:
                for part in messageObj.walk():
                    # name = part.get_param('name')
                    if part.get_filename() != None:
                        # print(part,part.get_filename())
                        with open(part.get_filename(), 'wb') as f:
                            f.write(part.get_payload(decode=True))
            #设置邮件已读
            imapObj.set_flags(rawMessage, b'\\Seen', silent=False)
        else:
            pass
    #退出邮件
    imapObj.logout()
    #如果邮件内容存在链接则返回链接，若不存在则直接下载邮件附件
    return url

getDowmlodUrl()
