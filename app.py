from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import News
import requests
from xml.etree import ElementTree
import re
from bs4 import BeautifulSoup
import os

CHAT_ID = os.environ['CHAT_ID']
BOT = os.environ['BOT']
engine = create_engine(os.environ['DATABASE_URL'])
session = sessionmaker(bind=engine)()


def parse():
    r = requests.get('http://urod.ru/xml/rss.xml')
    root = ElementTree.fromstring(r.content)

    for item in root.iter('item'):
        save(item)


def save(item):
    urod_id = int(re.sub('\D', '', item.find('link').text) or None)
    if not urod_id:
        return
    if session.query(News).get(urod_id):
        return
    soup = BeautifulSoup(item.find('description').text, 'html.parser')
    if soup.img:
        n = News(format='img', text=soup.img['src'])
    elif soup.iframe:
        n = News(format='video', text=soup.iframe['src'])
    elif len(soup.greeting.text.strip()) == 0:
        n = News(format='none', text=None)
    else:
        n = News(format='text', text=soup.greeting.text)
    n.urod_id = urod_id
    n.link = item.find('link').text
    n.title = item.find('title').text
    session.add(n)
    session.commit()


def generate_img(n):
    return {
        'action': 'sendPhoto',
        'data': {
            'photo': n.text,
            'caption': '%s\n%s' % (n.title, n.link)
        }
    }


def generate_video(n):
    return {
        'action': 'sendMessage',
        'data': {
            'text': '<b>%s</b>\n%s\n%s' % (n.title, n.text, n.link),
            'parse_mode': 'html'
        }
    }


def generate_none(n):
    return {
        'action': 'sendMessage',
        'data': {
            'text': '*%s*\n%s' % (n.title, n.link),
            'parse_mode': 'markdown'
        }
    }


def generate_text(n):
    return {
        'action': 'sendMessage',
        'data': {
            'text': '*%s*\n%s\n%s' % (n.title, n.text, n.link),
            'parse_mode': 'markdown'
        }
    }


METHODS = {
    'img': generate_img,
    'video': generate_video,
    'none': generate_none,
    'text': generate_text
}


def send_news():
    limitation = 100
    news = session.query(News).filter(News.send_msg.isnot(True)) \
        .order_by(News.urod_id)
    for n in news:
        data = METHODS[n.format](n)
        send(data)
        n.send_msg = True
        session.commit()
    count = session.query(News).count()
    if count > limitation:
        q = session.query(News.urod_id).order_by(News.urod_id)\
            .limit(count - limitation).subquery()
        session.query(News).filter(News.urod_id.in_(q))\
            .delete(synchronize_session='fetch')
        session.commit()


def send(data):
    data['data']['chat_id'] = CHAT_ID
    url = 'https://api.telegram.org/bot%s/%s' % (BOT, data['action'])
    requests.post(url, data=data['data'])


if __name__ == "__main__":
    parse()
    send_news()
