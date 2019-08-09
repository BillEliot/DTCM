from django.db import models

class Sort(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=20)
    description = models.TextField(default='')
    parentSort = models.ForeignKey('Sort', on_delete=models.CASCADE)

    def __str__(self):
        return self.sortName



class Entry(models.Model):
    SimplifiedName = models.CharField(max_length=50)
    TraditionalName = models.CharField(max_length=50, blank=True, null=True)
    PinyinName = models.CharField(max_length=50)
    EnglishName_1 = models.CharField(max_length=100)
    EnglishName_2 = models.CharField(max_length=100, blank=True, null=True)
    EnglishName_3 = models.CharField(max_length=100, blank=True, null=True)
    EnglishInterpretation = models.TextField(blank=True, null=True)
    sort = models.ForeignKey('Sort', on_delete=models.CASCADE)

    def __str__(self):
        return self.SimplifiedName



class Review(models.Model):
    entry = models.ForeignKey('Entry', on_delete=models.CASCADE)
    item = models.CharField(max_length=30)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.entry.SimplifiedName
