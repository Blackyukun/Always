# coding: utf-8
import hashlib


def get_background_color(txt):

    return '#%s' % hashlib.md5(bytes(txt, 'utf-8')).hexdigest()[:6]

def avatar_generate(txt, color, size, css_class='sa-avatar', ecls=None):
    """
    :param txt: text for generate
    :param color: css color, like #abc
    :param size: integer, box size
    :param css_class: str, default css_class
    :param ecls: list, extra css classes
    :return: html of avatar
    """
    params = {
        'width': '%spx' % size,
        'height': '%spx' % size,
        'line-height': '%spx' % size,
        'font-size': '%spx' % (size-10),
        'background-color': color,
    }
    char = txt[0]

    if ecls:
        css_classes = '%s %s' % (css_class, ' '.join(ecls))
    else:
        css_classes = css_class

    return u"""<div class="%s" style="%s">%s</div>"""\
           % (css_classes, ';'.join('%s:%s' % x for x in params.items()), char.upper())


def get_avatar_html(txt, size, css_class='sa-avatar', ecls=None, color_func=get_background_color):

    return avatar_generate(txt, color_func(txt), size, css_class, ecls)
