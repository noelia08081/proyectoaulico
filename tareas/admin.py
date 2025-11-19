from django.contrib import admin
from .models import Categoria, Presupuesto, Transaccion, MetaFinanciera, LeccionEducativa


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'icono', 'fecha_creacion']
    list_filter = ['tipo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'monto_limite', 'mes', 'año', 'porcentaje_usado']
    list_filter = ['año', 'mes', 'categoria']
    search_fields = ['nombre', 'categoria__nombre']
    date_hierarchy = 'fecha_creacion'


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'monto', 'tipo', 'categoria', 'fecha']
    list_filter = ['tipo', 'categoria', 'fecha']
    search_fields = ['descripcion', 'notas']
    date_hierarchy = 'fecha'


@admin.register(MetaFinanciera)
class MetaFinancieraAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'monto_objetivo', 'monto_actual', 'porcentaje_completado', 'estado', 'fecha_objetivo']
    list_filter = ['estado', 'fecha_objetivo', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    date_hierarchy = 'fecha_creacion'


@admin.register(LeccionEducativa)
class LeccionEducativaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nivel', 'duracion_minutos', 'orden', 'activa']
    list_filter = ['nivel', 'activa', 'fecha_creacion']
    search_fields = ['titulo', 'contenido']
    ordering = ['orden', 'fecha_creacion']

