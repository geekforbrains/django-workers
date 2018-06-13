from importlib import import_module


def autodiscover(log):
    """
    Autodiscover tasks.py files in much the same way as admin app
    """
    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        log('searching {0}'.format(app))
        try:
            app_path = import_module(app).__path__
        except (AttributeError, ImportError):
            continue
        try:
            imp.find_module('tasks', app_path)
        except ImportError:
            continue

        log('found: {0}.tasks'.format(app))
        import_module("%s.tasks" % app)
