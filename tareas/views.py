from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import Categoria, Presupuesto, Transaccion, MetaFinanciera, LeccionEducativa
from .serializers import (
    CategoriaSerializer, PresupuestoSerializer, TransaccionSerializer,
    MetaFinancieraSerializer, LeccionEducativaSerializer
)


class CategoriaViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar categorías"""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def get_queryset(self):
        queryset = Categoria.objects.all()
        tipo = self.request.query_params.get('tipo', None)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        return queryset


class PresupuestoViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar presupuestos"""
    queryset = Presupuesto.objects.all()
    serializer_class = PresupuestoSerializer
    
    def get_queryset(self):
        queryset = Presupuesto.objects.all()
        mes = self.request.query_params.get('mes', None)
        año = self.request.query_params.get('año', None)
        
        if mes:
            queryset = queryset.filter(mes=mes)
        if año:
            queryset = queryset.filter(año=año)
        
        return queryset


class TransaccionViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar transacciones"""
    queryset = Transaccion.objects.all()
    serializer_class = TransaccionSerializer
    
    def get_queryset(self):
        queryset = Transaccion.objects.all()
        tipo = self.request.query_params.get('tipo', None)
        categoria = self.request.query_params.get('categoria', None)
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        if categoria:
            queryset = queryset.filter(categoria_id=categoria)
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def resumen_mensual(self, request):
        """Obtiene resumen financiero del mes actual"""
        ahora = timezone.now()
        mes = int(request.query_params.get('mes', ahora.month))
        año = int(request.query_params.get('año', ahora.year))
        
        transacciones = Transaccion.objects.filter(
            fecha__year=año,
            fecha__month=mes
        )
        
        ingresos = transacciones.filter(tipo='ingreso').aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')
        
        gastos = transacciones.filter(tipo='gasto').aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')
        
        balance = ingresos - gastos
        
        # Gastos por categoría
        gastos_por_categoria = transacciones.filter(tipo='gasto').values(
            'categoria__nombre'
        ).annotate(
            total=Sum('monto')
        ).order_by('-total')
        
        return Response({
            'mes': mes,
            'año': año,
            'ingresos': float(ingresos),
            'gastos': float(gastos),
            'balance': float(balance),
            'gastos_por_categoria': list(gastos_por_categoria)
        })
    
    @action(detail=False, methods=['get'])
    def tendencias(self, request):
        """Obtiene tendencias de los últimos meses"""
        meses = int(request.query_params.get('meses', 6))
        ahora = timezone.now()
        
        datos = []
        for i in range(meses):
            fecha = ahora - timedelta(days=30 * i)
            mes = fecha.month
            año = fecha.year
            
            transacciones = Transaccion.objects.filter(
                fecha__year=año,
                fecha__month=mes
            )
            
            ingresos = transacciones.filter(tipo='ingreso').aggregate(
                total=Sum('monto')
            )['total'] or Decimal('0.00')
            
            gastos = transacciones.filter(tipo='gasto').aggregate(
                total=Sum('monto')
            )['total'] or Decimal('0.00')
            
            datos.append({
                'mes': mes,
                'año': año,
                'ingresos': float(ingresos),
                'gastos': float(gastos),
                'balance': float(ingresos - gastos)
            })
        
        return Response(datos[::-1])  # Invertir para mostrar del más antiguo al más reciente


class MetaFinancieraViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar metas financieras"""
    queryset = MetaFinanciera.objects.all()
    serializer_class = MetaFinancieraSerializer
    
    def get_queryset(self):
        queryset = MetaFinanciera.objects.all()
        estado = self.request.query_params.get('estado', None)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset
    
    @action(detail=True, methods=['post'])
    def agregar_monto(self, request, pk=None):
        """Agrega monto a una meta financiera"""
        meta = self.get_object()
        monto = Decimal(request.data.get('monto', 0))
        meta.monto_actual += monto
        
        if meta.monto_actual >= meta.monto_objetivo:
            meta.estado = 'completada'
        
        meta.save()
        serializer = self.get_serializer(meta)
        return Response(serializer.data)


class LeccionEducativaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para leer lecciones educativas"""
    queryset = LeccionEducativa.objects.filter(activa=True)
    serializer_class = LeccionEducativaSerializer
    
    def get_queryset(self):
        queryset = LeccionEducativa.objects.filter(activa=True)
        nivel = self.request.query_params.get('nivel', None)
        if nivel:
            queryset = queryset.filter(nivel=nivel)
        return queryset


# ViewSet para análisis y estadísticas
class AnalisisViewSet(viewsets.ViewSet):
    """ViewSet para análisis financieros"""
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dashboard con estadísticas generales"""
        ahora = timezone.now()
        mes_actual = ahora.month
        año_actual = ahora.year
        
        # Transacciones del mes actual
        transacciones_mes = Transaccion.objects.filter(
            fecha__year=año_actual,
            fecha__month=mes_actual
        )
        
        ingresos_mes = transacciones_mes.filter(tipo='ingreso').aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')
        
        gastos_mes = transacciones_mes.filter(tipo='gasto').aggregate(
            total=Sum('monto')
        )['total'] or Decimal('0.00')
        
        # Presupuestos del mes
        presupuestos = Presupuesto.objects.filter(mes=mes_actual, año=año_actual)
        total_presupuestado = presupuestos.aggregate(
            total=Sum('monto_limite')
        )['total'] or Decimal('0.00')
        
        # Metas activas
        metas_activas = MetaFinanciera.objects.filter(estado='en_progreso')
        total_metas = metas_activas.aggregate(
            total=Sum('monto_objetivo')
        )['total'] or Decimal('0.00')
        total_ahorrado = metas_activas.aggregate(
            total=Sum('monto_actual')
        )['total'] or Decimal('0.00')
        
        return Response({
            'mes_actual': {
                'ingresos': float(ingresos_mes),
                'gastos': float(gastos_mes),
                'balance': float(ingresos_mes - gastos_mes),
                'presupuesto_total': float(total_presupuestado),
                'presupuesto_usado': float(gastos_mes),
                'presupuesto_restante': float(total_presupuestado - gastos_mes)
            },
            'metas': {
                'total_metas': metas_activas.count(),
                'monto_total_objetivo': float(total_metas),
                'monto_total_ahorrado': float(total_ahorrado),
                'porcentaje_promedio': float((total_ahorrado / total_metas * 100) if total_metas > 0 else 0)
            },
            'categorias_mas_usadas': list(
                Transaccion.objects.values('categoria__nombre')
                .annotate(total=Count('id'), monto_total=Sum('monto'))
                .order_by('-total')[:5]
            )
        })
