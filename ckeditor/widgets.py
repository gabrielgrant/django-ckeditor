import re

try:
    import simplejson as json
except ImportError:
    import json

from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

if hasattr(settings, 'CKEDITOR_CONFIGS'):
    CKEDITOR_CONFIGS = dict((k, json.dumps(v)) for k, v in settings.CKEDITOR_CONFIGS.items())
else:
    CKEDITOR_CONFIGS = {}
if 'default' not in CKEDITOR_CONFIGS:
    CKEDITOR_CONFIGS['default'] = '{}'

FILEBROWSER_PRESENT = 'filebrowser' in getattr(settings, 'INSTALLED_APPS', [])
GRAPPELLI_PRESENT = 'grappelli' in getattr(settings, 'INSTALLED_APPS', [])
if hasattr(settings, 'STATIC_URL'):
    MEDIA_URL = '%s/ckeditor' % settings.STATIC_URL.rstrip('/')
else:
    MEDIA_URL = getattr(
        settings, 'CKEDITOR_MEDIA_URL', '%s/ckeditor' % settings.MEDIA_URL.rstrip('/')
    )

_CSS_FILE = 'grappelli.css' if GRAPPELLI_PRESENT else 'standard.css'

class CKEditor(forms.Textarea):
    def __init__(
        self, attrs=None, ckeditor_config='default', *args, **kwargs
    ):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'django-ckeditor'
        kwargs['attrs'] = attrs

        self.ckeditor_config = ckeditor_config

        super(CKEditor, self).__init__(*args, **kwargs)

    def get_ckeditor_config_dict(self):
        if hasattr(self.ckeditor_config, 'items'):
            return self.ckeditor_config
        elif hasattr(settings, 'CKEDITOR_CONFIGS'):
            return settings.CKEDITOR_CONFIGS.get(self.ckeditor_config, {})
        else:
            return {}

    def get_ckeditor_config(self):
        if hasattr(self.ckeditor_config, 'items'):
            config = json.dumps(self.ckeditor_config)
        else:
            config = CKEDITOR_CONFIGS[self.ckeditor_config]
        return config

    def render(self, name, value, attrs=None, **kwargs):
        final_attrs = self.build_attrs(attrs)
        if 'ckeditor_config' in final_attrs:
            config = self.get_ckeditor_config_dict()
            config.update(final_attrs.pop('ckeditor_config'))
            self.ckeditor_config = config
        rendered = super(CKEditor, self).render(name, value, attrs)
        context = {
            'name': name,
            'config': self.get_ckeditor_config(),
            'filebrowser': FILEBROWSER_PRESENT,
        }
        return rendered +  mark_safe(render_to_string(
            'ckeditor/ckeditor_script.html', context
        ))

    def value_from_datadict(self, data, files, name):
        val = data.get(name, u'')
        r = re.compile(r"""(.*?)(\s*<br\s*/?>\s*)*\Z""", re.MULTILINE | re.DOTALL)
        m = r.match(val)
        return m.groups()[0].strip()

    class Media:
        js = (
            MEDIA_URL.rstrip('/') + '/ckeditor/ckeditor.js',
        )
        css = {
            'screen': (
                MEDIA_URL.rstrip('/') + '/css/' + _CSS_FILE,
            ),
        }



class AdminCKEditor(admin_widgets.AdminTextareaWidget, CKEditor):
    pass

