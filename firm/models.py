import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import RegexValidator


# FİRMA
class Firm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50, verbose_name="Firma Adı")
    slug = models.SlugField(unique=True, editable=False, max_length=50)
    full_name = models.CharField(max_length=255, verbose_name="Firma Tam Adı")
    tax = models.CharField(unique=True, max_length=10, verbose_name="Vergi Numarası", validators=[RegexValidator(r'^\d{10}$')])
    phone = models.CharField(max_length=10, verbose_name="Telefon", validators=[RegexValidator(r'^\d{10}$')])
    fax = models.CharField(max_length=10, verbose_name="Fax", validators=[RegexValidator(r'^\d{10}$')])
    web = models.URLField(max_length=50, verbose_name="Web")
    email = models.EmailField(max_length=50, verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Firma Adresi")
    image = models.ImageField(blank=True, null=True, verbose_name='Resim')
    active = models.BooleanField(default=True) # aktif
    firm = models.BooleanField(default=False) # firma
    subcontractor = models.BooleanField(default=False) # taşeron
    supply = models.BooleanField(default=False) # tedarikçi
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Firm'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('firm:firm_update', kwargs={'slug':self.slug})

    def get_image_or_default(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/site/img/firm.png'

    def get_unique_slug(self):
        slug = slugify(self.name.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Firm.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
            os.mkdir(settings.BASE_DIR+settings.MEDIA_URL+self.slug)
        if self.image:
            self.image.name = self.slug+'/'+self.slug+os.path.splitext(self.image.name)[1]
        return super(Firm, self).save(*args, **kwargs)


# ŞANTİYE
class Worksite(models.Model):
    id = models.AutoField(primary_key=True)
    firm = models.ForeignKey('Firm', verbose_name='Firma', related_name="worksites", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50, verbose_name="Şantiye Adı")
    slug = models.SlugField(unique=True, editable=False, max_length=50)
    employer = models.CharField(max_length=50, verbose_name="İşveren")
    name_of_job = models.CharField(max_length=100, verbose_name="İşin Adı")
    control = models.CharField(max_length=50, verbose_name="Kontrol")
    construction_area = models.IntegerField(verbose_name="İnşaat Alanı")
    threader_no = models.CharField(max_length=20, verbose_name="Pafta No")
    island_no = models.CharField(max_length=20, verbose_name="Ada No")
    parcel_no = models.CharField(max_length=20, verbose_name="Parsel No")
    phone = models.CharField(max_length=10, blank=True, null=True, verbose_name="Telefon", validators=[RegexValidator(r'^\d{10}$')])
    fax = models.CharField(max_length=10, blank=True, null=True, verbose_name="Fax", validators=[RegexValidator(r'^\d{10}$')])
    address = models.CharField(max_length=100, verbose_name="Şantiye Adresi")
    image = models.ImageField(blank=True, null=True, verbose_name='Resim')
    start_date = models.DateField(verbose_name="Başlangıç Tarihi")
    end_date = models.DateField(verbose_name="Bitiş Tarihi")
    create_date = models.DateField(auto_now_add=True, editable=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Worksite'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('firm:worksite_update', kwargs={'slug':self.slug})

    def get_image_or_default(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/site/img/worksite.png'

    def get_unique_slug(self):
        slug = slugify(self.name.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Worksite.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, counter)
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
            os.mkdir(settings.BASE_DIR+settings.MEDIA_URL+slugify(str(self.firm).replace('ı','i'))+'/'+self.slug)
        if self.image:
            self.image.name = slugify(str(self.firm).replace('ı','i'))+'/'+self.slug+os.path.splitext(self.image.name)[1]
        return super(Worksite, self).save(*args, **kwargs)


# TAŞERON
class Subcontractor(models.Model):
    id = models.AutoField(primary_key=True)
    firm = models.ForeignKey('Firm', verbose_name='Firma', related_name="subcontractors", on_delete=models.CASCADE)
    worksite = models.ManyToManyField('Worksite', related_name="subcontractors", verbose_name='Şantiye')
    # Taşeron bir firma ise ve ilerde bu sistemi kullanırsa vergi no ile eşlerek şantiyesine eklenecektir.
    tax = models.CharField(max_length=10, verbose_name="Vergi Numarası", blank=True, null=True,validators=[RegexValidator(r'^\d{10}$')], help_text="Eklenen taşeron bir firma ise vergi numarası girilmelidir.")
    name = models.CharField(max_length=50, unique=True, verbose_name="Taşeron Adı")
    email = models.EmailField(max_length=50, verbose_name="Email")
    phone = models.CharField(max_length=10, verbose_name="Telefon", validators=[RegexValidator(r'^\d{10}$')])
    subject = models.CharField(max_length=50, verbose_name="İşin Konusu")
    address = models.CharField(max_length=100, verbose_name="Taşeron Adresi")

    class Meta:
        db_table = 'Subcontractor'
        ordering = ['-id']

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('firm:subcontractor_update', kwargs={'pk':self.pk})

    def get_image_or_default(self):
        return '/static/site/img/subcontractor.png'


# SÖZLEŞME
class Contract(models.Model):
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('Worksite', verbose_name='Şantiye', related_name="contracts", on_delete=models.CASCADE)
    subcontractor = models.ForeignKey('Subcontractor', blank=True, null=True, verbose_name='Taşeron', related_name="subcontractors", on_delete=models.CASCADE)
    no = models.CharField(max_length=10, verbose_name="Sözleşme No")
    name = models.CharField(max_length=50, verbose_name="Sözleşme Adı")
    date = models.DateField(verbose_name="Sözleşme Tarihi")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Sözleşme Bedeli")
    guarantee = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name="Teminat Bedeli")
    advance = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name="Avans Bedeli")
    progress = models.CharField(max_length=2, verbose_name="Hakediş Günü")
    note = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Sözleşme Notları")
    file = models.FileField(verbose_name='Sözleşme', help_text="İmzalı sözleşmeyi PDF olarak yükleyiniz.")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Contract'
        ordering = ['-id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('firm:contract_update', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = slugify(str(self.worksite.firm).replace('ı','i'))+'/'+slugify(str(self.worksite).replace('ı','i'))+'/contract/'+slugify(str(self.name).replace('ı','i'))+os.path.splitext(self.file.name)[1]
        return super(Contract, self).save(*args, **kwargs)


# ŞARTNAME
class Specification(models.Model):
    id = models.AutoField(primary_key=True)
    contract = models.ForeignKey('Contract', verbose_name='Sözleşme', related_name="specifications", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Şartname Adı")
    file = models.FileField(verbose_name='Şartname', help_text="İmzalı şartnameyi PDF olarak yükleyiniz.")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Specification'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('firm:contract_specification_update', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = slugify(str(self.contract.worksite.firm).replace('ı','i'))+'/'+slugify(str(self.contract.worksite).replace('ı','i'))+'/specification/'+slugify(str(self.name).replace('ı','i'))+os.path.splitext(self.file.name)[1]
        return super(Specification, self).save(*args, **kwargs)


# PROJE
class Project(models.Model):
    category = (
        ("Statik", "Statik"),
        ("Mimari", "Mimari"),
        ("Mekanik", "Mekanik"),
        ("Elektrik", "Elektrik"),
        ("Peyzaj", "Peyzaj")
    )
    id = models.AutoField(primary_key=True)
    worksite = models.ForeignKey('Worksite', verbose_name='Şantiye', related_name="projects", on_delete=models.CASCADE)
    no = models.CharField(max_length=10, verbose_name="Revize No")
    name = models.CharField(max_length=50, verbose_name="Proje Adı")
    date = models.DateField(verbose_name="Revize Tarihi")
    category = models.CharField(max_length=10, verbose_name="Kategori", choices=category, default="Statik")
    file = models.FileField(verbose_name='Proje', help_text="Projeyi DWG olarak yükleyiniz.")
    create_date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        db_table = 'Project'
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('firm:project_update', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if self.file:
            self.file.name = slugify(str(self.worksite.firm).replace('ı','i'))+'/'+slugify(str(self.worksite).replace('ı','i'))+'/project/'+slugify(str(self.category))+'/'+str(self.no)+slugify(str(self.name).replace('ı','i'))+os.path.splitext(self.file.name)[1]
        return super(Project, self).save(*args, **kwargs)


