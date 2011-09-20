import settings
import threading
from datetime import datetime
from django.contrib.sessions.models import Session
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext

_local_thread = threading.local()

#The theme stores in this different places:
#   - Cookie (session)
#   - Local thread
#   - Request context
#

def _init_theme(request):
    """
    We need to access to some variables sometimes and we don't have so we
    push them in the thread data (global) the vars are: request and theme.
    with request we have enough because we have 
    """
    global _local_thread
    _local_thread = threading.local()
    _local_thread.request = request
    _local_thread.theme = None


def get_theme_from_cookie(request):
    
    cookie_key = getattr(settings, 'CHAMELEON_COOKIE_VAR', 'theme')
    cookie_theme = request.session.get(cookie_key)
    
    return cookie_theme


def get_theme_from_request(request):
    """
        gets the site theme from the GET or POST request
    """
    
    default = 'theme'
    selected_theme=None
    
    #check if there is a different name for the cookie var setted in settings
    theme_var = getattr(settings, 'CHAMELEON_COOKIE_VAR', None)
    if not theme_var:
        theme_var = default
    
    #Check if is a request
    if request:
        # Check if there is in POST or HEAD a change theme request
        if request.POST.get(theme_var):
            selected_theme = request.POST.get(theme_var)
        elif request.GET.get(theme_var): 
            selected_theme = request.GET.get(theme_var)
        
    
    return selected_theme

def get_theme_from_local_thread():
    return getattr(_local_thread, 'theme')


def set_theme_in_local_thread(theme):
    global  _local_thread
    
    #If not theme then get from the cookie
    if not theme:
        theme = get_theme_from_cookie(_local_thread.request)

    print theme
    print _local_thread.theme
    #if the cookie hasn't changed then don't update the theme in the thread
    if theme != _local_thread.theme:
        _local_thread.theme =  theme
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Local thread variable setted to: ' + theme)

def set_theme_in_cookie(request, theme):
    """
        Sets the key(variable) that we decided (or the default one) in the session
        cookie, if there is no value, the cookie will be 'default' and means that 
        the default theme is going to be used
    """
    cookie_key = getattr(settings, 'CHAMELEON_COOKIE_VAR', 'theme')
    
    cookie_theme = get_theme_from_cookie(request)
    
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


def set_theme_in_context(request, response):
    
    context_key = getattr(settings, 'CHAMELEON_CONTEXT_VAR', 'theme')
    
    #create the context data and set the theme variable
    request_context = response.resolve_context(response.context_data)
    request_context[context_key] = get_theme_from_cookie(request)
    
    response.context_data = request_context
    
    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Added theme to context data')
    
    
def get_theme_path(theme):
    """
        returns the theme path of a given theme (retrieves from settings)
    """
    t_path = ''
    
    try:
        themes_paths = getattr(settings, 'CHAMELEON_SITE_THEMES')
    except AttributeError: 
        if settings.DEBUG: #shhhhhh... silence
            raise ImproperlyConfigured('You must specify the themes paths in CHAMELEON_SITE_THEMES in your settings file')
        else:
            pass
   
   #check if there is the theme, if there isn't then use the default one ;)
    if theme in themes_paths:
        #If the path is void then use the name of the theme like root folder of the theme
        if not themes_paths[theme]:
            t_path = theme 
        else:
            t_path = themes_paths[theme]

        t_path += '/' #put the last slash
    else:
        if settings.DEBUG and theme != 'default': #shhhhhh... silence
            raise ImproperlyConfigured('theme not found in CHAMELEON_SITE_THEMES')
        else:
            pass

    return t_path
    
        
def set_template_in_response(request, response):
    """
        Sets the new template to a SimpleTemplateResponse or TemplateResponse
        Needs 1.3 and the use of the commented objects in the views
    """
    
    #get the actual template and modify to get the new path
    actual_theme = response.template_name
    cookie_theme = get_theme_from_cookie(request)
    
    #if there is no theme or is the default one, dont do anything
    if not cookie_theme or cookie_theme != 'default':
    
        new_template = get_theme_path(cookie_theme) + actual_theme
        
        #set the new template to the response
        response.resolve_template(new_template) # template exception if the template doesnt exist
        response.template_name = new_template
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] theme template changed to: ' + new_template)
    
    set_theme_in_context(request, response)    
    return response


def check_theme_in_request_cookie(request, theme):
    """
        checks if the cookie (request)theme value is the same as the theme arg
        returns True if is the same
    """
    return theme == get_theme_from_cookie(request)
