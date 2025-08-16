# a custom Context-Processor is used to populate the global template scope with additional
# values. this example fetches the current basket-count and provides this value for templates
# creating a custom process is quite easy
#   https://docs.djangoproject.com/en/5.2/ref/templates/api/#writing-your-own-context-processors
#
# it needs to be configured in the settings.py TEMPLATES > OPTIONS > context_processors


def url_path(request):
    path = "/"
    full_path = request.path_info
    if full_path != "":
        path_elements = full_path.split("/")
        if len(path_elements) > 1:
            path = path_elements[1]
    return {"url_path": path}
