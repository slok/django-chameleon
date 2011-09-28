#from django.shortcuts import render_to_response
#from django.template import RequestContext
from django.template.response import TemplateResponse
from forms import ColorForm
from chameleon import utils

def index(request):

    actual_theme = utils.get_theme_from_cookie(request)
    data = {
        'form': ColorForm(initial = {'theme' : actual_theme})
    }
    
    #return render_to_response('index.html', data, context_instance=RequestContext(request))
    return TemplateResponse(request, 'index.html', data)
