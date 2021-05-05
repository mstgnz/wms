import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# KEŞİF
class Discovery(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name="discoveries", on_delete=models.CASCADE)
    no = models.CharField(max_length=50, verbose_name="Poz No")
    name = models.CharField(max_length=500, verbose_name="Poz Adı")
    unit = models.CharField(max_length=5, verbose_name="Birim")
    amount = models.FloatField(default=0, verbose_name="Miktar")
    price = models.FloatField(default=0, verbose_name="Birim Fiyat")
    total = models.FloatField(default=0, verbose_name="Keşif Tutar")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Discovery'
        ordering = ['-id']

    def __str__(self):
        return self.name



# ANALİZ
class Analysis(models.Model):
    id = models.AutoField(primary_key=True)
    discovery = models.ForeignKey('Discovery', verbose_name='Keşif', related_name="analysis", on_delete=models.CASCADE)
    detail = models.TextField(max_length=2500, blank=True, null=True, verbose_name='Poz Detayı')
    profit = models.FloatField(default=0, verbose_name="Müteahhitlik Kârı")
    material = models.FloatField(default=0, verbose_name="Malzeme Toplam")
    workmanship = models.FloatField(default=0, verbose_name="İşçilik Toplam")
    overheads = models.FloatField(default=0, verbose_name="Genel Gider Toplam")
    tender = models.FloatField(default=0, verbose_name="Teklif Fiyatı")
    year = models.CharField(max_length=4, default=2019, verbose_name="Rayiç Yılı")
    note = models.TextField(max_length=1500, blank=True, null=True, verbose_name='Notlar')
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Analysis'
        ordering = ['-id']

    def __str__(self):
        return self.detail



# ANALİZ DETAY
class AnalysisDetail(models.Model):
    id = models.AutoField(primary_key=True)
    analysis = models.ForeignKey('Analysis', verbose_name='Analiz', related_name="analysis_detail", on_delete=models.CASCADE)
    category = models.CharField(max_length=15, verbose_name="Kategori")
    definition = models.CharField(max_length=100, verbose_name='Tanım')
    amount = models.FloatField(default=0, verbose_name="Miktar")
    price = models.FloatField(default=0, verbose_name="Birim Fiyat")
    total = models.FloatField(default=0, verbose_name="Tutar")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Analysis_Detail'
        ordering = ['-id']

    def __str__(self):
        return self.definition


# HAKEDİŞ
class Progress(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name="progress", on_delete=models.CASCADE)
    subcontractor = models.ForeignKey('firm.Subcontractor', blank=True, null=True, verbose_name='Taşeron', related_name="progress", on_delete=models.CASCADE)
    employer = models.CharField(max_length=30, verbose_name='İşveren')
    no = models.PositiveSmallIntegerField(verbose_name="Hakediş No")
    date = models.DateField(verbose_name="Hakediş Tarihi")
    cumulative = models.FloatField(default=0, verbose_name="Toplam İmalat Tutarı")
    acquisition = models.FloatField(default=0, verbose_name="İhzarat Tutar")
    additional = models.FloatField(default=0, verbose_name="İlave İşler Tutarı")
    total = models.FloatField(default=0, verbose_name="Toplam Hakediş Tutarı")
    previous_amount = models.FloatField(default=0, verbose_name="Önceki Hakediş Tutarı")
    this_amount = models.FloatField(default=0, verbose_name="Bu Hakediş Tutarı")
    vat = models.FloatField(default=0, verbose_name="KDV %18")
    progress_amount = models.FloatField(default=0, verbose_name="Net Hakediş Tutarı")
    total_warrant = models.FloatField(default=0, verbose_name="Toplam Teminat Kesintisi")
    previous_warrant = models.FloatField(default=0, verbose_name="Önceki Teminat Kesintisi")
    this_warrant = models.FloatField(default=0, verbose_name="Bu Teminat Kesintisi")
    total_advance = models.FloatField(default=0, verbose_name="Toplam Avans Kesintisi")
    previous_advance = models.FloatField(default=0, verbose_name="Önceki Avans Kesintisi")
    this_advance = models.FloatField(default=0, verbose_name="Bu Avans Kesintisi")
    total_stoppage = models.FloatField(default=0, verbose_name="Toplam Stopaj Kesintisi")
    previous_stoppage = models.FloatField(default=0, verbose_name="Önceki Stopaj Kesintisi")
    this_stoppage = models.FloatField(default=0, verbose_name="Bu Stopaj Kesintisi")
    total_tax_cut = models.FloatField(default=0, verbose_name="Toplam KDV Tevkifatı")
    previous_tax_cut = models.FloatField(default=0, verbose_name="Önceki KDV Tevkifatı")
    this_tax_cut = models.FloatField(default=0, verbose_name="Bu KDV Tevkifatı")
    total_penalty = models.FloatField(default=0, verbose_name="Toplam Ceza Kesintisi")
    previous_penalty = models.FloatField(default=0, verbose_name="Önceki Ceza Kesintisi")
    this_penalty = models.FloatField(default=0, verbose_name="Bu Ceza Kesintisi")
    total_deduction = models.FloatField(default=0, verbose_name="Toplam Diğer Kesintiler")
    previous_deduction = models.FloatField(default=0, verbose_name="Önceki Diğer Kesintiler")
    this_deduction = models.FloatField(default=0, verbose_name="Bu Diğer Kesintiler")
    amount_paid = models.FloatField(default=0, verbose_name="Ödenecek Tutar")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Progress'
        ordering = ['-id']

    def __str__(self):
        return str(self.no)


# HAKEDİŞ İCMAL
class Synopsis(models.Model):
    id = models.AutoField(primary_key=True)
    progress = models.ForeignKey('Progress', verbose_name='Hakediş', related_name="synopsis", on_delete=models.CASCADE)
    pose_no = models.CharField(max_length=10, verbose_name="Poz No")
    name = models.CharField(max_length=50, verbose_name="Poz Adı")
    unit = models.CharField(max_length=10, verbose_name="Birim")
    unit_price = models.FloatField(default=0, verbose_name="Birim Fiyat")
    total_quantity = models.FloatField(default=0, verbose_name="Toplam Miktar")
    previous_quantity = models.FloatField(default=0, verbose_name="Önceki Dönem Miktar")
    this_quantity = models.FloatField(default=0, verbose_name="Bu Dönem Miktar")
    total_price = models.FloatField(default=0, verbose_name="Toplam Tutar")
    previous_price = models.FloatField(default=0, verbose_name="Önceki Dönem Tutar")
    this_price = models.FloatField(default=0, verbose_name="Bu Dönem Tutar")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Synopsis'
        ordering = ['-id']
    
    def __str__(self):
        return self.name