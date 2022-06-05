import tensorflow as tf
import tensorflow_hub as hub


def crop_center(image):
  """正方形に切り取られた画像を返す。"""
  shape = image.shape
  new_shape = min(shape[1], shape[2])
  offset_y = max(shape[1] - shape[2], 0) // 2
  offset_x = max(shape[2] - shape[1], 0) // 2
  image = tf.image.crop_to_bounding_box(
      image, offset_y, offset_x, new_shape, new_shape)
  return image


def load_image(image_path, image_size=(256, 256), preserve_aspect_ratio=True):
  """画像の読み込みと前処理.
  float32のnumpy配列をロードして変換し、バッチ次元を追加して、範囲 [0, 1]に正規化する。
  インプット：画像のパス
  アウトプット：画像のEagerTensor型データ
  """ 
  img = tf.io.decode_image(
      tf.io.read_file(image_path),
      channels=3, dtype=tf.float32)[tf.newaxis, ...]
  img = crop_center(img)  # img_shape= (1, 768, 768, 3) #３次元目を２次元目と揃える。
  img = tf.image.resize(img, image_size, preserve_aspect_ratio=True) #image_sizeにリサイズする。
  return img  




def load_tf_hub():
    hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
    hub_module = hub.load(hub_handle)
    return hub_module


def conversion(content_image, style_image):
    hub_module = load_tf_hub()
    outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
    print("type=",type(outputs))
    print(outputs[0].shape)
    stylized_image = outputs[0]
    print("stylized_image.shape=", stylized_image.shape)
    return stylized_image
    

    
