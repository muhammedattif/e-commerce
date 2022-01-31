from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
          return self.name


class Category(MPTTModel):
    """docstring for ParentCategory."""

    # add initial values to db when migrating

    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='childs',
        on_delete=models.SET_NULL
    )

    class Meta:
        unique_together = ('name', 'parent')
        verbose_name_plural = 'Categories'

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])
