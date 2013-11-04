#coding:utf-8
from django.forms.util import ErrorDict
from django.core.validators import RegexValidator


class NgModelFormMixin(object):
    """
    Add this NgModelFormMixin to every class derived from forms.Form, if
    you want to manage that form through an Angular controller.
    It adds attributes ng-model, and optionally ng-change, ng-class and ng-style
    to each of your input fields.
    If form validation fails, the ErrorDict is rewritten in a way, so that the
    Angular controller can access the error strings using the same key values as
    for its models.

    TODO: Нужно добавить функционал чтобы ng-pattern принимал список паттернов
    """

    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.get('prefix')
        self.scope_prefix = kwargs.pop('scope_prefix', None)

        if self.prefix and kwargs.get('data'):
            kwargs['data'] = dict((self.add_prefix(name), value) for name, value in kwargs['data'].get(self.prefix).items())

        for name, field in self.base_fields.items():
            field = self.add_attr(name, field)

        super(NgModelFormMixin, self).__init__(*args, **kwargs)

    def add_attr(self, name, field):
        """
        Добавляем Angular аттрибуты к полю
        """

        identifier = self.add_prefix(name)
        field.widget.attrs['ng-model'] = self.scope_prefix and ('{0}.{1}'.format(self.scope_prefix, identifier)) or identifier
        field.widget.attrs['placeholder'] = field.label

        for validator in field.validators:
            if isinstance(validator, RegexValidator):
                field.widget.attrs['ng-pattern'] = u'/{}/'.format(validator.regex.pattern)
                break        

        if field.min_length:
            field.widget.attrs['ng-minlength'] = field.min_length
        if field.max_length:
            field.widget.attrs['ng-maxlength'] = field.max_length
        if field.required:
            field.widget.attrs['required'] = ''

        return field


    def add_prefix(self, field_name):
        """
        Если у формы есть префикс, то возвращаем имя поля с добавленным к нему префиксом.

        В оригинале она выглядела так:
        return self.prefix and ('{0}-{1}'.format(self.prefix, field_name)) or field_name

        Мы переопределили эту функция так как в Angular префикс указывается через точку.
        """
        return self.prefix and ('{0}.{1}'.format(self.prefix, field_name)) or field_name

    def full_clean(self):
        """
        Rewrite the error dictionary, so that its keys correspond to the model fields.
        """
        super(NgModelFormMixin, self).full_clean()
        if self._errors and self.prefix:
            self._errors = ErrorDict((self.add_prefix(name), value) for name, value in self._errors.items())

    def get_initial_data(self):
        """
        Return a dictionary specifying the defaults for this form. This dictionary
        shall be used to inject the initial values for an Angular controller using
        the directive 'ng-init={{thisform.get_initial_data|js|safe}}'.
        """
        data = {}
        for name, field in self.fields.items():
            if hasattr(field, 'widget') and 'ng-model' in field.widget.attrs:
                data[name] = self.initial and self.initial.get(name) or field.initial
        return data
