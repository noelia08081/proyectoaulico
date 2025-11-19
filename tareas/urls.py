from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, PresupuestoViewSet, TransaccionViewSet,
    MetaFinancieraViewSet, LeccionEducativaViewSet, AnalisisViewSet
)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'presupuestos', PresupuestoViewSet, basename='presupuesto')
router.register(r'transacciones', TransaccionViewSet, basename='transaccion')
router.register(r'metas', MetaFinancieraViewSet, basename='meta')
router.register(r'lecciones', LeccionEducativaViewSet, basename='leccion')
router.register(r'analisis', AnalisisViewSet, basename='analisis')

urlpatterns = [
    path('', include(router.urls)),
]

