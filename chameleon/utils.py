import settings
import threading
from datetime import datetime
from django.contrib.sessions.models import Session
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext

_local_thread = threading.local()

# The local thread has 3 vars
#   - request
#   - keys
#       * cookie theme key name
#       * context theme key name
#       * default theme
#       * form name
#   - theme
#
# The theme stores in this different places:
#   - Cookie (session)
#   - Local thread
#   - Request context
#

def _init_theme(request):
    """Add the necessary variables to the local thread
        
    :param request: The request object from Django
    """
    global _local_thread
    
    # Check if is properly configured the default theme
    def_theme = getattr(settings, 'CHAMELEON_DEFAULT_THEME')
    if not def_theme:
        raise ImproperlyConfigured('theme not found in CHAMELEON_SITE_THEMES')
    
    # Set the local thread variables
    keys = {
        'cookie': getattr(settings, 'CHAMELEON_COOKIE_KEY', 'theme'),
        'context': getattr(settings, 'CHAMELEON_CONTEXT_KEY', 'theme'),
        'default_theme': def_theme,
        'form': getattr(settings, 'CHAMELEON_FORM_KEY', 'theme'),
        }
        
    _local_thread.keys = keys
    _local_thread.request = request
    
    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Thread local variables setted' )

def get_theme_from_cookie(request = None):
    """Gets the Theme from the session/cookie variable
        
    :param request: The request object from Django. Default is None
    """

    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Get theme from cookie')

    #if we want the theme and we don't have the request, use the local thread data
    if not request:
        return _local_thread.request.session.get(_local_thread.keys['cookie'])
    else:
        return request.session.get(_local_thread.keys['cookie'])
    

def get_theme_from_request(request):
    """Gets the site theme from the GET or POST request. If there is no 
    value then returns None (So there is no change request)
        
    :param request: The request object from Django
    """
    
    selected_theme=None
    request_type = None
    theme_var = _local_thread.keys['form']
    
    #Check if is a request
    if request:
        # Check if there is in POST or HEAD a change theme request
        if request.POST.get(theme_var):
            selected_theme = request.POST.get(theme_var)
            request_POST = 'POST'
        elif request.GET.get(theme_var): 
            selected_theme = request.GET.get(theme_var)
            request_POST = 'GET'
	
        if settings.DEBUG:
            date = datetime.today()
            if not request_type:
                print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] No request')
            else:
                print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Theme '+ selected_theme +' retrieved from ' + request_type + ' request')
            
                
    return selected_theme

def set_theme_in_cookie(request, theme):
    """Sets the key(variable) that we decided (or the default one) in 
    the session cookie, if there is no value, the cookie will be the 
    default theme
        
    :param request: Request object from Django
    :param theme: the theme to set in the session cookie
    """
    
    cookie_theme = get_theme_from_cookie(request)
    
    #If cookie does not exist (new cookie) set the cookie value to default, 
    #otherwise check if there isn't a value in the var (this means that we haven't 
    #request the change of theme and we need to use the previous one)
    if not cookie_theme:
        theme = _local_thread.keys['default_theme']
    elif not theme:
        theme = cookie_theme
        
    #If is the same theme don't do anything
    if cookie_theme != theme:
        request.session[_local_thread.keys['cookie']] = theme
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Cookie setted to: ' + theme)


def set_theme_in_context(request, response):
    """Sets the theme in the context variable inside the response object
    
    :param request: Request object from Django
    :param response: Response object from Django
    """
    
    #create the context data and set the theme variable
    request_context = response.resolve_context(response.context_data)
    request_context[_local_thread.keys['context']] = get_theme_from_cookie(request)
    
    response.context_data = request_context
    
    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Added theme to context data')
    
    
def get_theme_path(theme):
    """returns the full theme path of a given theme
    
    :param theme: the theme name of the theme path we are looking for
    """
    
    t_path = ''
    
    # Check if is properly configured
    try:
        themes_paths = getattr(settings, 'CHAMELEON_SITE_THEMES')
    except AttributeError: 
        if settings.DEBUG: 
            raise ImproperlyConfigured('You must specify the themes paths in CHAMELEON_SITE_THEMES in your settings file')
   
    #check if there is the theme
    if theme in themes_paths:
        # If the path is void, that means that is in the root folder
        if not themes_paths[theme]:
            t_path = ''
        else:
            t_path = themes_paths[theme]

        t_path += '/' #put the last slash
    else:
        if settings.DEBUG and theme != _local_thread.keys['default_theme']:
            raise ImproperlyConfigured('theme '+ theme +' not found in CHAMELEON_SITE_THEMES')

    return t_path
        
def set_template_in_response(request, response):
    """Sets the new template to a SimpleTemplateResponse or 
    TemplateResponse needs 1.3
    
    :param request: Request object from Django
    :param response: Response object from Django
    """
    
    #get the actual template and modify to get the new path
    actual_template = response.template_name
    cookie_theme = get_theme_from_cookie()
    new_template = get_theme_path(cookie_theme) + actual_template
    
    #set the new template to the response
    response.resolve_template(new_template) # template exception if the template doesnt exist
    response.template_name = new_template
    
    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] template updated to: ' + new_template)
    
    return response
