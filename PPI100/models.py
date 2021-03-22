from django.db import models

# Create your models here.
class mst_PPI100(models.Model):
    Product_Code=models.IntegerField()
    Commodity=models.CharField(max_length=100)
    industry=models.CharField(max_length=100)
    Unit=models.CharField(max_length=100)
    Value=models.CharField(max_length=100)
    Date=models.DateTimeField()


    def __str__(self):
        return self.Commodity
