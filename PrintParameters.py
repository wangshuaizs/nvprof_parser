def print_parameter_info():

    parameter_count = 0
    print("="*64)
    for var in tf.trainable_variables():
        print(var.name, end='\t')
        print("@%s" % var.device, end='\t')
        print(var.shape)
        parameter_count = parameter_count + reduce(lambda x, y: x * y, var.get_shape().as_list())
    print("Total parameter : %d, i.e., %.0f MB" % (parameter_count, parameter_count/1024/256))
    print("="*64)