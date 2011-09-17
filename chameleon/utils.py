import settings


def get_site_theme(request=None):
    
    #check if there is a different name for the context var setted in settings
    theme = getattr(settings, 'CHAMELEON_CONTEXT_NAME', None)
    
    if not theme:
        theme = 'theme'
        
    selected_theme= None
    
    #Check if is a request, if is not
    if request:
        # Check if there is in POST or HEAD a change theme request
        if request.POST.get(theme):
            selected_theme = request.POST.get(theme)
        elif request.GET.get(theme): 
            selected_theme = request.GET.get(theme)
        else:
            pass # I'm comfortable with this passes :D
    else:
        pass
    
    print selected_theme
