import re

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def limit_content(value, length=100):
    """
    Фильтр для ограничения вывода контента, заменяющий изображения и ссылки на текст '[изображение]' и '[ссылка]'.
    """
    short_content = re.sub(r'<img[^>]*>', '[изображение] ', value.replace('&nbsp;', '').strip())

    short_content = re.sub(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)".*?>.*?</a>',
                           '[ссылка]', short_content)

    short_content = strip_tags(short_content)

    if len(short_content) > length:
        short_content = short_content[:length] + ' ...'

    return mark_safe(short_content)


