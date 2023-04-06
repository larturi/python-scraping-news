import os
import datetime
import requests
import lxml.html as html

HOME_URL = 'https://www.larepublica.co/'

X_PATH_LINK_TO_ARTICLE = '//div[@class="news V_Title_Img"]//a/@href'
X_PATH_TITLE = '//h2/span/text()'
X_PATH_SUMMARY = '//div[contains(@class, "lead")]/p/text()'
X_PATH_BODY = '//div[@class="html-content"]/p//text()'

def parse_home():
    try:
        response = requests.get(HOME_URL)
        
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            
            links_to_notices = parsed.xpath(X_PATH_LINK_TO_ARTICLE)
                        
            today = datetime.date.today().strftime('%d-%m-%y')
            
            if not os.path.isdir('articles'):
                os.mkdir(f'articles')
            
            if not os.path.isdir(f'articles/{today}'):
                os.mkdir(f'articles/{today}')
                
            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
        
        
def parse_notice(link, today):
    try:
        response = requests.get(link)
        
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            
            try:
                title = parsed.xpath(X_PATH_TITLE)[0].strip()
                title = title.replace('\"', '')
                summary = parsed.xpath(X_PATH_SUMMARY)[0].strip()
                body = parsed.xpath(X_PATH_BODY)
            except IndexError:
                print(IndexError)
            
            with open(f'articles/{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                
                for p in body:
                    f.write(p.strip())
                    f.write('\n')
                            
        else:
            raise ValueError(f'Error: {response.status_code}')
        
    except ValueError as ve:
        print(ve)


def run():
    parse_home()
    

if __name__ == '__main__':
    run()