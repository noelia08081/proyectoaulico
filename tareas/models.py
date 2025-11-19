from django.db import models
from django.utils import timezone
from decimal import Decimal


class Categoria(models.Model):
    """Categorías para clasificar transacciones financieras"""
    
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo'
    )
    icono = models.CharField(max_length=50, default='💰', verbose_name='Icono')
    color = models.CharField(max_length=20, default='#3498db', verbose_name='Color')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['tipo', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Presupuesto(models.Model):
    """Presupuesto mensual para categorías de gastos"""
    
    nombre = models.CharField(max_length=200, verbose_name='Nombre del Presupuesto')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo': 'gasto'},
        verbose_name='Categoría'
    )
    monto_limite = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Monto Límite'
    )
    mes = models.IntegerField(verbose_name='Mes')
    año = models.IntegerField(verbose_name='Año')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-año', '-mes', 'categoria']
        unique_together = ['categoria', 'mes', 'año']
    
    def __str__(self):
        return f"{self.nombre} - {self.mes}/{self.año}"
    
    @property
    def gasto_actual(self):
        """Calcula el gasto actual en esta categoría para el mes/año"""
        from django.db.models import Sum
        total = self.categoria.transaccion_set.filter(
            tipo='gasto',
            fecha__year=self.año,
            fecha__month=self.mes
        ).aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')
        return total
    
    @property
    def porcentaje_usado(self):
        """Calcula el porcentaje del presupuesto usado"""
        if self.monto_limite > 0:
            return round((self.gasto_actual / self.monto_limite) * 100, 2)
        return 0
    
    @property
    def monto_restante(self):
        """Calcula el monto restante del presupuesto"""
        return max(Decimal('0.00'), self.monto_limite - self.gasto_actual)


class Transaccion(models.Model):
    """Transacciones financieras (ingresos y gastos)"""
    
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('gasto', 'Gasto'),
    ]
    
    descripcion = models.CharField(max_length=200, verbose_name='Descripción')
    monto = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Monto')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, verbose_name='Categoría')
    fecha = models.DateField(verbose_name='Fecha', default=timezone.now)
    notas = models.TextField(blank=True, verbose_name='Notas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-fecha', '-fecha_creacion']
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.descripcion} - {self.monto}"


class MetaFinanciera(models.Model):
    """Metas financieras a largo plazo"""
    
    ESTADO_CHOICES = [
        ('en_progreso', 'En Progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    monto_objetivo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Monto Objetivo'
    )
    monto_actual = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Monto Actual'
    )
    fecha_objetivo = models.DateField(verbose_name='Fecha Objetivo')
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='en_progreso',
        verbose_name='Estado'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Meta Financiera'
        verbose_name_plural = 'Metas Financieras'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    @property
    def porcentaje_completado(self):
        """Calcula el porcentaje completado de la meta"""
        if self.monto_objetivo > 0:
            return min(100, round((self.monto_actual / self.monto_objetivo) * 100, 2))
        return 0
    
    @property
    def monto_restante(self):
        """Calcula el monto restante para alcanzar la meta"""
        return max(Decimal('0.00'), self.monto_objetivo - self.monto_actual)
    
    @property
    def dias_restantes(self):
        """Calcula los días restantes para alcanzar la meta"""
        if self.fecha_objetivo:
            delta = self.fecha_objetivo - timezone.now().date()
            return max(0, delta.days)
        return None


class LeccionEducativa(models.Model):
    """Contenido educativo sobre finanzas personales"""
    
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name='Título')
    contenido = models.TextField(verbose_name='Contenido')
    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='basico',
        verbose_name='Nivel'
    )
    duracion_minutos = models.IntegerField(default=5, verbose_name='Duración (minutos)')
    orden = models.IntegerField(default=0, verbose_name='Orden')
    activa = models.BooleanField(default=True, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Lección Educativa'
        verbose_name_plural = 'Lecciones Educativas'
        ordering = ['orden', 'fecha_creacion']
    
    def __str__(self):
        return self.titulo

