import requests
from django.http import JsonResponse
from django.views import View
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

SERVICE_MAP = {
    'users': 'http://user-service:8000',
    'patient': 'http://patient-service:8000',
    'doctor': 'http://doctor-service:8000',
    # 'appointment': 'http://appointment-service:8003',
    # add other services here
}

@method_decorator(csrf_exempt, name='dispatch')
class ProxyView(View):
    def dispatch(self, request, service_name, path='', *args, **kwargs):
        if service_name not in SERVICE_MAP:
            return JsonResponse({'error': f'Service "{service_name}" not found'}, status=404)
        
        base_url = SERVICE_MAP[service_name].rstrip('/')
        path = path.lstrip('/')
        target_url = f"{base_url}/{path}"

        # Thêm query string nếu có
        query_string = request.META.get('QUERY_STRING', '')
        if query_string:
            target_url = f"{target_url}?{query_string}"

        headers = {k: v for k, v in request.headers.items()}
        headers.pop('Host', None)
        headers.pop('Content-Length', None)

        data = request.body if request.method in ['POST', 'PUT', 'PATCH'] else None

        try:
            resp = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                data=data,
                allow_redirects=True,
            )
            try:
                content = resp.json()
                return JsonResponse(content, status=resp.status_code, safe=False)
            except ValueError:
                return HttpResponse(resp.content, status=resp.status_code, content_type=resp.headers.get('Content-Type', 'text/plain'))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
def home(request):
    return render(request, 'gateway_app/home.html') 