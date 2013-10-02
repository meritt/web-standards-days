# coding=utf-8

from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField, PasswordField, FileField, HiddenField
from flask.ext.wtf import DataRequired, Email


def generateField(field):
        """
        Преобразуем словарь, описывающий поле формы в инстанс поля WTForms

        :rtype : wtforms.Input
        :param field: dict
        """
        types = {
            'textField': TextField,
            'textarea': TextAreaField,
            'checkboxField': BooleanField,
            'hiddenField': HiddenField,
        }
        return types[field['type']](field['label'])


def RegistrationForm(fields):
    """
    Фабрика формы регистрации

    :rtype : Form инстанс формы
    :param fields: dict словарь полей формы
    """

    class RegistrationFormClass(Form):
        email = TextField(u"Адрес электронной почты", validators=[
            DataRequired(message=u"Обязательное поле"),
            Email(u"Введите действующий адрес электронной почты")
        ])

    for field in fields:
        setattr(RegistrationFormClass, field['name'], generateField(field))

    return RegistrationFormClass
