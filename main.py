from __future__ import print_function

import time

import tensorflow.compat.v1 as tf


from data import DataGenerator


def define_net(input_batch):
    return input_batch + 20  # simplest network I could think of.


def main():
    tf.compat.v1.disable_eager_execution()
    batch_size = 4

    coord = tf.train.Coordinator()
    with tf.name_scope('create_inputs'):
        reader = DataGenerator(coord)
        input_batch = reader.dequeue(batch_size)

    sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
    init = tf.global_variables_initializer()
    sess.run(init)

    threads = reader.start_threads(sess)
    net = define_net(input_batch)
    queue_size = reader.queue_size
    for step in range(10000):
        print('size queue =', queue_size.eval(session=sess))
        print(sess.run(net))

        # Make this thread slow. You can comment this line. If you do so, you will dequeue
        # faster than you enqueue, so expect the queue not to reach its maximum (32 by default)
        time.sleep(1)

    coord.request_stop()
    print("stop requested.")
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
