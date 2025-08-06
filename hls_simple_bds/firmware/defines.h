#ifndef DEFINES_H_
#define DEFINES_H_

#include "ap_fixed.h"
#include "ap_int.h"
#include "nnet_utils/nnet_types.h"
#include <cstddef>
#include <cstdio>

// hls-fpga-machine-learning insert numbers
#define N_INPUT_1_1 16
#define N_LAYER_2 32
#define N_LAYER_2 32
#define N_LAYER_4 16
#define N_LAYER_4 16
#define N_LAYER_6 8
#define N_LAYER_6 8
#define N_LAYER_8 2
#define N_LAYER_8 2


// hls-fpga-machine-learning insert layer-precision
typedef ap_fixed<16,6> input_t;
typedef ap_fixed<16,6> hidden1_accum_t;
typedef ap_fixed<16,6> layer2_t;
typedef ap_fixed<16,6> hidden1_weight_t;
typedef ap_fixed<16,6> hidden1_bias_t;
typedef ap_uint<1> layer2_index;
typedef ap_fixed<16,6> layer3_t;
typedef ap_fixed<18,8> hidden1_relu_table_t;
typedef ap_fixed<16,6> hidden2_accum_t;
typedef ap_fixed<16,6> layer4_t;
typedef ap_fixed<16,6> hidden2_weight_t;
typedef ap_fixed<16,6> hidden2_bias_t;
typedef ap_uint<1> layer4_index;
typedef ap_fixed<16,6> layer5_t;
typedef ap_fixed<18,8> hidden2_relu_table_t;
typedef ap_fixed<16,6> hidden3_accum_t;
typedef ap_fixed<16,6> layer6_t;
typedef ap_fixed<16,6> hidden3_weight_t;
typedef ap_fixed<16,6> hidden3_bias_t;
typedef ap_uint<1> layer6_index;
typedef ap_fixed<16,6> layer7_t;
typedef ap_fixed<18,8> hidden3_relu_table_t;
typedef ap_fixed<16,6> output_accum_t;
typedef ap_fixed<16,6> layer8_t;
typedef ap_fixed<16,6> output_weight_t;
typedef ap_fixed<16,6> output_bias_t;
typedef ap_uint<1> layer8_index;
typedef ap_fixed<16,6> result_t;
typedef ap_fixed<18,8> output_softmax_table_t;
typedef ap_fixed<18,8,AP_RND,AP_SAT,0> output_softmax_exp_table_t;
typedef ap_fixed<18,8,AP_RND,AP_SAT,0> output_softmax_inv_table_t;


#endif
