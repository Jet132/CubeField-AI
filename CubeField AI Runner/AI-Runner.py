import tensorflow as tf
from PIL import ImageGrab
from numpy import array
import time
from pynput.keyboard import Key,Controller

keyboard = Controller()

x = tf.placeholder(tf.float32, [None, 247, 392, 3])

def resize_image(image, resized_size):
    size = image.size
    if(size[0] > resized_size[0] and size[1] > resized_size[1]):
        ratio = (size[0]-resized_size[0])-(size[1]-resized_size[1])
        if(ratio > 0):
            new_width  = resized_size[0]
            new_height = new_width * size[1] / size[0]
        else:
            new_height = resized_size[1]
            new_width  = new_height * size[0] / size[1]
        #print(new_height,new_width)
        image = image.resize((int(new_width), int(new_height)))
    #image.show()
    return image

def create_new_conv_layer(input_data, num_input_channels, num_filters, filter_shape, pool_shape, name):
    # setup the filter input shape for tf.nn.conv_2d
    conv_filt_shape = [filter_shape[0], filter_shape[1], num_input_channels,
                      num_filters]

    # initialise weights and bias for the filter
    weights = tf.Variable(tf.truncated_normal(conv_filt_shape, stddev=0.03),
                                      name=name+'_W')
    bias = tf.Variable(tf.truncated_normal([num_filters]), name=name+'_b')

    # setup the convolutional layer operation
    out_layer = tf.nn.conv2d(input_data, weights, [1, 1, 1, 1], padding='SAME')

    # add the bias
    out_layer += bias

    # apply a ReLU non-linear activation
    out_layer = tf.nn.relu(out_layer)

    # now perform max pooling
    ksize = [1, pool_shape[0], pool_shape[1], 1]
    strides = [1, 2, 2, 1]
    out_layer = tf.nn.max_pool(out_layer, ksize=ksize, strides=strides, 
                               padding='SAME')

    return out_layer

# create some convolutional layers
layer1 = create_new_conv_layer(x, 3, 9, [5, 5], [2, 2], name='layer1')
layer2 = create_new_conv_layer(layer1, 9, 18, [5, 5], [2, 2], name='layer2')
layer3 = create_new_conv_layer(layer2, 18, 18, [5, 5], [2, 2], name='layer3')
layer4 = create_new_conv_layer(layer3, 18, 18, [5, 5], [2, 2], name='layer4')
layer5 = create_new_conv_layer(layer4, 18, 18, [5, 5], [2, 2], name='layer5')

flattened = tf.reshape(layer5, [-1, 13*8*18])

# setup some weights and bias values for this layer, then activate with ReLU
wd1 = tf.Variable(tf.truncated_normal([13*8*18, 1000], stddev=0.03), name='wd1')
bd1 = tf.Variable(tf.truncated_normal([1000], stddev=0.01), name='bd1')
dense_layer1 = tf.matmul(flattened, wd1) + bd1
dense_layer1 = tf.nn.relu(dense_layer1)

# another layer with softmax activations
wd2 = tf.Variable(tf.truncated_normal([1000, 3], stddev=0.03), name='wd2')
bd2 = tf.Variable(tf.truncated_normal([3], stddev=0.01), name='bd2')
dense_layer2 = tf.matmul(dense_layer1, wd2) + bd2
y_ = tf.nn.softmax(dense_layer2)

with tf.Session() as sess:
    saver = tf.train.Saver()
    saver.restore(sess, 'Model 1\CubeFieldCNN.ckpt')
    while (0==0):
        img = resize_image(ImageGrab.grab().crop((540, 390, 1325, 885)), [392, 247])
        input = [array(img)]
        output = sess.run(y_, feed_dict={x: input})
        if(output[0][0] > output[0][1] and output[0][0] > output[0][2]):
            keyboard.release(Key.right)
            keyboard.press(Key.left)
        elif(output[0][1] > output[0][0] and output[0][1] > output[0][2]):
            keyboard.release(Key.left)
            keyboard.release(Key.right)
        elif(output[0][2] > output[0][0] and output[0][2] > output[0][1]):
            keyboard.release(Key.left)
            keyboard.press(Key.right)
    
    