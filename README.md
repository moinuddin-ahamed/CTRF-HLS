# Vitis HLS 2023.2 Synthesis Report
## BDS and OBDS HLS Implementation for xcu250-figd2104-2L-e FPGA

### Synthesis Overview

Both BDS (Bidirectional Data Structure) and OBDS (Optimized Bidirectional Data Structure) models have been successfully synthesized using Vitis HLS 2023.2 targeting the Xilinx UltraScale+ xcu250 FPGA device.

## Model Architectures

### BDS Model Architecture
- **Input Layer**: 16 features
- **Hidden Layer 1**: 32 neurons (Dense + ReLU)
- **Hidden Layer 2**: 16 neurons (Dense + ReLU) 
- **Hidden Layer 3**: 8 neurons (Dense + ReLU)
- **Output Layer**: 2 neurons (Dense + Softmax)
- **Total Parameters**: 1,226

### OBDS Model Architecture
- **Input Layer**: 16 features
- **Hidden Layer 1**: 24 neurons (Dense + ReLU)
- **Hidden Layer 2**: 12 neurons (Dense + ReLU)
- **Output Layer**: 2 neurons (Dense + Softmax)
- **Total Parameters**: 734

## Performance Analysis

### Timing Performance

| Model | Latency (cycles) | Latency (ns) | Clock Period | Estimated Fmax | Initiation Interval |
|-------|------------------|--------------|--------------|----------------|---------------------|
| **BDS**  | 17              | 170.000      | 10ns (100MHz) | 137.34 MHz     | 4                   |
| **OBDS** | 14              | 140.000      | 10ns (100MHz) | 169.28 MHz     | 4                   |

### Performance Insights
- **OBDS is 17.6% faster** than BDS (14 vs 17 cycles)
- **OBDS has 23% higher Fmax** (169.28 MHz vs 137.34 MHz)
- Both models maintain the same initiation interval (II = 4)
- OBDS achieves better performance due to its simpler architecture with fewer layers

## Resource Utilization

### Overall Resource Comparison

| Resource Type | BDS Usage | BDS % of Device | OBDS Usage | OBDS % of Device | OBDS Savings |
|---------------|-----------|-----------------|------------|------------------|--------------|
| **DSP48s**    | 294       | 2%              | 176        | 1%               | **40.1%**    |
| **BRAMs**     | 4         | ~0%             | 4          | ~0%              | **0%**       |
| **Flip-Flops**| 9,429     | ~0%             | 6,074      | ~0%              | **35.6%**    |
| **LUTs**      | 42,704    | 2%              | 25,276     | 1%               | **40.8%**    |
| **URAMs**     | 0         | 0%              | 0          | 0%               | **0%**       |

### Detailed Layer-by-Layer Analysis

#### BDS Model Resource Breakdown
```
Layer 1 (16→32): DSP: 128, FF: 3,855, LUT: 17,667
Layer 2 (32→16): DSP: 128, FF: 2,951, LUT: 17,546  
Layer 3 (16→8):  DSP: 32,  FF: 1,147, LUT: 4,479
Layer 4 (8→2):   DSP: 4,   FF: 272,   LUT: 575
Softmax:         DSP: 2,   FF: 37,    LUT: 213, BRAM: 4
```

#### OBDS Model Resource Breakdown
```
Layer 1 (16→24): DSP: 96,  FF: 2,865, LUT: 12,992
Layer 2 (24→12): DSP: 72,  FF: 1,896, LUT: 9,817
Layer 3 (12→2):  DSP: 6,   FF: 399,   LUT: 792
Softmax:         DSP: 2,   FF: 37,    LUT: 213, BRAM: 4
```

## Hardware Implementation Details

### Interface Specifications
- **Input**: 256-bit wide interface for 16 features (16-bit each)
- **Output**: 2×16-bit outputs for classification results
- **Protocol**: AXI4-Stream with ap_ctrl_hs control interface
- **Precision**: ap_fixed<16,6> (16-bit fixed-point, 6 integer bits)

### Memory Organization
- **BRAM Usage**: 4 BRAMs for softmax lookup tables (exponential and inverse)
- **Array Partitioning**: Complete partitioning applied to all intermediate arrays
- **Pipeline Strategy**: Function-level pipelining with II=4

### Optimization Features
- **Loop Unrolling**: Complete unrolling of all dense layer loops
- **Expression Balancing**: Automatic optimization of arithmetic expressions
- **Resource Sharing**: Optimized DSP utilization across layers
- **Fixed-Point Arithmetic**: 16-bit precision with 6 integer bits

## Synthesis Quality Metrics

### Resource Efficiency
| Metric | BDS | OBDS | OBDS Advantage |
|--------|-----|------|----------------|
| **DSPs per Parameter** | 0.24 | 0.24 | Same efficiency |
| **LUTs per Parameter** | 34.8 | 34.4 | 1.1% more efficient |
| **Performance/DSP** | 0.47 MHz/DSP | 0.96 MHz/DSP | **104% better** |

### Design Characteristics
- **Clock Domain**: Single clock domain at 100 MHz
- **Reset Strategy**: Synchronous reset with active high polarity
- **Interface Type**: Blocking handshake protocol (ap_ctrl_hs)
- **Memory Access**: All weights and biases stored in distributed RAM/LUTs

## Compiler Optimizations Applied

### HLS Pragmas and Directives
1. **Pipeline Directives**: Applied to all layer functions
2. **Array Partitioning**: Complete partitioning for parallel access
3. **Loop Unrolling**: Complete unrolling for maximum parallelism
4. **Interface Optimization**: Optimal port configurations

### Synthesis Flow Optimizations
- **Expression Balancing**: 380+ expressions balanced in BDS, 283+ in OBDS
- **Resource Binding**: Optimal DSP and LUT mapping
- **Dataflow Optimization**: Efficient data movement between layers
- **Clock Domain Optimization**: Single clock strategy for timing closure

## Comparison Summary

### OBDS Advantages over BDS:
1. **40% Reduction in DSP Usage** (294 → 176 DSPs)
2. **36% Reduction in Flip-Flops** (9,429 → 6,074 FFs)
3. **41% Reduction in LUT Usage** (42,704 → 25,276 LUTs)
4. **18% Faster Execution** (170ns → 140ns)
5. **23% Higher Clock Frequency** (137MHz → 169MHz)
6. **Same Memory Footprint** (4 BRAMs each)

### Key Insights:
- **OBDS demonstrates superior resource efficiency** with significantly lower hardware requirements
- **Performance gains** are substantial despite fewer parameters
- **Memory usage remains constant** due to fixed softmax implementation
- **Both designs fit comfortably** within the xcu250 device resources

## Target Device Specifications

**Xilinx UltraScale+ xcu250-figd2104-2L-e:**
- DSP48s: ~12,000 available
- Block RAM: ~2,160 available  
- UltraRAM: ~960 available
- Flip-Flops: ~2,364,480 available
- LUTs: ~1,182,240 available

Both implementations utilize <3% of available device resources, leaving substantial capacity for additional processing elements or system integration.

---

*Generated by Vitis HLS 2023.2 on Wed Aug 6, 2025*
*Target Device: xcu250-figd2104-2L-e*
*Clock Frequency: 100 MHz (10ns period)*
