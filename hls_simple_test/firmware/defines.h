#ifndef DEFINES_H_
#define DEFINES_H_

#include "ap_fixed.h"
#include "ap_int.h"
#include "nnet_utils/nnet_types.h"
#include <cstddef>
#include <cstdio>

// hls-fpga-machine-learning insert numbers
#define N_INPUT_1_1 4
#define N_LAYER_2 8
#define N_LAYER_2 8
#define N_LAYER_4 2
#define N_LAYER_4 2


// hls-fpga-machine-learning insert layer-precision
typedef ap_fixed<16,6> input_t;
typedef ap_fixed<16,6> model_default_t;
typedef ap_fixed<35,15> dense_1_result_t;
typedef ap_fixed<16,6> dense_1_weight_t;
typedef ap_fixed<16,6> dense_1_bias_t;
typedef ap_uint<1> layer2_index;
typedef ap_fixed<16,6> layer3_t;
typedef ap_fixed<18,8> dense_1_relu_table_t;
typedef ap_fixed<36,16> dense_2_result_t;
typedef ap_fixed<16,6> dense_2_weight_t;
typedef ap_fixed<16,6> dense_2_bias_t;
typedef ap_uint<1> layer4_index;
typedef ap_fixed<16,6> result_t;
typedef ap_fixed<18,8> dense_2_softmax_table_t;
typedef ap_fixed<18,8,AP_RND,AP_SAT,0> dense_2_softmax_exp_table_t;
typedef ap_fixed<18,8,AP_RND,AP_SAT,0> dense_2_softmax_inv_table_t;


#endif
