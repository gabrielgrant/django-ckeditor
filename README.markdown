django-ckeditor
===============

`django-ckeditor` makes it easy to use [CKEditor][] with your Django text
fields.

[CKEditor]: http://ckeditor.com/

Setup
-----

Install the package with [pip][] and [Mercurial][] or [git][]:

    pip install -e hg+http://bitbucket.org/dwaiter/django-ckeditor#egg=django-ckeditor
    
    # or ...
    
    pip install -e git://github.com/dwaiter/django-ckeditor.git#egg=django-ckeditor

[pip]: http://pip.openplans.org/
[Mercurial]: http://hg-scm.org/
[git]: http://git-scm.com/

Add `ckeditor` to your `INSTALLED_APPS`.

If you are not using the [staticfiles app][], see the "Static Media Setup"
section (at the end of this document). `staticfiles` is shipped as a contrib
app in Django >= 1.3 and is also available as [django-staticfiles][] for
earlier versions.

[staticfiles app]: http://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/
[django-staticfiles]: http://pypi.python.org/pypi/django-staticfiles/

If you would like to use [configuration settings][] other
than CKEditor's defaults, add a `CKEDITOR_CONFIGS` variable to your
`settings.py` with at least a `default` config:

[configuration settings]: http://docs.cksource.com/ckeditor_api/symbols/CKEDITOR.config.html

    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': [
                [      'Undo', 'Redo',
                  '-', 'Bold', 'Italic', 'Underline',
                  '-', 'Link', 'Unlink', 'Anchor',
                  '-', 'Format',
                  '-', 'SpellChecker', 'Scayt',
                  '-', 'Maximize',
                ],
                [      'HorizontalRule',
                  '-', 'Table',
                  '-', 'BulletedList', 'NumberedList',
                  '-', 'Cut','Copy','Paste','PasteText','PasteFromWord',
                  '-', 'SpecialChar',
                  '-', 'Source',
                  '-', 'About',
                ]
            ],
            'width': 840,
            'height': 300,
            'toolbarCanCollapse': False,
        }
    }

Usage
-----

To use CKEditor for a particular field in a form, set its widget to an
instance of `ckeditor.widgets.CKEditor` like this:

    from ckeditor.widgets import CKEditor
    
    class SampleForm(forms.Form):
        body = forms.CharField(
            widget=CKEditor()
        )
    

As a shortcut you can use a `ckeditor.fields.HTMLField` instead of
`django.db.models.TextField` in a model to automatically use the CKEditor
widget, like so:

    from django.db import models
    from ckeditor.fields import HTMLField
    
    class Sample(models.Model):
        # This will use a normal <textarea> when rendered in a (Model)Form
        plain_body = models.TextField(blank=True, verbose_name='plain version')
        
        # This will use CKEditor when rendered in a (Model)Form
        html_body = HTMLField(blank=True, verbose_name='HTML version')

Custom Configurations
---------------------

Sometimes it's nice to be able to configure each CKEditor widget separately.
For example, you may want one field to have all the buttons on the toolbar,
but another field to only show bold/italic/underline buttons.

To do this, add additional configurations to your `CKEDITOR_CONFIGS` setting
like this:

    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': [
                [      'Undo', 'Redo',
                  '-', 'Bold', 'Italic', 'Underline',
                  '-', 'Link', 'Unlink', 'Anchor',
                  '-', 'Format',
                  '-', 'SpellChecker', 'Scayt',
                  '-', 'Maximize',
                ],
            ],
            'width': 840,
            'height': 300,
            'toolbarCanCollapse': False,
        },
        
        'simple_toolbar': {
            'toolbar': [
                [ 'Bold', 'Italic', 'Underline' ],
            ],
            'width': 840,
            'height': 300,
        },
    }

When setting up the `CKEditor` widget in your `Form` class you can pass a
`ckeditor_config` keyword argument to specify the config to use. Either
pass the name of a config defined in your settings, or pass a complete
configuration dictionary :

    class BlogPostForm(forms.Form):
        title = forms.CharField()
        
        # This field will render as a CKEditor with the 'simple_toolbar' config.
        subtitle = forms.CharField(
            widget=CKEditor(ckeditor_config='simple_toolbar')
        )
        
        # This field will render as a CKEditor with the 'default' config.
        body = forms.CharField(
            widget=CKEditor()
        )
        
        # This field will render as a CKEditor with the CKEditor's builtin
        # 'Basic' toolbar.
        subtitle = forms.CharField(
            widget=CKEditor(ckeditor_config={'toolbar':'Basic'})
        )
    

You cannot use the `HTMLField` shortcut if you want to specify a custom config
-- you *must* create a form.

### Static Media Setup

By default django-ckeditor will use [Django's staticfiles app]
(http://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/) to serve
its static media. If you aren't using `django.contrib.staticfiles`(or
django-staticfiles on pre-1.3 versions of Django), an additional
setup step is needed so that django-ckeditor find its static files.
Symlink the necessary media and templates:

    ln -s [/full/path/to]/django-ckeditor/ckeditor/static/ckeditor media/ckeditor
    ln -s [/full/path/to]/django-ckeditor/ckeditor/templates/ckeditor templates/ckeditor

### Custom Static Media URL

Even if you are not using `django.contrib.staticfiles`, you can still
customize the URL that django-ckeditor will look for the CKEditor
media at by adding `CKEDITOR_MEDIA_URL` to your `settings.py` file like this:

    CKEDITOR_MEDIA_URL = '/static/third-party/ckeditor'

The default value is `MEDIA_URL/ckeditor` which is why the static media setup
instructions tell you to symlink it into your `media/` directory.
