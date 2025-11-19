from rest_framework import serializers
from .models import Categoria, Presupuesto, Transaccion, MetaFinanciera, LeccionEducativa


class CategoriaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Categoria"""
    
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'tipo', 'icono', 'color', 'fecha_creacion']


class PresupuestoSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Presupuesto"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    gasto_actual = serializers.ReadOnlyField()
    porcentaje_usado = serializers.ReadOnlyField()
    monto_restante = serializers.ReadOnlyField()
    
    class Meta:
        model = Presupuesto
        fields = [
            'id', 'nombre', 'categoria', 'categoria_nombre',
            'monto_limite', 'mes', 'año',
            'gasto_actual', 'porcentaje_usado', 'monto_restante',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class TransaccionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Transaccion"""
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    categoria_icono = serializers.CharField(source='categoria.icono', read_only=True)
    
    class Meta:
        model = Transaccion
        fields = [
            'id', 'descripcion', 'monto', 'tipo', 'categoria',
            'categoria_nombre', 'categoria_icono',
            'fecha', 'notas', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class MetaFinancieraSerializer(serializers.ModelSerializer):
    """Serializador para el modelo MetaFinanciera"""
    porcentaje_completado = serializers.ReadOnlyField()
    monto_restante = serializers.ReadOnlyField()
    dias_restantes = serializers.ReadOnlyField()
    
    class Meta:
        model = MetaFinanciera
        fields = [
            'id', 'titulo', 'descripcion', 'monto_objetivo', 'monto_actual',
            'fecha_objetivo', 'estado',
            'porcentaje_completado', 'monto_restante', 'dias_restantes',
            'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_actualizacion']


class LeccionEducativaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo LeccionEducativa"""
    
    class Meta:
        model = LeccionEducativa
        fields = [
            'id', 'titulo', 'contenido', 'nivel',
            'duracion_minutos', 'orden', 'activa', 'fecha_creacion'
        ]
        read_only_fields = ['fecha_creacion']
