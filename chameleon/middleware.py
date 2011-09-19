import settings
from chameleon import utils
from django.core.exceptions import MiddlewareNotUsed


class DetectTheme(object):
    """
        This middleware will detect if there is a theme var 
        in GET or POST and set the Cookie
    """
    
    
    def process_request(self, request):
        #get from POST and GET
        #TODO: Get from Request context var
        actual_theme = utils.get_site_theme(request)
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
        # Start the checks to stop this middleware (a.k.a don't change the theme!)
        # Note: Init method only is called when the web server starts
        
        # 1- If we want manual management in the templates then we don't need to use this middleware 
        try:
            apply_theme = getattr(settings, 'CHAMELEON_AUTOMATED')
            if not apply_theme:
                raise MiddlewareNotUsed()
                
        except AttributeError: #put exact exception otherwise the MiddlewareNotUsed is catched too
            pass #we don't do anything, act like in the normal (automated) way
        
        # TODO: CHECK IF THERE IS THE LOADER PLACED TO DON'T USE THIS
        
    
    def process_template_response(self, request, response):
        
        
        new_response = utils.set_template_in_response(request, response)
        
        #TODO: Put the Context data
        
        return new_response

