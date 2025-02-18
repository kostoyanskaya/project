from decimal import Decimal

from django.db import models


class Order(models.Model):
    """
    Модель заказа в кафе.
    """

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Список блюд", default=list)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name="Общая стоимость"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус заказа",
    )

    def save(self, *args, **kwargs):
        """
        Переопределяем метод save() для автоматического
        расчета общей стоимости заказа.
        """
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self) -> Decimal:
        """
        Вычисляет общую стоимость заказа на основе списка блюд.
        """
        return sum(Decimal(item['price']) for item in self.items)

    def __str__(self) -> str:
        """
        Возвращает строковое представление заказа для удобства отладки.
        """
        return f"Заказ №{self.id} - Стол {self.table_number}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
