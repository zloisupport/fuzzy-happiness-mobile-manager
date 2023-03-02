import datetime
import io

from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from common.view import TitleMixin
from products import models
from products.forms import PhoneAddForm, StockAddForm, SupplierAddForm, SupplierEditForm, ManufacturerAddForm
from products.models import PhoneModel, Stock, Supplier, Manufacturer

student_name = settings.STUDENT_NAME


def my_view(request):
    stock = {"quantity": 1}  # определение переменной stock.quantity
    return render(request, "products/base.html", {"stock": stock})


# ----------------Stock View--------------
class StockAddView(TitleMixin, CreateView):
    model = Stock
    form_class = StockAddForm
    template_name = "products/stock/add.html"


class StockView(TitleMixin, ListView):
    model = Stock
    template_name = "products/stock.html"

    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StockView, self).get_context_data()
        return context


# ----------------SupplierView View--------------
class SupplierView(TitleMixin, ListView):
    model = Supplier
    template_name = "products/supplier/list.html"

    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SupplierView, self).get_context_data()
        return context


class SupplierAddView(TitleMixin, CreateView):
    model = Supplier
    form_class = SupplierAddForm
    template_name = "products/supplier/add.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SupplierAddView, self).get_context_data()
        return context


class SupplierEditView(TitleMixin, UpdateView):
    model = Supplier
    form_class = SupplierEditForm
    template_name = "products/supplier/edit.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SupplierEditView, self).get_context_data()
        return context


class SupplierRemoveView(TitleMixin, DeleteView):
    model = Supplier
    template_name = "products/supplier/remove.html"
    success_url = reverse_lazy("products:supplier")


# ----------------Phone View--------------
class PhoneView(TitleMixin, ListView):
    model = PhoneModel
    template_name = "products/phone/list.html"

    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhoneView, self).get_context_data()
        context["total_quantity"] = Stock.objects.aggregate(Sum("quantity"))[
            "quantity__sum"
        ]
        return context


class PhoneAddView(TitleMixin, CreateView):
    model = PhoneModel
    form_class = PhoneAddForm
    template_name = "products/phone/add.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PhoneAddView, self).get_context_data()
        return context


# ----------------Manufacture View--------------
class ManufactureView(ListView):
    model = Manufacturer
    template_name = "products/other/list.html"
    # 
    paginate_by = 0
    fields = ['name']
    # def get_queryset(self):
    #     return super().get_queryset().all()
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ManufactureView, self).get_context_data()
    #     return context


class ManufacturerAddView(TitleMixin, CreateView):
    model = Manufacturer
    form_class = ManufacturerAddForm
    template_name = "products/other/manufacture/add.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerAddView, self).get_context_data()
        return context


# class ManufacturerRemoveView(TitleMixin, DeleteView):
#     model = Manufacturer
#     template_name = "products/other/list.html"
#     success_url = reverse_lazy('products:manufacture_list')

def ManufacturerRemoveView(request, pk):
    basket = Manufacturer.objects.get(id=pk)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


