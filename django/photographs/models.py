from django.db import models
from django.urls import reverse
from account.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Photograph(models.Model):
    """
    A photograph and related data
    """

    related_name = 'photographs'

    image = models.ImageField(upload_to='photographs', blank=True, null=True)
    description_es = RichTextUploadingField(blank=True, null=True, verbose_name='Description (Spanish)')
    description_en = RichTextUploadingField(blank=True, null=True, verbose_name='Description (English)')
    acknowledgements = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False, help_text='Check this box to include this photograph on the public website')
    notes = models.TextField(blank=True, null=True, help_text='Notes are for admins only and will not be visible on the public website')

    # Metadata
    meta_created_by = models.ForeignKey(User, related_name=f'{related_name}_created_by', on_delete=models.PROTECT, blank=True, null=True, verbose_name="created by")
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
    meta_lastupdated_by = models.ForeignKey(User, related_name=f'{related_name}_lastupdated_by', on_delete=models.PROTECT, blank=True, null=True, verbose_name="last updated by")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    @property
    def admin_url(self):
        return reverse('admin:photographs_photograph_change', args=[self.id])

    @property
    def image_name(self):
        return str(self.image.name).split('/')[-1].split('.')[0]

    def __str__(self):
        return f'Photograph #{self.id}: {self.image_name}'

    def get_absolute_url(self):
        return reverse('photographs:detail', args=[self.meta_slug])


class PhotographUserContribution(models.Model):
    """
    A user's contribution in response to a photograph
    """

    related_name = 'photographusercontributions'

    photograph = models.ForeignKey(Photograph, related_name=related_name, on_delete=models.PROTECT)
    contribution = models.TextField()
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    agree_to_ethics = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True, help_text='Notes are for admins only and will not be visible on the public website')

    # Metadata
    meta_created_datetime = models.DateTimeField(default=timezone.now, verbose_name="created")
    meta_lastupdated_datetime = models.DateTimeField(blank=True, null=True, verbose_name="last updated")

    def __str__(self):
        return f'User contribution for "{self.photograph}" on {str(self.meta_created_datetime)[:19]}'
