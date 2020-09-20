from djongo import models

from django.contrib.postgres.fields import ArrayField

class OptionsUrl(models.Model):
    url = models.CharField(max_length=200,default=None)
    request_type= models.CharField(max_length=200,default=None)

    class Meta:
        abstract = True
        
    def __str__(self):
        return self.url
    
class Fields(models.Model):
    field=models.CharField(max_length=255)
    label=models.CharField(max_length=255)
    data_type=models.CharField(max_length=255)
    default=models.CharField(max_length=255)
    field_type=models.CharField(max_length=255)
    field_type_label=models.CharField(max_length=255)
    is_removable=models.BooleanField(default=False)
    mandatory=models.BooleanField(default=False)
    options_list=ArrayField(models.CharField(max_length=255),blank=True,null=True)
    option_url = models.EmbeddedField(
        model_container=OptionsUrl,
        null=True
    )
    class Meta:
        abstract=True
    def __str__(self):
        return self.field

class Templates(models.Model):
    type=models.CharField(max_length=255)
    entity=models.CharField(max_length=255)
    customerId=models.IntegerField()
    law=models.CharField(max_length=255)
    fields = models.ArrayField(
        model_container=Fields,
        null=True
    )

    def __str__(self):
        return self.entity


