from django.template.loader import BaseLoader
from django.template import TemplateDoesNotExist 
from datetime import datetime
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
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][LOADER] Call __init__')
        

    def prepare_template_path(self, template_name):
        """
            Prepares the template path with the cookie theme prefix and the template name
        """
        actual_theme = utils.get_theme_from_cookie()
        
        path =  utils.get_theme_path(actual_theme) + template_name
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][LOADER] Call prepare_template_path: '+ path)
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][LOADER] Call prepare_template_path: '+ actual_theme)
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][LOADER] Call prepare_template_path: '+ template_name)
        
        return path

    def load_template(self, template_name, template_dirs=None):
        #we load the new template with the common loaders. If they don't return nothing the exception is captured and pass. 
        #And the last one if returns something doesn't do the raise son this way we know if none of the loaders has found 
        #the template when the final raise executes
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][LOADER] Call load_template')
        
        #check if we have automated mode 
        if getattr(settings, 'CHAMELEON_AUTOMATED', True):
            new_template_name = self.prepare_template_path(template_name)
        else:
            new_template_name = template_name
        print(new_template_name)
        for loader in self.template_source_loaders:
            class_import = import_class_from_str(loader)
            loader_class = class_import()
            try:
                return loader_class.load_template(new_template_name, template_dirs)
            except TemplateDoesNotExist:
                raise TemplateDoesNotExist("Tried %s" % template_name)

        
    def load_template_source(self, template_name, template_dirs=None):
        #similar to load_template
        
        if settings.DEBUG:
            date = datetime.today()
            print('[' + date.strftime('%d/%b/%Y %X') + '] [CHAMELEON][LOADER] Call load_template_source')
        
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
                    raise TemplateDoesNotExist("Tried %s" % template_name)
