from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from forms import ColorForm

def index(request):

    return render_to_response('index.html', {'form': ColorForm()}, context_instance=RequestContext(request))
    #return TemplateResponse(request, 'index.html', {'form': ColorForm()})
