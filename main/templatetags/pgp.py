from django import template
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

def format_key(key_id):
    if len(key_id) in (8, 20):
        return u'0x%s' % key_id
    elif len(key_id) == 40:
        # normal display format is 5 groups of 4 hex chars seperated by spaces,
        # double space, then 5 more groups of 4 hex chars
        split = tuple(key_id[i:i+4] for i in range(0, 40, 4))
        return u'%s&nbsp; %s' % (' '.join(split[0:5]), ' '.join(split[5:10]))
    return u'0x%s' % key_id

@register.simple_tag
def pgp_key_link(key_id):
    if not key_id:
        return "Unknown"
    # Something like 'pgp.mit.edu:11371'
    pgp_server = getattr(settings, 'PGP_SERVER', None)
    if not pgp_server:
        return format_key(key_id)
    url = 'http://%s/pks/lookup?op=vindex&amp;fingerprint=on&amp;exact=on&amp;search=0x%s' % \
            (pgp_server, key_id)
    values = (url, format_key(key_id), key_id[-8:])
    return '<a href="%s" title="PGP key search for %s">0x%s</a>' % values

@register.filter
def pgp_fingerprint(key_id, autoescape=True):
    if not key_id:
        return u''
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    return mark_safe(format_key(esc(key_id)))
pgp_fingerprint.needs_autoescape = True

# vim: set ts=4 sw=4 et:
