# inference with tensorflow

from __future__ import absolute_import
import argparse
import numpy as np
from six import text_type as _text_type
from tensorflow.contrib.keras.api.keras.preprocessing import image
import tensorflow as tf


parser = argparse.ArgumentParser()

parser.add_argument('-n', type=_text_type, default='kit_imagenet',
                    help='Network structure file name.')


parser.add_argument('-w', type=_text_type, required=True,
                    help='Network weights file name')

parser.add_argument('--image', '-i',
                    type=_text_type, help='Test image path.',
                    default="mmdnn/conversion/examples/data/seagull.jpg"
)


args = parser.parse_args()
if args.n.endswith('.py'):
    args.n = args.n[:-3]

# import converted model
model_converted = __import__(args.n).KitModel(args.w)
input_tf, model_tf = model_converted

# load img with BGRTranspose=True
img = image.load_img(args.image, target_size = (112, 112))
img = image.img_to_array(img)
img = img[..., ::-1]

input_data = np.expand_dims(img, 0)

# inference with tensorflow
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    predict = sess.run(model_tf, feed_dict = {input_tf : input_data})
print(predict)