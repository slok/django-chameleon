Chameleon
=========

Description
-----------

Django Chameleon is a dinamic theme (template) changer  for the Django projects. 

Dependencies
------------
* Django >= 1.2 [if we use the loader method]
* Django >= 1.3 [if we use the `TemplateResponse` method]
* Python >= 2.4 (I think, I use 2.6)
* Session middleware (I think that is necessary to save the satatus of the theme)
* RequestContext [OPTIONAL] but recommended

How it works
------------

Chameleon gets the theme from the POST or GET request, then inserts in the session and the request context. You can set and get the theme in the cookie with some methods that are in `chameleon.utils`

Chameleon supports the theme change in two ways. With a loader or using the new [`TemplateResponse`](https://docs.djangoproject.com/en/1.3/ref/template-response/) instead of `HttpResponse` (`render_to_response`...) 
this has been added in **Django 1.3**. For example a view that uses this new feature 
(doesn't change the previous functionality) only manages the response in a different way that the middleware can interact
with the response before rendering. This is an example

    #from django.shortcuts import render_to_response
    #from django.template import RequestContext
    from django.template.response import TemplateResponse
    from forms import ColorForm

    def index(request):

        #return render_to_response('index.html', context_instance=RequestContext(request))
        return TemplateResponse(request, 'index.html', {'form': ColorForm()})


In my opinion I recomend using `TemplateResponse` to not mess with the default Django loaders, or any other custom loaders.

###Settings template structure###

**THE THEMES (TEMPLATES) NEED TO HAVE THE SAME STRUCTURE AS IN THE DEFAULT THEME.** 

For example we have a basic structure inside `templates` (the root where django will search for the templates).
In the root there are `base.html` and `index.html`. `index.html` extends from `base.html` and in the views the template to render is `index.html`.
So we add other themes, **red**, **blue**, **green** and **black**. These themes the only requeriment that need is to have is `index.html` because is the one that 
is rendered from the view. If all the themes want to extend from the same base.html they could. Also they could extend from an individual base.html but 
this has to be put in the template, for example in the blue one the extend from `/templates/blue/base.html` is: `{% extends 'blue/base.html' %}`  

As we can see all the templates have the same structure. default is in `templates`, blue and red are in `templates/xxxx`, and grend and black are  `templates/themes/xxxx` **but always the same structure of templates**


    Templates
    │ 
    ├── base.html
    ├── index.html
    ├── red
    │   ├── [base.html] 
    │   └── index.html
    │ 
    ├── blue
    │   ├── [base.html] 
    │   └── index.html
    │
    └── themes
        ├── black
        │   ├── [base.html] 
        │   └── index.html
        │
        └── green
            ├── [base.html] 
            └── index.html


###Settings variables###

There are some vars that can be set in `settings.py`. `TEMPLATE_CONTEXT_PROCESSOR` and `CHAMELEON_SITE_THEMES` are neccesary, the others are optional. For example:
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    
    TEMPLATE_CONTEXT_PROCESSORS += ('chameleon.context_processors.theme',)

    # Django settings for chameleonTest project.

    # [OPTIONAL] If you want to manage the theme change looking in your templates  manually 
    # with the request context var. Put down this flag
    #CHAMELEON_AUTOMATED = True

    # [OPTIONAL] If you want to name the form var in a different name
    #CHAMELEON_FORM_KEY = ''

    # [OPTIONAL] If you want to name the default theme different to 'default'
    #CHAMELEON_DEFAULT_THEME = ''

    # [OPTIONAL] If you want to change the var name in the context, set this
    #CHAMELEON_CONTEXT_KEY = ''

    # [OPTIONAL] If you want to change the var name in the cookie set this
    #CHAMELEON_COOKIE_KEY = ''


    # The themes and their paths(the path where the structure starts). 
    # The structure of the theme has to be the same as the default one.
    # If a empty then the name of the theme will be the folder to search in  
    CHAMELEON_SITE_THEMES = {
        'green':'themes/green',
        'black':'themes/black',
        'blue': 'blue',
        'red':'',
    }
    
###Add chameleon to installed apps###
In settings add chameleon to `INSTALLED_APPS`, for example: 
    
    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chameleon',
    
###Add middleware###
Add both middlewares to `MIDDLEWARE_CLASSES` (the second one is only for the TemplateResponse method, but if loader is activated in `TEMPLATE_LOADERS` the SetResponseTemplate middleware disables automatically)

    'chameleon.middleware.DetectTheme',
    'chameleon.middleware.SetResponseTemplate',

###Select method. `loader` or `TemplateResponse`###

We have to select the method to change the theme between Loader and TemplateResponse(Recommended)

####Loader####

Add our loader to settings (**the first one**) for example:


    TEMPLATE_LOADERS = (
        'chameleon.loader.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',


####TemplateResponse####

* We **don't** have to add the loader to `TEMPLATE_LOADERS` 
* All the views have to call the template with TemplateResponse (or SimpleTemplateResponse)



####Other####

If you want that the default option of the form (theme choice) renders the theme that currently is activated you have to use `chameleon.utils` methods like is in the example(`views.py`). The example shows how to use the app with a basic example

Current status
--------------

* Initial state
* Basic functionality
* No installer
* Not many tests
* Many bugs :D

License
-------

3 clause/New BSD license: [opensource](http://www.opensource.org/licenses/BSD-3-Clause), [wikipedia](http://en.wikipedia.org/wiki/BSD_licenses)

Thanks
------
Thanks to [django-mobile](https://github.com/gregmuellegger/django-mobile) for the inspiration and code learning :)
