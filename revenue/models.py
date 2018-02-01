from django.db import models

class Revenue(models.Model):
    good = models.CharField(blank=False, max_length=255, verbose_name="Product type")
    revenue = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Revenue")
    date_sold = models.DateField(verbose_name="Date sold")

    class Meta:
        db_table = 'revenue'
        verbose_name = 'Revenue by goods'

    def __unicode__(self):
        if self.good:
            return '%s' % self.good

        return 'Good'

# Create your models here.
