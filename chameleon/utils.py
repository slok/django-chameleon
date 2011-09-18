import settings
import threading
from datetime import datetime

_local_thread = threading.local()

def get_site_theme(request=None):
    """
        gets the site theme from the cooki, GET or POST
    """
    
    request = request or getattr(_local_thread, 'request', None)
    default = 'theme'
    selected_theme=None
    
    #check if there is a different name for the context var setted in settings
    theme = getattr(settings, 'CHAMELEON_CONTEXT_VAR', None)
    if not theme:
        theme = default
    
    
    #Check if is a request (theme change), if is not then we need to know the seession theme so we look in the cookie
    if request:
        # Check if there is in POST or HEAD a change theme request
        if request.POST.get(theme):
            selected_theme = request.POST.get(theme)
        elif request.GET.get(theme): 
            selected_theme = request.GET.get(theme)
        else:
            pass # I'm comfortable with this pass :D
    else:
        #Check if there is a different name for the cookie var setted in settings
        theme_cookie = getattr(settings, 'CHAMELEON_COOKIE_VAR', None)
        if not theme_cookie:
            theme_cookie = default
        #check the session cookie
        if True:
            pass
        else:
            selected_theme= None
    
    return selected_theme


def set_template_in_response(response):
    """
        Sets the new template to a SimpleTemplateResponse or TemplateResponse
        Needs 1.3 and the use of the commented objects in the views
    """
    
    #get the actual template and modify to get the new path
    actual_template = response.template_name
    
    new_template = actual_template
    
    #set the new template to the response
    response.resolve_template(new_template)
    
    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] Chameleon changed theme template')
    
    return response