# ----------------Generate PDF View--------------
def gen_pdf(request):
    # https://gist.github.com/nngogol/6e19b97ce3f6e06b21a1add1a196ce3b
    # https://stackoverflow.com/questions/43345494/add-rows-in-a-table-using-reportlab-django
    # response = HttpResponse(content_type='application/pdf')
    # current_datetime = datetime.datetime.now().strftime('%D %H:%M:%S')
    # response['Content-Disposition'] = f'attachment; filename="Supplier{current_datetime}.pdf"'
    # width, height = A4
    # styles = getSampleStyleSheet()
    # pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf', 'UTF-8'))
    # styles['Normal'].fontName = 'DejaVuSerif'
    # styles['Heading1'].fontName = 'DejaVuSerif'
    # styleN = styles["BodyText"]
    # styleN.alignment = TA_LEFT
    # styleBH = styles["Normal"]
    # styleBH.alignment = TA_CENTER
    #
    # def coord(x, y, unit=1):
    #     x, y = x * unit, height - y * unit
    #     return x, y
    #
    # inspection = Paragraph('''<b>№</b>''', styleBH)
    # licplt = Paragraph('''<b>Название</b>''', styleBH)
    # imgs = Paragraph('''<b>Адрес</b>''', styleBH)
    # cmnts = Paragraph('''<b>Телефон</b>''', styleBH)
    #
    # buffer = io.BytesIO()
    # p = canvas.Canvas(buffer, pagesize=A4)
    # p.setTitle("Supplier")
    # p.drawString(20, 800,""+str(current_datetime))
    #
    #
    # damage_data = Supplier.objects.all()
    #
    # # Fill the first row of `data` with the heading, only once!
    # data = [[inspection, licplt, imgs, cmnts]]
    #
    # for num, value in enumerate(damage_data):
    #     name = Paragraph(f'''{value.name}''', styleBH)
    #     address = Paragraph(f'''{value.address}''', styleBH)
    #     phone = Paragraph(f'''{value.phone}''', styleBH)
    #     data.append([num, name, address, phone])
    #
    # table = Table(data, colWidths=[4 * cm, 4 * cm, 5 * cm, 4 * cm])
    #
    # table.setStyle(TableStyle([
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    # ]))
    # # table.wrapOn(p, width, height)
    # # table.wrapOn(p, width, height)
    # # table.drawOn(p, *coord(1.8, 9.6, cm))
    # p.showPage()
    # p.save()
    # pdf = buffer.getvalue()
    # buffer.close()
    # response.write(pdf)
    # return response

    #     ============================================================
    response = HttpResponse(content_type="application/pdf")
    current_date_time = datetime.datetime.now().strftime("%D %H:%M:%S")
    pdf_name = "supplier-%s.pdf" % str(current_date_time)
    response["Content-Disposition"] = "attachment; filename=%s" % pdf_name
    pdfmetrics.registerFont(TTFont("DejaVuSerif", "DejaVuSerif.ttf", "UTF-8"))

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "DejaVuSerif"
    styles["Heading1"].fontName = "DejaVuSerif"
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    buff = io.BytesIO()
    p = canvas.Canvas(buff, pagesize=A4)
    p.drawString(20, 800, "wwwwwwwwww")
    menu_pdf = SimpleDocTemplate(
        buff,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
        title="Supplier",
    )

    inspection = Paragraph("""<b>№</b>""", styleBH)
    licplt = Paragraph("""<b>Название</b>""", styleBH)
    imgs = Paragraph("""<b>Адрес</b>""", styleBH)
    cmnts = Paragraph("""<b>Телефон</b>""", styleBH)
    # container for pdf elements

    elements = [(Paragraph("Поставщики", styles["Normal"]))]
    data = [[inspection, licplt, imgs, cmnts]]
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="centered", alignment=TA_CENTER))

    damage_data = Supplier.objects.all()
    # damage_data =[]
    for num, value in enumerate(damage_data):
        num += 1
        name = Paragraph(f"""{value.name}""", styleBH)
        address = Paragraph(f"""{value.address}""", styleBH)
        phone = Paragraph(f"""{value.phone}""", styleBH)
        data.append([num, name, address, phone])

    t2 = Table(data, colWidths=[1 * cm, 4 * cm, 5 * cm, 4 * cm])

    t2.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 1), (-2, -2), "RIGHT"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    t2.wrapOn(p, 200, 200)
    p.showPage()
    p.save()
    elements.append(t2)

    menu_pdf.build(elements)
    response.write(buff.getvalue())
    buff.close()
    return response


