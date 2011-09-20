Chameleon
=========

Description
-----------

Django Chameleon is a theme changer  for our Django projects. 

How it works
------------

At the moment chameleon only supports using the new [`TemplateResponse`](https://docs.djangoproject.com/en/1.3/ref/template-response/) over `HttpResponse` (`render_to_response`...) 
this has been added in **Django 1.3** so this is the first dependency. For example a view that uses this new feature 
(doesn't change the previous functionality) only manages the response in a different way that the middleware can interact
with the response before rendering. This is an example

    #from django.shortcuts import render_to_response
    #from django.template import RequestContext
    from django.template.response import TemplateResponse
    from forms import ColorForm

    def index(request):

        #return render_to_response('index.html', context_instance=RequestContext(request))
        return TemplateResponse(request, 'index.html', {'form': ColorForm()})


In the future I plan implementing a new loader that the 1.3 version could not be used and so not the `TemplateResponse`. In particular I recomend using 
`TemplateResponse` to not mess with the default Django loaders, or any other custom loaders.

You can run the simple test site that comes with the app. 

Current status
--------------

**BASIC FUNCTIONALITY**

License
-------

3 clause/New BSD license: [opensource](http://www.opensource.org/licenses/BSD-3-Clause), [wikipedia](http://en.wikipedia.org/wiki/BSD_licenses)
