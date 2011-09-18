from chameleon import utils

class DetectTheme(object):
    """
        This middleware will detect if there is a theme var 
        in GET or POST and set the Cookie
    """
    
    def process_request(self, request):
        
        utils.get_site_theme(request)

class SetResponseTemplate(object):
    """
        Sets the theme if the new SimpleTemplateResponse or 
        TemplateResponse is used (new in 1.3)
        https://docs.djangoproject.com/en/1.3/ref/template-response/
        This way is to not use a custom Loader ;)
    """
    def process_template_response(self, request, response):
        
        new_response = utils.set_template_in_response(response)
        
        return new_response

