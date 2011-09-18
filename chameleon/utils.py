import settings
import threading
from datetime import datetime
from django.contrib.sessions.models import Session

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
            
        #only call to set the cookie when we change the theme (although the method checks if the theme has change)
        set_theme_in_cookie(request, selected_theme) 
    else:
        pass
    
    return selected_theme



def set_theme_in_cookie(request, theme):
    """
        Sets the key(variable) that we decided (or the default one) in the session
        cookie, if there is no value, the cookie will be 'default' and means that 
        the default theme is going to be used
    """
    
    cookie_key = getattr(settings, 'CHAMELEON_COOKIE_VAR', 'theme')
    cookie_theme = request.session.get(cookie_key)
    
    #If cookie does not exist (new cookie) set the cookie value to default, 
    #otherwise check if there isn't a value in the var (this means that we haven't 
    #request the change of theme and we need to use the previous one)
    if not cookie_theme:
        theme = 'default'
    elif not theme:
        theme = cookie_theme
        
    #If is the same theme don't do anything
    if cookie_theme != theme:
        request.session[cookie_key] = theme
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Cookie setted to: ' + theme)

def check_theme_in_request_cookie(request, theme):
    """
        checks if the cookie (request)theme value is the same as the theme arg
        returns True if is the same
    """
    
    cookie_key = getattr(settings, 'CHAMELEON_COOKIE_VAR', 'theme')
    cookie_theme = request.session.get(cookie_key)
    return cookie_theme == theme    
    

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
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] theme template changed to: ' + new_template)
    
    return response

