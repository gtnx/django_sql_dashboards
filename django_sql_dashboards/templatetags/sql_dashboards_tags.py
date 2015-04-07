# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

from django import template
from django.utils.numberformat import format

register = template.Library()


@register.filter
def floatdot(value, decimal_pos=4):
    return format(value, ".", decimal_pos)
floatdot.is_safe = True
