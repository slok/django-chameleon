from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse

def index(request):

    return TemplateResponse(request, 'index.html', {})

    #return render_to_response('index.html', context_instance=RequestContext(request))
