# nvprof_parser

- GPUTraceParser.py

This shell takes gpu trace generated by nvprof as input and creates a .xlsx file which includes the start/stop time of the computation in each iteration, wait time and compute time.
Note:
	- ```computation_start_flag```: the GPU operation as the begining of computation. e.g., 'cudnn::detail::implicit_convolve_sgemm'
	- ```computation_stop_flag```: the GPU operation as the begining of computation. e.g., 'cudnn::detail::wgrad_alg0_engine'