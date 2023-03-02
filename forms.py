from django import forms
from django.utils.translation import gettext_lazy as _

from products.models import Manufacturer, OperatingSystem, PhoneModel, Stock, Supplier


class StockAddForm(forms.ModelForm):
    phone_model = forms.ModelChoiceField(
        label="Телефон",
        queryset=PhoneModel.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    color = forms.CharField(
        label="Цвет", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    quantity = forms.CharField(
        label="Количество", widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    supplier = forms.ModelChoiceField(
        label="Поставщик",
        queryset=Supplier.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Stock
        fields = ("phone_model", "color", "quantity", "supplier")
        labels = {
            "phone_model": _("phone_model"),
        }



class PhoneAddForm(forms.ModelForm):
    manufacturer = forms.ModelChoiceField(
        label="Производитель",
        queryset=Manufacturer.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    name = forms.CharField(
        label="Название",
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-4",
                "placeholder": "Название",
            }
        ),
    )
    os = forms.ModelChoiceField(
        label="Операционная система",
        queryset=OperatingSystem.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control py-4", "placeholder": "Операционная система"}
        ),
    )

    rom = forms.CharField(
        label="Память устройства",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "32 ГБ"}
        ),
    )
    ram = forms.CharField(
        label="Оперативная память",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "2ГБ"}
        ),
    )
    camera = forms.CharField(
        label="Основная камера",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "12 Мп"}
        ),
    )

    front_camera = forms.CharField(
        label="Основная камера",
        widget=forms.TextInput(
            attrs={"class": "form-control py-4", "placeholder": "5 Мп"}
        ),
    )
    price = forms.CharField(
        label="Цена",
        widget=forms.NumberInput(
            attrs={"class": "form-control py-4", "placeholder": "Цена"}
        ),
    )

    class Meta:
        model = PhoneModel
        fields = ("manufacturer", "name", "rom", "ram", "os", "camera", "front_camera", "price")


class ManufacturerAddForm(forms.ModelForm):
    name = forms.CharField(
        label="Название", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    country = forms.CharField(
        label="Страна", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Manufacturer
        fields = ("name", "country")
