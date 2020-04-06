import imapclient
import pyzmail
from bs4 import BeautifulSoup
import webbrowser
old = []
mail_addr = input('Enter gmail address: ')
pwd = input('Enter application password: ')
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl = True)
imapObj.login(mail_addr, pwd)
imapObj.select_folder('INBOX', readonly = True)
UIDs = imapObj.search(['ALL'])
#print(UIDs)
for each in UIDs:
    print(each)
    raw = imapObj.fetch([each], ['BODY[]'])
    #print('RAW obtained')
    msg = pyzmail.PyzMessage.factory(raw[each][b'BODY[]'])
    #print('PYZ MAIL PARSED')
    fromAddr = msg.get_addresses('from')
    print(fromAddr)
    #print(msg.get_addresses('to'))
    #print(msg.get_subject())
    if fromAddr not in old:
        if msg.html_part != None:
            #print('Got a HTML')
            body = msg.html_part.get_payload().decode(msg.html_part.charset)
            #print(body)
            soup = BeautifulSoup(body, 'lxml')
            try:
                for x in soup.find_all('a', href = True):
                    if x.string == 'click here' or x.string == 'Click Here' or x.string == 'Click here':
                        #print(x.string)
                        link = x['href']
                        print(x['href'])
                        print('\n\n')
                        webbrowser.open(link)
                        old.append(fromAddr)
                        input()
                        
            except:
                print('No unsubscribe option')
        


imapObj.logout()
