from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError, HttpResponse


class ErrorHandler:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            
            if response.status_code == 400:
                return render(request, 'main/error/400.html', status=400)
            
            elif response.status_code == 403:
                return render(request, 'main/error/403.html', status=403)
            
            elif response.status_code == 404:
                return render(request, 'main/error/404.html', status=404)
            
            elif response.status_code == 429:
                return render(request, 'main/error/429.html', status=429)
            
            elif response.status_code == 500:
                return render(request, 'main/error/500.html', status=500)

            return response
        except Exception as e:
            print(f'error handling request {e}')
            return HttpResponseServerError('Internal server error. Please try again later.')
        