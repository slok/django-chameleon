#from django.shortcuts import render_to_response
#from django.template import RequestContext
from django.template.response import TemplateResponse
from chameleon import utils, forms
import sys

def appIndex(request):

    actual_theme = utils.get_theme_from_cookie(request)
    data = {
        'form': forms.ColorForm(initial = {'theme' : actual_theme})
    }
    
    #return render_to_response('index.html', data, context_instance=RequestContext(request))
    return TemplateResponse(request, 'exampleApp/index.html', data)

def sysInfo(request):

    actual_theme = utils.get_theme_from_cookie(request)
    data = {
        'form': forms.ColorForm(initial = {'theme' : actual_theme}),
        'path': sys.path,
        'modules': sys.modules,
        'system': sys.platform,
        'prefix': sys.prefix,
        'version': sys.version,
        'python_legal': sys.copyright,
    }

    return TemplateResponse(request, 'exampleApp/sys.html', data)
