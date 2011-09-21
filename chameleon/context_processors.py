import utils

def theme(request):
    return {
        utils._local_thread.keys['context']: utils.get_theme_from_cookie(),
    } 