def gen_stock_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    current_date_time = datetime.datetime.now().strftime("%D %H:%M:%S")
    pdf_name = "stock-%s.pdf" % str(current_date_time)
    response["Content-Disposition"] = "attachment; filename=%s" % pdf_name
    pdfmetrics.registerFont(TTFont("DejaVuSerif", "DejaVuSerif.ttf", "UTF-8"))

    styles = getSampleStyleSheet()
    styles["Normal"].fontName = "DejaVuSerif"
    styles["Heading1"].fontName = "DejaVuSerif"
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER
    buff = io.BytesIO()
    p = canvas.Canvas(buff, landscape(letter))

    p.drawString(20, 800, "wwwwwwwwww")
    menu_pdf = SimpleDocTemplate(
        buff,
        rightMargin=10,
        leftMargin=10,
        topMargin=10,
        bottomMargin=18,
        title="Supplier",
        pagesize=landscape(landscape(letter))
    )

    title_enum = Paragraph("""<b>№</b>""", styleBH)
    title_supplier = Paragraph("""<b>Поставщик</b>""", styleBH)
    title_quantity = Paragraph("""<b>Количество</b>""", styleBH)
    title_name = Paragraph("""<b>Название</b>""", styleBH)
    title_price = Paragraph("""<b>Стоимость </b>""", styleBH)
    title_group_price = Paragraph("""<b>Стоимость *</b>""", styleBH)
    title_color = Paragraph("""<b>Цвет</b>""", styleBH)
    title_ram = Paragraph("""<b>RAM</b>""", styleBH)
    title_rom = Paragraph("""<b>ROM</b>""", styleBH)
    title_front_cam = Paragraph("""<b>Фронт Камера</b>""", styleBH)
    title_back_cam = Paragraph("""<b>Осн Камера</b>""", styleBH)
    # container for pdf elements
    all_quanity = Stock.objects.aggregate(Sum("quantity"))[
        "quantity__sum"
    ]

    elements = [Paragraph("---------------------------------------", styles["Normal"])]
    elements.append((Paragraph("Cклад", styles["Normal"])))

    elements.append(Paragraph("---------------------------------------", styles["Normal"]))
    data = [[title_enum, title_supplier, title_quantity, title_name, title_color, title_ram, title_rom,
             title_front_cam, title_back_cam, title_price,
             title_group_price]]
    total_price = 0
    damage_data = Stock.objects.all()
    # damage_data =[]
    for _num, value in enumerate(damage_data):
        _num += 1
        _name = Paragraph(f"""{value.supplier}""", styleBH)
        _quantity = Paragraph(f"""{value.quantity}""", styleBH)
        _phone = Paragraph(f"""{value.phone_model}""", styleBH)
        _price = Paragraph(f"""{value.phone_model.price}""", styleBH)
        _color = Paragraph(f"""{value.color}""", styleBH)
        _ram = Paragraph(f"""{value.phone_model.ram}""", styleBH)
        _rom = Paragraph(f"""{value.phone_model.rom}""", styleBH)
        _front_cam = Paragraph(f"""{value.phone_model.front_camera}""", styleBH)
        _gen_cam = Paragraph(f"""{value.phone_model.camera}""", styleBH)
        _group_price = Paragraph(f"""{value.phone_model.price * value.quantity}""", styleBH)
        total_price += value.phone_model.price * value.quantity
        data.append([_num, _name, _quantity, _phone, _color, _ram, _rom, _gen_cam, _front_cam, _price, _group_price])
    data.append(
        ["*", (Paragraph("Всего", styles["Normal"])), str(all_quanity), "", "", "", "", "", "", "", total_price])

    t2 = Table(data, colWidths=[1 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 2 * cm, 3 * cm])

    t2.setStyle(
        TableStyle(
            [
                ("ALIGN", (1, 1), (-2, -2), "RIGHT"),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    t2.wrapOn(p, 200, 200)
    p.showPage()
    p.save()
    elements.append(t2)
    # elements.append(Paragraph("Общая стоимость товара " + str(total_price), styles["Normal"]))
    menu_pdf.build(elements)
    response.write(buff.getvalue())
    buff.close()
    return response
