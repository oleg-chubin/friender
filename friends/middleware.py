from django.shortcuts import render


class KeyErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        request.foo_value = 12
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        context = {
            'error_message': exception.args,
        }
        if isinstance(exception, KeyError):
            context['error_class'] = 'Super-puper KeyError'
        else:
            return None
        return render(request, 'error.html', context)


class ValueErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        request.foo_value = 12
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        context = {
            'error_message': exception.args,
        }
        if isinstance(exception, ValueError):
            context['error_class'] = 'Super-puper ValueError'
        else:
            context['error_class'] = repr(type(exception))
        return render(request, 'error.html', context)