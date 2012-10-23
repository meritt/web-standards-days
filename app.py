# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template

app = Flask(__name__)

def add_null(val):
    return val if val >= 10 else "0%s" % val


@app.route('/')
def hello_world():

    return u'Главная'


@app.route('/<int:year>/<int:month>/<int:day>/')
def event(year, month, day):
    data = {i:json.load(open('data/%s.json' % i)) for i in ['events', 'partners', 'presentations', 'speakers']}

    event_date = '%s-%s-%s' % (add_null(day), add_null(month), year)

    try:
        event = filter(lambda x: x if x['date'] == event_date else False, data['events'].values())[0]
    except IndexError:
        return render_template('page_not_found.html'), 404
    except Exception:
        return render_template('server_error.html'), 500

    for schedule_item in event['schedule']:
        if schedule_item.has_key('presentation'):
            schedule_item['presentation'] = data['presentations'][schedule_item['presentation']]

    speakers_keys = [x['presentation']['speaker'] for x in filter(lambda x: x.has_key('presentation'), event['schedule'])]

    speakers = sorted(
        [(key, data['speakers'][key]) for key in speakers_keys],
        key=lambda x: x[1]['last_name']
    )

    speakers_dict = {x:'%s %s' % (y['first_name'], y['last_name']) for x, y in speakers}

    return render_template('event.html', date=event_date, data=data, event=event, speakers=speakers,
        speakers_dict=speakers_dict, partners=data['partners'])


@app.route('/<int:year>/<int:month>/<int:day>/register/')
def register(year, month, day):

    return u'Регистрация на событие'


if __name__ == '__main__':
    app.debug = True
    app.run()
