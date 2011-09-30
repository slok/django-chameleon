Installation
============

Dependencies
------------

* Django (Depends on the method)
    * Loader method: Django >= 1.2
    * TemplateResponse method: Django = 1.3
* Python >= 2.4 (I use 2.6)
* Session middleware (database. if you use db session store)
* sphinx [Optional for the docs]

Options
-------

There are some options to put them in settings.py, a few of them are necessary, the rest are optional.

CHAMELEON_AUTOMATED
~~~~~~~~~~~~~~~~~~~
* Optional
* Type: Boolean
* Default: True

This option will automate the process of theme changing. If is activated, the theme will be changed in the session variable, 
in the request context and in the loader or middleware. If the flag is False then the user is the one that has to 
change the theme, for example in the views, The session and the request context are automaticm, but the loader or the 
middleware(theme setter) not. 
Example::
 
    CHAMELEON_AUTOMATED = True
 

CHAMELEON_FORM_KEY
~~~~~~~~~~~~~~~~~~
* Optional
* Type: String
* Default: 'theme'

This option is to set the name where the theme selection will be placed in the GET and POST
Example::

    CHAMELEON_FORM_KEY = ''


CHAMELEON_DEFAULT_THEME
~~~~~~~~~~~~~~~~~~~~~~~

* Optional
* Type: String
* Default: 'default'

This option is to set the default name of the primary or default theme
Example::

    CHAMELEON_DEFAULT_THEME = ''


CHAMELEON_CONTEXT_KEY
~~~~~~~~~~~~~~~~~~~~~
* Optional
* Type: String
* Default: 'theme'

This option is to set the request context variable name, to access from the templates, for example with ``{{ theme }}``
Example::

    CHAMELEON_CONTEXT_KEY = ''


CHAMELEON_COOKIE_KEY
~~~~~~~~~~~~~~~~~~~~
* Optional
* Type: String
* Default: 'theme'

This option is to set the session/cookie variable name.
Example::

    CHAMELEON_COOKIE_KEY = ''


DEFAULT_LEVEL_CUT
~~~~~~~~~~~~~~~~~
* Optional
* Type: Integer
* Default: 0

If you want to put the default theme in a subfolder where the other themes aren't placed you could say how many levels to remove 
from the default path (like in patch/diff ;) )

Example with no cut level::

    template root folder: /templates
    default theme: /templates/default/*.html
    blue theme: /templates/default/blue/*.html

Example with cut level 1::

    template root folder: /templates
    default theme: /templates/default/*.html
    blue theme: /templates/blue/*.html

Example::

    DEFAULT_LEVEL_CUT = 0


CHAMELEON_SITE_THEMES
~~~~~~~~~~~~~~~~~~~~~
* **Not** optional
* Type: Dictionary
    * key(name): String
    * value(path): String

This option is necessary to know where and wich are the themes. If some theme path is void ('') then the app asumes that the 
path is the name of the theme. The structure inside the theme (f.e: blue) has to be the same as the default one. The path is 
from the template root folder (normally is ``templates/``)  

Example::

    CHAMELEON_SITE_THEMES = {
        'green':'themes/green',
        'black':'themes/black',
        'blue': 'blue',
        'red':'',
    }


Template change methods
-----------------------

Chameleon manages two methods to change the themes, ``Loader`` and the new Django TemplateResponse_ both have good and bad things.

The loader methos is the old one, this is the common one that have been used when we wanted to interact with the response of the view 
before rendering. 
The other method is new in Django 1.3, This method has been made to interact with the view return data before creating the response 
and rendering (middleware). The preffered way is the new templateResponse method. The differences are this:

Loader
~~~~~~

* No need to change anything(only add the loader in ``settings.py``)
* Django 1.2
* Heavier method (in terms of load and time)

TemplateResponse
~~~~~~~~~~~~~~~~

* If the views dont return a simpleTemplateResponse or TemplateResponse we have to change
* Django 1.3
* Middleware, so is clean and very lightweight (fast)
* This method is created for this such of things (it was necessary a method like this and finally we can use it)


.. _TemplateResponse: https://docs.djangoproject.com/en/1.3/ref/template-response/

Use/installation
----------------

Settings variables
~~~~~~~~~~~~~~~~~~

First we have to add the `options`_ that we want in settings.py

.. note:: ``CHAMELEON_SITE_THEMES`` is **not** optional

Also we need to add our contextProcessors to ``TEMPLATE_CONTEXT_PROCESSOR`` this way we can use ``{{theme}}`` 
in templates, to do this::

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

    TEMPLATE_CONTEXT_PROCESSORS += ('chameleon.context_processors.theme',)


Add chameleon to installed apps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In settings add chameleon to INSTALLED_APPS, for example::

    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chameleon',
    )

Add middleware
~~~~~~~~~~~~~~

Add both middlewares to MIDDLEWARE_CLASSES (the second one is only for the TemplateResponse method, but if loader is 
activated in TEMPLATE_LOADERS the SetResponseTemplate middleware disables automatically). Like this::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'chameleon.middleware.DetectTheme',
        'chameleon.middleware.SetResponseTemplate',
    )

Set method (Loader or TemplateResponse)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We have to select the `Template change methods`_ to use when Django has to change the themes

.. note:: TemplateResponse is recommended

Loader
++++++

Add our loader to settings (the first one) for example::

    TEMPLATE_LOADERS = (
        'chameleon.loader.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
    )

.. note:: Place the loader the first one

TemplateResponse
++++++++++++++++

* We don't have to add the loader to TEMPLATE_LOADERS
* All the views have to call the template with TemplateResponse (or SimpleTemplateResponse)

