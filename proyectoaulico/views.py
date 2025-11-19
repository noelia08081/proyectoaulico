from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def api_root(request):
    """
    Vista raíz que muestra información sobre los endpoints disponibles de la API
    """
    return JsonResponse({
        'message': 'Bienvenido a la API de Educación Financiera',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api': {
                'categorias': '/api/categorias/',
                'presupuestos': '/api/presupuestos/',
                'transacciones': '/api/transacciones/',
                'metas': '/api/metas/',
                'lecciones': '/api/lecciones/',
                'analisis': '/api/analisis/',
            }
        },
        'documentation': 'Consulta los endpoints disponibles en /api/'
    })

