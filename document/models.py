import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator


# TUTANAK
class Minutes(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name='minutes', on_delete=models.CASCADE)
    no = models.IntegerField(default=1, verbose_name="Tutanak No")
    subject = models.CharField(max_length=50, verbose_name="Konu")
    note = models.TextField(max_length=1500, verbose_name="Notlar")
    date = models.DateField(verbose_name="Tutanak Tarihi")
    labor_cost = models.FloatField(default=0, verbose_name="Yevmiye Bedeli")
    material_cost = models.FloatField(default=0, verbose_name="Malzeme Bedeli")
    total_cost = models.FloatField(default=0, verbose_name="Toplam Bedel")
    file = models.FileField(verbose_name="Tutanak Seçiniz", help_text="İmzalı tutanağı PDF olarak yükleyiniz.")
    status = models.BooleanField(default=False, verbose_name="Onay")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Minutes'
        ordering = ['-id']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('document:minutes_update', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = slugify(str(self.worksite.firm).replace('ı','i'))+'/'+slugify(str(self.worksite).replace('ı','i'))+'/minutes/'+slugify(str(self.subject).replace('ı','i'))+os.path.splitext(self.file.name)[1]
        return super(Minutes, self).save(*args, **kwargs)



class Writing(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name='writings', on_delete=models.CASCADE)
    no = models.IntegerField(default=1, verbose_name="Üst Yazı No")
    subject = models.CharField(max_length=50, verbose_name="Üst Yazı Konu")
    note = models.TextField(max_length=2000, verbose_name="Üst Yazı Notları")
    date = models.DateField(verbose_name="Üst Yazı Tarihi")
    file = models.FileField(verbose_name="Üst Yazı Seçiniz", help_text="İmzalı üst yazıyı PDF olarak yükleyiniz.")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Writing'
        ordering = ['-id']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('document:writing_update', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = slugify(str(self.worksite.firm).replace('ı','i'))+'/'+slugify(str(self.worksite).replace('ı','i'))+'/writing/'+slugify(str(self.subject).replace('ı','i'))+os.path.splitext(self.file.name)[1]
        return super(Writing, self).save(*args, **kwargs)


class DailyReport(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('firm.Worksite', verbose_name='Şantiye', related_name='daily_reports', on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Tarih")
    works = models.CharField(max_length=20, verbose_name="Çalışma Saatleri")
    hours = models.CharField(max_length=20, verbose_name="Mesai Saatleri")
    temperature = models.CharField(max_length=10, verbose_name="Sıcaklık")
    weather = models.CharField(max_length=20, verbose_name="Hava Durumu")
    wind = models.CharField(max_length=10, verbose_name="Rüzgar")
    production = models.CharField(max_length=500, verbose_name="İmalatlar") # diziler birleştirilecek
    direct = models.CharField(max_length=200, verbose_name="Direkt")
    direct_count = models.CharField(max_length=20, verbose_name="Direkt Mevcut")
    indirect = models.CharField(max_length=200, verbose_name="Endrekt")
    indirect_count = models.CharField(max_length=20, verbose_name="Endirekt Mevcut")
    note = models.CharField(max_length=500, blank=True, null=True, verbose_name="Not")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Daily_Report'
        ordering = ['-id']

    def __str__(self):
        return self.date
    
    def get_absolute_url(self):
        return reverse('document:daily_update', kwargs={'pk':self.pk})