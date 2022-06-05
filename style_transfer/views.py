from django.shortcuts import render
from .forms import PhotoForm, StyleForm
from .models import Photo, Style
from .network import load_image, load_tf_hub
from django.http import JsonResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io, base64
import mimetypes
from django.views import View


class MainView(View):
    
    def get(self,request):
        context = {'form': PhotoForm(),'form2': StyleForm()}
        context["styles"] = Style.objects.all()
  
        return render(request,'style_transfer/index.html', context)
    
    
    def post(self,request):
        
        form = PhotoForm(request.POST, request.FILES)
        form2 = StyleForm(request.POST)
        if not form.is_valid():
            raise ValueError('Formが不正です。')
        if not form2.is_valid():
            raise ValueError('Form2が不正です。')
        
        if form.is_valid():
            file_name = form.cleaned_data['image'].name
            photo = Photo(image=form.cleaned_data['image'])
            photo.save()
               
        if form2.is_valid():
            #画面で選択した変換スタイル名を取得
            selected_style = form2.cleaned_data.get('name')
            #変換スタイル画像のパスを取得
            style_image_path= Style.objects.get(name=selected_style).image.path
        
        
        #変換画像のロード
        content_image = load_image(photo.image.path, (384, 384))
        #スタイル画像のロード
        style_image = load_image(style_image_path, (256, 256))  #画像を(1, 384, 384, 3)に変換
        style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')   #画像を(1, 256, 256, 3)に変換
        
        #画像スタイル変換モデルのロード
        hub_module = load_tf_hub()
        
        #スタイル変換処理の実行
        outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
        stlylized_image = np.array(outputs[0][0])
        
        
        pil_img = Image.fromarray((stlylized_image * 255).astype('uint8'), mode='RGB') 
        buffer = io.BytesIO()
        pil_img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue())
        img_str = str(img_str)[2:-1]
        content_type=mimetypes.guess_type(file_name)[0]
        translated_img = 'data:' + content_type + ';base64,' + img_str
        
        d = {
            'img_str' : translated_img,
        }

        return JsonResponse(d)
