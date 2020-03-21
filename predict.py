from model import VietOcr
from dataset import DataSet
from generate_dataset import DataGenerator
import tensorflow as tf
import numpy as np
import cv2 as cv
from PIL import Image

def predict(character_image):
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    sess.run(tf.local_variables_initializer())
    saver = tf.train.import_meta_graph('viet_ocr_brain.ckpt.meta')
    saver.restore(sess, tf.train.latest_checkpoint('./'))

    graph = tf.get_default_graph()

    X = graph.get_tensor_by_name("X:0")
    Y = graph.get_tensor_by_name("Y:0")
    keep_prob = graph.get_tensor_by_name("keep_prob:0")
    logits = graph.get_tensor_by_name("fc2/logits:0")
    softmax = graph.get_tensor_by_name("softmax:0")

    probs, chars = sess.run([logits, softmax], feed_dict={X: character_image.reshape((1, 28, 28, 1)), keep_prob: 1})

    probs = (np.exp(probs) / np.sum(np.exp(probs))) * 100    
    idx = np.argmax(chars)
    return (probs[0, idx], idx)


ds = DataSet(test_prob=1, one_hot=False)
characters = DataGenerator().get_list_characters()

# x, y = ds.next_batch_test(1)

# print('x.shape', x.shape)
# print('y.shape', y.shape)


# prob, idx = predict(x)

# print('Input character: ', characters[int(y[0])])
# print('Predicted: ', characters[idx], ' with probability = ', prob, '%')
# print('Result: ', characters[int(y[0])] == characters[idx])
# print('-' * 10)


img = Image.open('test/train20X20/7/7_6.jpg').convert('L')

new_width = 28
new_height = 28
img = img.resize((new_width, new_height), Image.ANTIALIAS)

arr = np.array(img, np.float32)

flat_arr = arr.ravel()

flat_arr = flat_arr.reshape((1, 28, 28, 1))

prob, idx = predict(flat_arr)

print('Predicted: ', characters[idx], ' with probability = ', prob, '%')
print('-' * 10)