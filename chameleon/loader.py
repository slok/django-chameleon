from django.template.loader import find_template_loader, BaseLoader
import utils

class Loader(BaseLoader):
    is_usable = True
    """
    def __init__():
        loaders = []
        for loader_name in settings.FLAVOURS_TEMPLATE_LOADERS:
            loader = find_template_loader(loader_name)
            if loader is not None:
                loaders.append(loader)
        self.template_source_loaders = tuple(loaders)
        super(BaseLoader, self).__init__(*args, **kwargs)
    """
    def prepare_template_path(self, template_name):
        """
            Prepares the template path with the cookie theme prefix and the template name
        """
        actual_theme = utils.get_theme_from_local_thread()
        return utils.get_theme_path(actual_theme)


    def load_template(self, template_name, template_dirs=None):
        return self.prepare_template_path(template_name)
        
    def load_template_source(self, template_name, template_dirs=None):
        pass
