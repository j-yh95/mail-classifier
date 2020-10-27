#-*- coding: utf-8 -*-
import json
import re
import sys

#RFC5322
regexer = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'

def spliter(email_account):
    account = email_account.split('@')[0]
    email = email_account.split('@')[1]

    return email, account

if __name__ == "__main__":
    emails = open(sys.argv[1], 'r', encoding='utf-8')
    emails = emails.readlines()
    regex = re.compile(regexer)

    search_success = {}
    search_failed = []

    search_success_csv = open('./' +sys.argv[1]+ '_search_success.csv', 'w')
    search_failed_csv = open('./' +sys.argv[1]+ '_search_failed_csv.csv', 'w')

    #DB파일에서 이메일 검색 후 분류 성공, 분류 실패에 삽입
    for email in emails:
        email = email.replace('\n', '')
        search_email = regex.search(email)
        if search_email != None:
            email_account = spliter(search_email.group())
            
            mail = email_account[0]
            account = email_account[1]

            search_success.setdefault(mail, []).append(account)
        else:
            search_failed.append(email)

    #분류 실패 메일 CSV write
    for line in search_failed:
        search_failed_csv.write(line + '\n')


    # #분류 성공 메일 CSV write
    for mail, accounts in search_success.items():
        count=0
        accounts_length = len(accounts)
        search_success_csv.write(mail + ',' + str(accounts_length) + ',')

        for account in accounts:
            account = str(account)
            count = count + 1

            if accounts_length != count:
                account = account + ','
            search_success_csv.write(account)
        search_success_csv.write('\n')
