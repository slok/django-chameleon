from chameleon import utils

class DetectTheme(object):
    """
        This middleware will detect if there is a theme var 
        in GET or POST
    """
    
    def process_request(self, request):
        
        utils.get_site_theme(request)
