from django.db import models

class Entry(models.Model):
    SimplifiedName = models.CharField(max_length=50)
    TraditionalName = models.CharField(max_length=50)
    PinyinName = models.CharField(max_length=50)
    EnglishName_1 = models.CharField(max_length=50)
    EnglishName_2 = models.CharField(max_length=50)
    EnglishName_3 = models.CharField(max_length=50)
    EnglishInterpretation = models.TextField()

    def __str__(self):
        return self.SimplifiedName
