import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
import datetime
import calendar


# İRSALİYE
class Waybill(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name='waybills', on_delete=models.CASCADE)
    vendor = models.CharField(max_length=50, verbose_name="Satıcı Firma")
    waybill_no = models.CharField(max_length=15, verbose_name="İrsaliye No")
    date_of_issue = models.DateField(verbose_name="Düzenlenme Tarihi")
    date_of_shipment = models.DateField(verbose_name="Fiili Sevk Tarihi")
    invoice_no = models.CharField(max_length=15, blank=True, verbose_name="Fatura No")
    consigner = models.CharField(max_length=15, verbose_name="Teslim Eden")
    recipient = models.CharField(max_length=15, verbose_name="Teslim Alan")
    note = models.CharField(max_length=1000, blank=True, null=True, verbose_name="İrsaliye Notları")
    file = models.FileField(verbose_name="İrsaliye Seçiniz", help_text="İrsaliyeyi PDF olarak yükleyiniz.")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Waybill'
        ordering = ['-id']

    def __str__(self):
        return self.vendor

    def get_absolute_url(self):
        return reverse('accounting:waybill_update', kwargs={'pk':self.pk})
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file.vendor = slugify(str(self.worksite.firm).replace('ı','i'))+'/'+slugify(str(self.worksite).replace('ı','i'))+'/waybill/'+slugify(str(self.vendor).replace('ı','i'))+os.path.splitext(self.file.name)[1]
        return super(Waybill, self).save(*args, **kwargs)



# İRSALİYE MALZEME LİSTESİ
class WaybillMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    waybill = models.ForeignKey('Waybill', verbose_name='İrsaliye', related_name="waybill_materials", on_delete=models.CASCADE)
    name = models.CharField(max_length=40, verbose_name='Malzeme Adı')
    unit = models.CharField(max_length=10, verbose_name="Birim")
    amount = models.FloatField(default=0, verbose_name="Miktar")
    price = models.FloatField(default=0, verbose_name="Birim Fiyat")
    total = models.FloatField(default=0, verbose_name="Tutar")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Waybill_Material'
        ordering = ['-id']

    def __str__(self):
        return self.name


# İŞÇİ
class Worker(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name='workers', on_delete=models.CASCADE)
    subcontractor = models.ForeignKey('firm.Subcontractor', verbose_name="Taşeron", related_name="workers", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=30, verbose_name="Ad Soyad")
    title = models.CharField(max_length=15, verbose_name="Ünvan")
    phone = models.CharField(max_length=10, verbose_name="Telefon", validators=[RegexValidator(r'^\d{10}$')])
    input_date = models.DateField(verbose_name="Giriş Tarihi")
    output_date = models.DateField(verbose_name="Çıkış Tarihi", blank=True, null=True)
    id_number = models.CharField(unique=True, max_length=11, verbose_name="Kimlik Numarası", validators=[RegexValidator(r'^\d{11}$')])
    mother_name = models.CharField(max_length=30, verbose_name="Anne Adı", blank=True, null=True)
    father_name = models.CharField(max_length=30, verbose_name="Baba Adı", blank=True, null=True)
    place_of_birth = models.CharField(max_length=20, verbose_name="Doğum Yeri", blank=True, null=True)
    birth_date = models.DateField(verbose_name="Doğum Tarihi", blank=True, null=True)
    marital_status = models.CharField(max_length=5, verbose_name="Medeni Hali", blank=True, null=True)
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Worker'
        ordering = ['-id']
    
    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('accounting:worker_update', kwargs={'pk':self.pk})


# PUANTAJ
def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Tally(models.Model):
    YEAR_CHOICES = [(i,i) for i in range(2017, datetime.date.today().year+1)]
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    id = models.AutoField(primary_key=True)
    worker = models.ForeignKey('Worker', verbose_name='Personel', related_name='tally', on_delete=models.CASCADE)
    year = models.CharField(max_length=4, choices=YEAR_CHOICES, default=current_year, verbose_name="Yıl")
    month = models.CharField(max_length=9, choices=MONTH_CHOICES, default='1', verbose_name="Ay")
    wage = models.FloatField(verbose_name="Toplam Yevmiye")
    permit = models.FloatField(verbose_name="Toplam İzin")
    overtime = models.FloatField(verbose_name="Toplam Mesai")
    sunday = models.FloatField(verbose_name="Toplam Pazar")
    notch = models.CharField(max_length=250, blank=True, null=True, verbose_name="İşlem")
    shift = models.CharField(max_length=250, blank=True, null=True, verbose_name="Mesai")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Tally'
        ordering = ['-id']
    
    def __str__(self):
        return self.worker

    def get_absolute_url(self):
        return reverse('accounting:worker_tally_update', kwargs={'pk':self.pk})


# SİPARİŞ
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name='orders', on_delete=models.CASCADE)
    orderer = models.CharField(max_length=20, verbose_name="Sipariş Veren")
    deadline = models.DateField(verbose_name="Termin Tarihi")
    note = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Sipariş Notları")
    status = models.BooleanField(default=False, verbose_name="Durum")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Order'
        ordering = ['-id']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('accounting:order_update', kwargs={'pk':self.pk})


# SİPARİŞ MALZEME LİSTESİ
class OrderMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Order', verbose_name='Sipariş', related_name="order_materials", on_delete=models.CASCADE)
    name = models.CharField(max_length=40, verbose_name='Malzeme Adı')
    unit = models.CharField(max_length=10, verbose_name="Birim")
    amount = models.FloatField(default=0, verbose_name="Miktar")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Order_Material'
        ordering = ['-id']

    def __str__(self):
        return self.name