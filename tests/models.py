from django.db import models


class Language(models.Model):
    iso = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    shortlist = models.BooleanField(default=False)

    def __str__(self):
        return self.iso

    class Meta:
        ordering = ("iso",)


class Paper(models.Model):
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=30, blank=True, null=True)
