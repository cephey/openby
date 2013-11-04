#coding:utf-8

import re
# from datetime import date, timedelta
from django.core.validators import RegexValidator, EmailValidator
# from django.utils.encoding import smart_unicode


# NAME_RE = u'^[а-яёА-Я -]+$'
# DATE_RE = u'^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$'
# YEAR_RE = u'^(19|20)\d\d$'
# EXP_RE = u'^([1-9]{1})([0-9]{0,2})$' # стаж
# PHONE_RE = u'^((\+7)[ ])(\(\d{3}\))(\d{3}[\-])(\d{2}[\-])(\d{2})$'
# HOURS_RE = u'^\d{1,10}$'
# ID_RE = u'^\d{1,4}$'

USERNAME_RE = re.compile(u'^[\w.@+-]+$')
validate_username = RegexValidator(regex=USERNAME_RE)

# EMAIL_RE = email_re
EMAIL_RE = re.compile(u'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$')
validate_email = EmailValidator(regex=EMAIL_RE)

# validate_name = RegexValidator(regex=re.compile(NAME_RE))
# validate_year = RegexValidator(regex=re.compile(YEAR_RE))
# validate_exp = RegexValidator(regex=re.compile(EXP_RE))
# validate_phone = RegexValidator(regex=re.compile(PHONE_RE))
# validate_hours = RegexValidator(regex=re.compile(HOURS_RE))
# validate_id = RegexValidator(regex=re.compile(ID_RE))


# class DateValidator(RegexValidator):

#     def __call__(self, value):
#         if not self.regex.search(smart_unicode(value)):
#             raise ValidationError(self.message, code=self.code)

#         # если дата прошла регулярку то проверяем
#         # что она не больше текущей даты
#         value_date = map(lambda x: int(x), reversed(value.split('.')))

#         if date.today() - date(*value_date) < timedelta(0):
#             raise ValidationError(self.message, code=self.code)

# validate_date = DateValidator(regex=re.compile(DATE_RE))