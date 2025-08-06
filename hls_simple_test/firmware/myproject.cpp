#include <iostream>

#include "myproject.h"
#include "parameters.h"


void myproject(
    input_t dense_1_input[N_INPUT_1_1],
    result_t layer5_out[N_LAYER_4]
) {

    // hls-fpga-machine-learning insert IO
    #pragma HLS ARRAY_RESHAPE variable=dense_1_input complete dim=0
    #pragma HLS ARRAY_PARTITION variable=layer5_out complete dim=0
    #pragma HLS INTERFACE ap_vld port=dense_1_input,layer5_out 
    #pragma HLS PIPELINE

    // hls-fpga-machine-learning insert load weights
#ifndef __SYNTHESIS__
    static bool loaded_weights = false;
    if (!loaded_weights) {
        nnet::load_weights_from_txt<dense_1_weight_t, 32>(w2, "w2.txt");
        nnet::load_weights_from_txt<dense_1_bias_t, 8>(b2, "b2.txt");
        nnet::load_weights_from_txt<dense_2_weight_t, 16>(w4, "w4.txt");
        nnet::load_weights_from_txt<dense_2_bias_t, 2>(b4, "b4.txt");
        loaded_weights = true;    }
#endif
    // ****************************************
    // NETWORK INSTANTIATION
    // ****************************************

    // hls-fpga-machine-learning insert layers

    dense_1_result_t layer2_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer2_out complete dim=0
    nnet::dense<input_t, dense_1_result_t, config2>(dense_1_input, layer2_out, w2, b2); // dense_1

    layer3_t layer3_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer3_out complete dim=0
    nnet::relu<dense_1_result_t, layer3_t, relu_config3>(layer2_out, layer3_out); // dense_1_relu

    dense_2_result_t layer4_out[N_LAYER_4];
    #pragma HLS ARRAY_PARTITION variable=layer4_out complete dim=0
    nnet::dense<layer3_t, dense_2_result_t, config4>(layer3_out, layer4_out, w4, b4); // dense_2

    nnet::softmax<dense_2_result_t, result_t, softmax_config5>(layer4_out, layer5_out); // dense_2_softmax

}

