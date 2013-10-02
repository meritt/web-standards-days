# coding=utf-8

import os
from datetime import datetime

import pytz
from flask import render_template, redirect
from jinja2 import TemplateNotFound
from mailsnake.exceptions import *

from . import app
from .models import Events, Speakers, Presentations, Event, Partners
from .forms import RegistrationForm


def process_register(data, list_id):
    from mailsnake import MailSnake
    api_key = os.environ['MAILCHIMP_API_KEY']

    ms = MailSnake(api_key)
    try:
        status = ms.listSubscribe(
            id=list_id,
            email_address=data['email'],
            double_optin=False,
            merge_vars={
                "FNAME": data['firstName'],
                "LNAME": data['lastName'],
                "COMPANY": data['company'],
                "POSITION": data['position'],
                "TWITTER": data['twitter']
            }
        )
        return {
            'success': status
        }
    except ListAlreadySubscribedException, e:
        return {
            'success': False,
            'message': u'Адрес электронной почты {} уже зарегистрирован'.format(data['email']),
        }
    except MailSnakeException, e:
        # TODO: Нужно логгировать ошибки
        print e.message
        return {
            'success': False,
            'message': u'Возникла непредвиденная ошибка',
        }

@app.route('/')
def index():
    import random
    from itertools import groupby

    events = Events('events')
    speakers = Speakers('speakers')
    presentations = Presentations('presentations', speakers)

    return render_template('index.html',
                           history=groupby(
                               events.order_by('-date'),
                               key=lambda x: x['date'].year
                           ),
                           speakers=speakers.order_by('lastName'),
                           presentations=random.sample(presentations.filter('videoId'), 3),
                           today=datetime.now(pytz.utc)
    )


@app.route('/<int:year>/<int:month>/<int:day>/')
def legacy_event(year, month, day):
    events = Events('events')
    event = events.getByDate(day, month, year)
    if event:
        return redirect('/events/{}/'.format(event['id']))
    else:
        return render_template('page-not-found.html'), 404


@app.route('/events/<event_id>/', methods=['GET', 'POST'])
def event(event_id):
    events = Events('events')
    speakers = Speakers('speakers')
    partners = Partners('partners')
    presentations = Presentations('presentations', speakers)

    event = Event(events.get(event_id))

    if not event:
        return render_template('page-not-found.html'), 404

    data = event.getData(speakers, presentations)

    if event.showRegistration:
        form = RegistrationForm(event['registration']['fields'])
    else:
        form = False

    return render_template('event.html',
                           event=event,
                           schedule=data.get('schedule'),
                           speakers=data.get('speakers'),
                           speakers_dict=data.get('speakers_dict'),
                           partners=partners,
                           registration_form=form,
    )


@app.route('/events/<event_id>/registration/', methods=['POST',])
def registration(event_id):
    events = Events('events')
    event = Event(events.get(event_id))
    if app.debug is True:
        from time import sleep
        sleep(2)

    return render_template('result.html')


@app.route('/<staticpage>/')
def staticpage(staticpage):
    try:
        return render_template('staticpages/%s.html' % staticpage)
    except TemplateNotFound, e:
        return render_template('page-not-found.html'), 404
