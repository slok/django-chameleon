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
#   - theme
#
#The theme stores in this different places:
#   - Cookie (session)
#   - Local thread
#   - Request context
#

def _init_theme(request):
    """
    We need to access to some variables sometimes and we don't have so we
    push them in the thread. Also we add some others for convenience
    """
    global _local_thread
    
    _local_thread = threading.local()
    _local_thread.request = request
    #_local_thread.theme = None
    
    keys = {
        'cookie': getattr(settings, 'CHAMELEON_COOKIE_KEY', 'theme'),
        'context': getattr(settings, 'CHAMELEON_CONTEXT_KEY', 'theme'),
        'default_theme': getattr(settings, 'CHAMELEON_DEFAULT_THEME', 'default'),
        'form': getattr(settings, 'CHAMELEON_FORM_KEY', 'theme'),
        }

    _local_thread.keys = keys
    

def get_theme_from_cookie(request = None):
    """
        Gets the Theme from the session/cookie variable
    """

    #if we want the theme and we don't have the request, use the local thread data
    if not request:
        return _local_thread.request.session.get(_local_thread.keys['cookie'])
    else:
        return request.session.get(_local_thread.keys['cookie'])
    

def get_theme_from_request(request):
    """
        gets the site theme from the GET or POST request
        If there is no value then returns None (So there is no change request)
    """
    
    selected_theme=None
    
    theme_var = _local_thread.keys['form']
    
    #Check if is a request
    if request:
        # Check if there is in POST or HEAD a change theme request
        if request.POST.get(theme_var):
            selected_theme = request.POST.get(theme_var)
        elif request.GET.get(theme_var): 
            selected_theme = request.GET.get(theme_var)
    
    return selected_theme
"""
def set_theme_in_local_thread(theme=None):
    global  _local_thread
    
    #If not theme then get from the cookie
    if not theme:
        theme = get_theme_from_cookie(_local_thread.request)
   
    _local_thread.theme =  theme
    if settings.DEBUG:
        date = datetime.today()
        print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] Local thread variable setted to: ' + theme)
"""

def set_theme_in_cookie(request, theme):
    """
        Sets the key(variable) that we decided (or the default one) in the session
        cookie, if there is no value, the cookie will be 'default' and means that 
        the default theme is going to be used
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
    """
        Sets the theme in the context variable inside the response object
    """
    
    #create the context data and set the theme variable
    request_context = response.resolve_context(response.context_data)
    request_context[_local_thread.keys['context']] = get_theme_from_cookie(request)
    
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
        if settings.DEBUG and theme != _local_thread.keys['default_theme']: #shhhhhh... silence
            raise ImproperlyConfigured('theme not found in CHAMELEON_SITE_THEMES')
        else:
            pass

    return t_path

def cut_theme_path_level(templatePath, level):
    """
        Cuts the path level with the integer that is passed to the function. For example:
        /f1/f2/f3/xxx with cut leve 1 is /f2/f3/xxx
    """
    split_path = templatePath.split('/')
    split_path.pop(0) #the first one is empty because the string starts with '/' so we removed from list
    #if the level is equal or higher than the path then exception
    if len(split_path) > level:
        #remove levels
        for i in range(level):
            split_path.pop(0)
        
        #create the new path with the remain levels of the path
        if len(split_path) == 1:
            final_path = split_path.pop(0)
        else:
            final_path = ''
            for i in split_path:
                final_path = final_path + '/' + i
        
        return final_path
         
    elif settings.DEBUG: #shhhhhh... silence
        raise ImproperlyConfigured('Your cut level in "DEFAULT_LEVEL_CUT" is higher or equal than the path levels')
        
def set_template_in_response(request, response):
    """
        Sets the new template to a SimpleTemplateResponse or TemplateResponse
        Needs 1.3 and the use of the commented objects in the views
    """
    
    #get the actual template and modify to get the new path
    actual_theme = response.template_name
    cookie_theme = get_theme_from_cookie(request)
    
    #if there is no theme or is the default one, dont do anything
    if cookie_theme or cookie_theme != _local_thread.keys['default_theme']:
    
        #cut the levels of the default theme (if necessary)
        try:
            cut_level = getattr(settings, 'DEFAULT_LEVEL_CUT')
            if cut_level > 0:
                actual_theme = cut_theme_path_level(actual_theme, cut_level)
        except AttributeError:
            pass
        
        new_template = get_theme_path(cookie_theme) + actual_theme
        #set the new template to the response
        response.resolve_template(new_template) # template exception if the template doesnt exist
        response.template_name = new_template
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON] theme template changed to: ' + new_template)
    
    
    return response
