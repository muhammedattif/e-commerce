from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    name = models.CharField(verbose_name = _('Name'), max_length=100)
    icon = models.ImageField(upload_to="brands/", blank=True, verbose_name = _('Icon'))

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    def __str__(self):
          return self.name


class Category(MPTTModel):
    """docstring for ParentCategory."""

    # add initial values to db when migrating

    name = models.CharField(max_length=100, unique=True, verbose_name = _('Name'))
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='childs',
        on_delete=models.SET_NULL,
        verbose_name = _('Parent')
    )

    class Meta:
        unique_together = ('name', 'parent')
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
