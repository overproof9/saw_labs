import re

from app import app


class Validator:
    # toggle data filtering if True filter is ON
    filter = app.config.get('FILTER', True)
    
    @classmethod
    def form2dict(cls, form):
        return {key: value.data for key, value in form._fields.items()}
    
    @classmethod
    def substitute_special(cls, value):
        expr = r'[\\,\-,\',\*,\.,\,,\%,\<,\>]'
        try:
            result = re.sub(expr, '', value)
            result = result.strip()
        except TypeError:
            result = value
        return result

    @classmethod
    def validate_form(cls, form):
        data = cls.form2dict(form)
        return cls.validate_data(data)
    
    @classmethod
    def validate_data(cls, data):
        if cls.filter is False:
            return data
        for key, value in data.items():
            data[key] = cls.substitute_special(value)
        return data

    @classmethod
    def validate_html(cls, value):
        if cls.filter is False:
            return value
        expr = r'[\\,\-,\',\*,\.,\,,\%,\<,\>]'
        try:
            result = re.sub(expr, '', value)
            result = result.strip()
        except TypeError:
            result = value
        return result