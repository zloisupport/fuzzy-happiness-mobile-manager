from django.db import models
from django.urls import reverse_lazy



class Manufacturer(models.Model):
    """Производитель товара"""

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("products:manufacture_list")


class OperatingSystem(models.Model):
    """Операционая система товара"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PhoneModel(models.Model):
    """Телефон"""

    manufacturer = models.ForeignKey(
        Manufacturer, blank=True, null=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    os = models.ForeignKey(
        OperatingSystem, blank=True, null=True, on_delete=models.CASCADE
    )
    ram = models.PositiveIntegerField(max_length=5, blank=True, default=0, null=True)
    rom = models.PositiveIntegerField(max_length=5, blank=True, default=0, null=True)
    camera = models.PositiveIntegerField(max_length=5, blank=True, default=0, null=True)
    front_camera = models.PositiveIntegerField(max_length=5, blank=True, default=0, null=True)
    image = models.ImageField(upload_to="product_images", blank=True, null=True)
    status = models.TextField(max_length=5, blank=True, default="New", null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def get_stock_quantity(self):
        return sum(stock.quantity for stock in self.stock_set.all())

    @property
    def stock_quantity(self):
        return self.get_stock_quantity()

    def get_absolute_url(self):
        return reverse_lazy("products:phone_list")


class Supplier(models.Model):
    """Поставщик товара"""

    name = models.CharField(max_length=100, verbose_name="Поставщик")
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("products:supplier")


class Stock(models.Model):
    """Склад"""

    phone_model = models.ForeignKey(PhoneModel, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.phone_model} - {self.color} - {self.quantity}"

    def get_absolute_url(self):
        return reverse_lazy("products:stock")


class Sale(models.Model):
    """Скидки"""

    phone_model = models.ForeignKey(PhoneModel, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.phone_model} - {self.quantity} - {self.price}"
