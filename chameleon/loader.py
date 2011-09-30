from django.template.loader import BaseLoader
from django.template import TemplateDoesNotExist 
import utils
import settings

def import_class_from_str(str_module):
    """
    Use this to import a class from a string. For example:
    'django.template.loaders.filesystem.Loader' is converted to:
    from django.template.loaders.filesystem import Loader
    """
    split_module = str_module.split('.')
    mod_class = split_module.pop()
    module = split_module.pop(0)
    
    for i in split_module:
        module = module + '.' + i

    mod = __import__(module, fromlist=[mod_class])
    return getattr(mod, mod_class)
    

class Loader(BaseLoader):
    is_usable = True

    def __init__(self, *args, **kwargs):
        #we want to execute all the loaders that the settings has (except calling ours again and again and... ) with the new template ;)
        loaders = []
        for loader in settings.TEMPLATE_LOADERS:
            if loader != 'chameleon.loader.Loader':
                loaders.append(loader)
        
        self.template_source_loaders = tuple(loaders)
        #super(BaseLoader, self).__init__(*args, **kwargs)
        

    def prepare_template_path(self, template_name):
        """
            Prepares the template path with the cookie theme prefix and the template name
        """
        actual_theme = utils.get_theme_from_cookie()
        
        #cut the levels of the default theme (if necessary)
        try:
            cut_level = getattr(settings, 'DEFAULT_LEVEL_CUT')
            if cut_level > 0:
                template_name = utils.cut_theme_path_level(template_name, cut_level)
        except AttributeError:
            pass
        
        path =  utils.get_theme_path(actual_theme) + template_name
        return path

    def load_template(self, template_name, template_dirs=None):
        #we load the new template with the common loaders. If they don't return nothing the exception is captured and pass. 
        #And the last one if returns something doesn't do the raise son this way we know if none of the loaders has found 
        #the template when the final raise executes
        
        #check if we have automated mode 
        if getattr(settings, 'CHAMELEON_AUTOMATED', True):
            new_template_name = self.prepare_template_path(template_name)
        else:
            new_template_name = template_name
            
        for loader in self.template_source_loaders:
            class_import = import_class_from_str(loader)
            loader_class = class_import()
            try:
                return loader_class.load_template(new_template_name, template_dirs)
            except TemplateDoesNotExist:
                #if the commons fail, use the default theme automatically
                try:
                    return loader_class.load_template(template_name, template_dirs)
                except:
                    pass
        
        raise TemplateDoesNotExist("Tried %s" % template_name)

        
    def load_template_source(self, template_name, template_dirs=None):
        #similar to load_template
        #check if we have automated mode 
        if getattr(settings, 'CHAMELEON_AUTOMATED', True):
            new_template_name = self.prepare_template_path(template_name)
        else:
            new_template_name = template_name
            
        for loader in self.template_source_loaders:
            if hasattr(loader, 'load_template_source'):
                class_import = import_class_from_str(loader)
                loader_class = class_import()
                try:
                    return loader_class.load_template_source(new_template_name, template_dirs)
                except TemplateDoesNotExist:
                    #if the commons fail, use the default theme automatically
                    try:
                        return loader_class.load_template(template_name, template_dirs)
                    except:
                        pass
                        
        raise TemplateDoesNotExist("Tried %s" % template_name)
