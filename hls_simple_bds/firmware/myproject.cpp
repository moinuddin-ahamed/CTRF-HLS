#include <iostream>

#include "myproject.h"
#include "parameters.h"


void myproject(
    input_t input_features[N_INPUT_1_1],
    result_t layer9_out[N_LAYER_8]
) {

    // hls-fpga-machine-learning insert IO
    #pragma HLS ARRAY_RESHAPE variable=input_features complete dim=0
    #pragma HLS ARRAY_PARTITION variable=layer9_out complete dim=0
    #pragma HLS INTERFACE ap_vld port=input_features,layer9_out 
    #pragma HLS PIPELINE

    // hls-fpga-machine-learning insert load weights
#ifndef __SYNTHESIS__
    static bool loaded_weights = false;
    if (!loaded_weights) {
        nnet::load_weights_from_txt<hidden1_weight_t, 512>(w2, "w2.txt");
        nnet::load_weights_from_txt<hidden1_bias_t, 32>(b2, "b2.txt");
        nnet::load_weights_from_txt<hidden2_weight_t, 512>(w4, "w4.txt");
        nnet::load_weights_from_txt<hidden2_bias_t, 16>(b4, "b4.txt");
        nnet::load_weights_from_txt<hidden3_weight_t, 128>(w6, "w6.txt");
        nnet::load_weights_from_txt<hidden3_bias_t, 8>(b6, "b6.txt");
        nnet::load_weights_from_txt<output_weight_t, 16>(w8, "w8.txt");
        nnet::load_weights_from_txt<output_bias_t, 2>(b8, "b8.txt");
        loaded_weights = true;    }
#endif
    // ****************************************
    // NETWORK INSTANTIATION
    // ****************************************

    // hls-fpga-machine-learning insert layers

    layer2_t layer2_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer2_out complete dim=0
    nnet::dense<input_t, layer2_t, config2>(input_features, layer2_out, w2, b2); // hidden1

    layer3_t layer3_out[N_LAYER_2];
    #pragma HLS ARRAY_PARTITION variable=layer3_out complete dim=0
    nnet::relu<layer2_t, layer3_t, relu_config3>(layer2_out, layer3_out); // hidden1_relu

    layer4_t layer4_out[N_LAYER_4];
    #pragma HLS ARRAY_PARTITION variable=layer4_out complete dim=0
    nnet::dense<layer3_t, layer4_t, config4>(layer3_out, layer4_out, w4, b4); // hidden2

    layer5_t layer5_out[N_LAYER_4];
    #pragma HLS ARRAY_PARTITION variable=layer5_out complete dim=0
    nnet::relu<layer4_t, layer5_t, relu_config5>(layer4_out, layer5_out); // hidden2_relu

    layer6_t layer6_out[N_LAYER_6];
    #pragma HLS ARRAY_PARTITION variable=layer6_out complete dim=0
    nnet::dense<layer5_t, layer6_t, config6>(layer5_out, layer6_out, w6, b6); // hidden3

    layer7_t layer7_out[N_LAYER_6];
    #pragma HLS ARRAY_PARTITION variable=layer7_out complete dim=0
    nnet::relu<layer6_t, layer7_t, relu_config7>(layer6_out, layer7_out); // hidden3_relu

    layer8_t layer8_out[N_LAYER_8];
    #pragma HLS ARRAY_PARTITION variable=layer8_out complete dim=0
    nnet::dense<layer7_t, layer8_t, config8>(layer7_out, layer8_out, w8, b8); // output

    nnet::softmax<layer8_t, result_t, softmax_config9>(layer8_out, layer9_out); // output_softmax

}

