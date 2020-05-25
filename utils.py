import tensorflow as tf
import numpy as np
from PIL import Image


def load_img(path_to_img):
    max_dim = 1024
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)

def generateNewsTweet(data, topic):
    source = data[0]['source']['name']
    description = data[0]['description']
    title = data[0]['title']
    url = data[0]['url']
    tweet_desc = 'Latest ' + topic + ' #news (via ' + source + '): ' + description + '\n' + url + '\n#technews #trn'
    tweet_title = 'Latest ' + topic + ' #news (via ' + source + '): ' + title + '\n' + url + '\n#technews #trn'
    tweet_normal = 'Latest ' + topic + ' #news (via ' + source + ')' + '\n' + url + '\n#technews #trn'

    if len(tweet_desc) < 280:
        return tweet_desc
    elif len(tweet_title) < 280:
        return tweet_title
    elif len(tweet_normal) < 280:
        return tweet_normal
    else:
        print('Tweet length exceeded')
        return None
