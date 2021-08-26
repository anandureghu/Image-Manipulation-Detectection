from django.db import models
import os
from django.conf import settings
# Create your models here.
class Images(models.Model):
    image = models.ImageField(upload_to='media/images')
    status = models.BooleanField(blank=True)

class Test(models.Model):
    image = models.ImageField(upload_to='media')
    status = models.BooleanField(blank=True, null=True, default=False)
    label = models.CharField(max_length=10, blank=True, null=True)
    result_img = models.ImageField(upload_to='media', null=True)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Test,self).delete(*args,**kwargs)