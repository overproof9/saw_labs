import re

from app import app


class Validator:
    filter = app.config.get('FILTER', True)
    
    @classmethod
    def form2dict(cls, form):
        return {key: value.data for key, value in form._fields.items()}
    
    @classmethod
    def substitute_special(cls, value):
        expr = r'[\\,\-,\',\*,\.,\,,\%]'
        try:
            result = re.sub(expr, '', value)
            result = result.strip(' \t\n\r')
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
