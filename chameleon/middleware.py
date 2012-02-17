import settings
from chameleon import utils
from django.core.exceptions import MiddlewareNotUsed
from datetime import datetime

class DetectTheme(object):
    """
        This middleware will detect if there is a theme var 
        in GET or POST and set the Cookie
    """
    
    
    def process_request(self, request):
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][DETECT_THEME MIDDLEWARE] Process request')
            
        #Init the variables
        utils._init_theme(request)
        #get from POST and GET
        actual_theme = utils.get_theme_from_request(request)
        
        #set the theme in the local thread
        #utils.set_theme_in_local_thread(actual_theme)
        
        #set the cookie
        utils.set_theme_in_cookie(request, actual_theme) 
        
        
        

class SetResponseTemplate(object):
    """
        Sets the theme if the new SimpleTemplateResponse or 
        TemplateResponse is used (new in 1.3)
        https://docs.djangoproject.com/en/1.3/ref/template-response/
        This way is for not using a custom Loader ;)
    """
    
    def __init__(self):
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][SET_RESPONSE_TEMPLATE MIDDLEWARE] Init')
        
        # Start the checks to stop this middleware (a.k.a don't change the theme!)
        # Note: Init method only is called when the web server starts
        
        # 1- If we want manual management in the templates then we don't need to use this middleware 
        try:
            apply_theme = getattr(settings, 'CHAMELEON_AUTOMATED')
            if not apply_theme:
                raise MiddlewareNotUsed()
                
        except AttributeError: #put exact exception otherwise the MiddlewareNotUsed is catched too
            pass #we don't do anything, act like in the normal (automated) way
        
        #2- if the loader is active then we don't need  this middleware
        if 'chameleon.loader.Loader' in settings.TEMPLATE_LOADERS:
            raise MiddlewareNotUsed()
        
    
    def process_template_response(self, request, response):
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][SET_RESPONSE_TEMPLATE MIDDLEWARE] Process template response')
        
        # set the Context data. We don't need, the context_processors.py puts automatically
        #utils.set_theme_in_context(request, response)   
        
        # set the new template ;)
        new_response = utils.set_template_in_response(request, response)
        
        return new_response

