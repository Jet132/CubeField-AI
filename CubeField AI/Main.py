import tensorflow as tf
import BatchManager
BatchManager.load_dataset()

# Python optimisation variables
learning_rate = 0.0001
epochs = 100
batch_size = 50

# declare the training data placeholders
# input x - for 28 x 28 pixels = 784 - this is the flattened image data that is drawn from 
# mnist.train.nextbatch()
# dynamically reshape the input
x = tf.placeholder(tf.float32, [None, 99, 157, 3])
# now declare the output data placeholder - 10 digits
y = tf.placeholder(tf.float32, [None, 3])

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

flattened = tf.reshape(layer4, [-1, 7*10*18])

# setup some weights and bias values for this layer, then activate with ReLU
wd1 = tf.Variable(tf.truncated_normal([7*10*18, 1000], stddev=0.03), name='wd1')
bd1 = tf.Variable(tf.truncated_normal([1000], stddev=0.01), name='bd1')
dense_layer1 = tf.matmul(flattened, wd1) + bd1
dense_layer1 = tf.nn.relu(dense_layer1)

# another layer with softmax activations
wd2 = tf.Variable(tf.truncated_normal([1000, 3], stddev=0.03), name='wd2')
bd2 = tf.Variable(tf.truncated_normal([3], stddev=0.01), name='bd2')
dense_layer2 = tf.matmul(dense_layer1, wd2) + bd2
y_ = tf.nn.softmax(dense_layer2)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=dense_layer2, labels=y))

# add an optimiser
optimiser = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

# define an accuracy assessment operation
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# setup the initialisation operator
init_op = tf.global_variables_initializer()

print('starting training')

with tf.Session() as sess:
    saver = tf.train.Saver()
    '''saver.restore(sess, 'Model 1\CubeFieldCNN.ckpt')'''
    # initialise the variables
    sess.run(init_op)
    total_batch = int(2662 / batch_size)
    for epoch in range(epochs):
        avg_cost = 0
        for i in range(total_batch):
            batch_x, batch_y = BatchManager.get_Batch(batch_size)
            _, c = sess.run([optimiser, cross_entropy], feed_dict={x: batch_x, y: batch_y})
            avg_cost += c / total_batch
        batch_x, batch_y = BatchManager.get_Batch(batch_size)
        test_acc = sess.run(accuracy, 
                       feed_dict={x: batch_x, y: batch_y})
        print("Epoch:", (epoch + 1), "cost =", "{:.3f}".format(avg_cost), 
              "test accuracy: {:.3f}".format(test_acc))

    print("\nTraining complete!")
    batch_x, batch_y = BatchManager.get_Batch(batch_size)
    print(sess.run(accuracy, feed_dict={x: batch_x, y: batch_y}))
    save_path = saver.save(sess, 'Model 1\CubeFieldCNN.ckpt')
    print("Model saved in file: %s" % save_path)
