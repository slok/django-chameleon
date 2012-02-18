Chameleon
=========

**[Update needed] documentation at: [readTheDocs](http://readthedocs.org/docs/django-chameleon/)**

Description
-----------

Django Chameleon is a dynamic theme (template) changer  for the Django projects. Sometimes a user wants to select the best theme
to read or navigate throug a webpage. Some users like dark backgrounds and light letters, othres prefer minimalistic web pages...
With Django chameleon you have the chance to bring all the themes you want to yout webpage

Dependencies
------------
* Django >= 1.2 [if we use the loader method]
* Django >= 1.3 [if we use the `TemplateResponse` method]
* Python >= 2.4 (I think, I use 2.6)
* Session middleware
* Session storage (database, filesystem...)
* RequestContext [OPTIONAL] but recommended

How it works
------------

Chameleon gets the theme from the POST or GET request, then inserts in the session and the request context. You can set and get the 
theme in the cookie with some methods that are in `chameleon.utils`

Chameleon supports the theme change in two ways. With a loader or using the new 
[`TemplateResponse`](https://docs.djangoproject.com/en/1.3/ref/template-response/) instead of `HttpResponse` (`render_to_response`...) 
this has been added in **Django 1.3**. 

For example a view that uses this new feature only manages the response in a different way, with this method the middleware can interact
with the response before rendering. This is an example

    #from django.shortcuts import render_to_response
    #from django.template import RequestContext
    from django.template.response import TemplateResponse
    from forms import ColorForm

    def index(request):

        #return render_to_response('index.html', context_instance=RequestContext(request))
        return TemplateResponse(request, 'index.html', {'form': ColorForm()})


Is recomended using `TemplateResponse` to not mess with the default Django loaders, or any other custom loaders.

Settings template structure
---------------------------

**THE THEMES (TEMPLATES) NEED TO HAVE THE SAME STRUCTURE AS IN THE DEFAULT THEME.** 

The template structure in the porject using Django chameleon, can be cmplex or simple. 

*All the templates need to have identical struncture*

The themes are placed in the root folder of our template folders, normally `templates`. Django chameleon only manages final templates,
this means that only manages the templates that are asked from the views, the "extend" templates inside the html webpages has to be 
manage by the user.

This has pros and cons. The cons is that isn't managed automatically, the pros is that if all the themes placed in subfolders inside the root folder of the templates
want to extend from base.html (in the root folder) they can. For example two themes that extend from the same html:

    templates
    │ 
    ├── base.html
    │
    ├── bootstrap
    │   └── index.html
    │ 
    └── minimalism
        └── index.html


Django chameleon also supports templates in apps the same way that supports the templates in the main level. 
The apps templates can extend from root templates htmls. 

For example we have the blog app:

    djangoProject
    │ 
    ├─ settings.py
    ├─ urls.py
    ├─ ...
    │
    ├─ blog
    │   ├─ settings.py
    │   ├─ urls.py
    │   ├─ ...
    │   └─ templates
    │       │
    │       ├── bootstrap
    │       │   └─ blogTemplates
    │       │       └── blog_index.html
    │       │ 
    │       └── minimalistic
    │           └─ blogTemplates
    │               └── blog_index.html
    │
    └─templates
        │ 
        ├── base.html
        │
        ├── bootstrap
        │   └── index.html
        │ 
        └── minimalism
            └── index.html


Getting started!
----------------

To set up django chameleon we need to set up various things. The first one is the 
conext processor. In settings.py we set this

    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    
    TEMPLATE_CONTEXT_PROCESSORS += ('chameleon.context_processors.theme',)

Next we need to set up the needded variables for Chameleon

    # If you want to name the default theme different to 'default'
    CHAMELEON_DEFAULT_THEME = 'bootstrap'

    # The themes and their paths(the path where the structure starts). 
    # The strucutre of the theme has to be the same as the default one.
    CHAMELEON_SITE_THEMES = {
        'bootstrap':'bootstrap',
        'minimal':'minimalism',
    }


In settings add chameleon to `INSTALLED_APPS`, for example: 
    
    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chameleon',


Now we need to select wich method want to use fro Chameleon. Could be 
middleware (recommended) or loader

###Middleware method###
If middleware is selected add to `MIDDLEWARE_CLASSES` 
(the second one is only for the TemplateResponse method,
but if loader is activated in `TEMPLATE_LOADERS` the SetResponseTemplate
 middleware disables automatically)

    'chameleon.middleware.DetectTheme',
    'chameleon.middleware.SetResponseTemplate',


With the middleware method we need to manage our views in a different way (not much trouble ;D)

For example, normally we can do:

    from django.shortcuts import render_to_response
    from django.template import RequestContext
    from chameleon import utils, forms

    def index(request):

        actual_theme = utils.get_theme_from_cookie(request)
        data = {
            'form': forms.ColorForm(initial = {'theme' : actual_theme})
        }
        
        return render_to_response('index.html', data, context_instance=RequestContext(request))

But now we need to use the templateResponse method. So we do this way:


    from django.template.response import TemplateResponse
    from chameleon import utils, forms

    def index(request):

        actual_theme = utils.get_theme_from_cookie(request)
        data = {
            'form': forms.ColorForm(initial = {'theme' : actual_theme})
        }
        
        return TemplateResponse(request, 'index.html', data)

###Loader method###
We need to add a middleware (yes I know...the other 
method is the middleware method ¬¬. But the loader needs to detect the 
theme so needs one middleware too, not two). Add to `MIDDLEWARE_CLASSES`

    'chameleon.middleware.DetectTheme',


Add our loader to settings (**the first one**) for example:


    TEMPLATE_LOADERS = (
        'chameleon.loader.Loader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',



Current status
--------------

* Beta release near alpha (testing)
* Milestone: 1.0 (stable release)
* Two ways of using it
* Installer (redo)
* No test
* Example
* Bugs :D

License
-------

3 clause/New BSD license: [opensource](http://www.opensource.org/licenses/BSD-3-Clause), [wikipedia](http://en.wikipedia.org/wiki/BSD_licenses)

Thanks
------
Thanks to [django-mobile](https://github.com/gregmuellegger/django-mobile) for the inspiration and code learning :)
