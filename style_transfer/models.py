from django.db import models
#from tensorflow import keras
#from tensorflow.keras.models import load_model
from PIL import Image
#from gan.network import CycleGAN
from django.conf import settings
import functools
import os


import numpy as np


#import numpy as np
#import tensorflow as tf
import io, base64
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Photo(models.Model):

    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return str(self.image.path)
    

class Style(models.Model):

    name = models.CharField("スタイル名", max_length=100)
    image = models.ImageField("スタイル画像", upload_to='style_images')
    def __str__(self):
        return self.name
    
    
@receiver(post_delete, sender=Style)
def delete_file(sender, instance, **kwargs):
    instance.image.delete(False)

