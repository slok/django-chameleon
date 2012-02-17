import utils

def theme(request):
    """
        Sets in the context processor the theme variable. By default the name is "theme"
        
        :param request: The request object from Django
    """
    return {
        utils._local_thread.keys['context']: utils.get_theme_from_cookie(),
    } 
