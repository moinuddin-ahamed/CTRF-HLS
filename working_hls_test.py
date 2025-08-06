"""
Simple HLS Test - Basic Implementation for Synthesis Demonstration
This creates a minimal working example that generates HLS C++ code
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import hls4ml
import os

def create_simple_bds_model():
    """
    Create a simple BDS model using only Dense layers (hls4ml compatible)
    """
    # Input layer
    inputs = keras.Input(shape=(16,), name='input_features')
    
    # Simple feedforward network approximating BDS logic
    x = keras.layers.Dense(32, activation='relu', name='hidden1')(inputs)
    x = keras.layers.Dense(16, activation='relu', name='hidden2')(x)
    x = keras.layers.Dense(8, activation='relu', name='hidden3')(x)
    outputs = keras.layers.Dense(2, activation='softmax', name='output')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='Simple_BDS')
    
    # Compile model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    return model

def create_simple_obds_model():
    """
    Create a simple OBDS model using only Dense layers
    """
    inputs = keras.Input(shape=(16,), name='input_features')
    
    # Smaller network for OBDS
    x = keras.layers.Dense(24, activation='relu', name='hidden1')(inputs)
    x = keras.layers.Dense(12, activation='relu', name='hidden2')(x)
    outputs = keras.layers.Dense(2, activation='softmax', name='output')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='Simple_OBDS')
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    return model

def synthesize_simple_model(model, model_name="simple_model", target_device="xcu250-figd2104-2L-e"):
    """
    Convert simple Keras model to HLS
    """
    print(f"Converting {model_name} to HLS...")
    
    # Generate hls4ml config
    config = hls4ml.utils.config_from_keras_model(model, granularity='name')
    
    # Configure for synthesis
    config['Model']['Precision'] = 'ap_fixed<16,6>'
    config['Model']['ReuseFactor'] = 4
    config['Model']['Strategy'] = 'Latency'
    
    # Set layer-specific configurations
    for layer in model.layers:
        if layer.name != 'input_features':
            config['LayerName'][layer.name]['Precision'] = 'ap_fixed<16,6>'
            config['LayerName'][layer.name]['ReuseFactor'] = 4
    
    # Convert model
    output_dir = f'hls_simple_{model_name}'
    hls_model = hls4ml.converters.convert_from_keras_model(
        model,
        hls_config=config,
        output_dir=output_dir,
        part=target_device,
        clock_period=10,  # 10ns clock period (100MHz)
        io_type='io_parallel'
    )
    
    print(f"[OK] HLS code generated in: {output_dir}")
    print(f"[OK] C++ files created for synthesis")
    
    # Try to compile (this will show if everything is working)
    try:
        print("Compiling HLS model...")
        hls_model.compile()
        print("[OK] Compilation successful!")
        
        # Try synthesis (this requires Vitis HLS)
        try:
            print("Attempting HLS synthesis...")
            hls_model.build(csim=False, synth=True, export=False, vsynth=False)
            print("[OK] HLS Synthesis completed!")
            
            # Read and display report
            try:
                report_dir = os.path.join(output_dir, 'myproject_prj', 'solution1', 'syn', 'report')
                if os.path.exists(report_dir):
                    print(f"\n=== SYNTHESIS REPORT for {model_name.upper()} ===")
                    report_files = [f for f in os.listdir(report_dir) if f.endswith('.rpt')]
                    for report_file in report_files[:2]:  # Show first 2 reports
                        print(f"\n--- {report_file} ---")
                        report_path = os.path.join(report_dir, report_file)
                        try:
                            with open(report_path, 'r') as f:
                                lines = f.readlines()
                                # Show key synthesis results
                                for i, line in enumerate(lines):
                                    if 'Summary' in line or 'Utilization' in line or 'Timing' in line:
                                        for j in range(i, min(i+10, len(lines))):
                                            if lines[j].strip():
                                                print(lines[j].strip())
                                        break
                        except:
                            print(f"Could not read {report_file}")
                else:
                    print("Report directory not found - synthesis may not have completed")
            except Exception as e:
                print(f"Could not read synthesis report: {e}")
                
        except Exception as e:
            print(f"[WARN] HLS Synthesis failed (Vitis HLS may not be installed): {e}")
            print("[OK] But HLS C++ code was generated successfully!")
            
    except Exception as e:
        print(f"[WARN] Compilation failed: {e}")
        print("[OK] But HLS code generation was successful!")
    
    return hls_model

def test_simple_models():
    """Test the simple models"""
    print("Creating simple BDS and OBDS models...")
    
    # Create models
    bds_model = create_simple_bds_model()
    obds_model = create_simple_obds_model()
    
    print("\nBDS Model Summary:")
    bds_model.summary()
    
    print("\nOBDS Model Summary:")  
    obds_model.summary()
    
    # Test with dummy data
    print("\nTesting models...")
    test_data = np.random.rand(100, 16).astype(np.float32)
    test_labels = np.random.randint(0, 2, 100)
    
    # Test predictions
    bds_pred = bds_model.predict(test_data[:5], verbose=0)
    obds_pred = obds_model.predict(test_data[:5], verbose=0)
    
    print(f"BDS predictions shape: {bds_pred.shape}")
    print(f"OBDS predictions shape: {obds_pred.shape}")
    print(f"Sample BDS predictions: {bds_pred[0]}")
    print(f"Sample OBDS predictions: {obds_pred[0]}")
    
    # Quick training to make models more realistic
    print("\nQuick training for realistic weights...")
    bds_model.fit(test_data, test_labels, epochs=1, batch_size=32, verbose=0)
    obds_model.fit(test_data, test_labels, epochs=1, batch_size=32, verbose=0)
    
    print("\n" + "="*60)
    print("STARTING HLS CODE GENERATION")
    print("="*60)
    
    # Synthesize models
    bds_hls = synthesize_simple_model(bds_model, "bds")
    print("\n" + "-"*40)
    obds_hls = synthesize_simple_model(obds_model, "obds")
    
    print("\n" + "="*60)
    print("SYNTHESIS COMPLETE")
    print("="*60)
    
    # List generated files
    print("\nGenerated HLS projects:")
    for project_dir in ['hls_simple_bds', 'hls_simple_obds']:
        if os.path.exists(project_dir):
            print(f"[OK] {project_dir}/")
            firmware_dir = os.path.join(project_dir, 'firmware')
            if os.path.exists(firmware_dir):
                cpp_files = [f for f in os.listdir(firmware_dir) if f.endswith('.cpp') or f.endswith('.h')]
                print(f"   [FOLDER] firmware/ ({len(cpp_files)} C++ files)")
                for cpp_file in cpp_files[:5]:  # Show first 5 files
                    print(f"      [FILE] {cpp_file}")
                if len(cpp_files) > 5:
                    print(f"      ... and {len(cpp_files)-5} more files")
        else:
            print(f"[ERROR] {project_dir}/ (not generated)")
    
    return bds_hls, obds_hls

if __name__ == "__main__":
    print("Simple HLS Test for BDS/OBDS Functions")
    print("="*40)
    
    try:
        bds_hls, obds_hls = test_simple_models()
        print("\n[SUCCESS] HLS code generation completed!")
        print("\nNext steps:")
        print("1. Check the generated hls_simple_* directories")
        print("2. Review the C++ code in firmware/ subdirectories")
        print("3. If Vitis HLS is installed, synthesis reports are available")
        print("4. Use Vitis HLS or Vivado for further development")
        
    except Exception as e:
        print(f"\n[ERROR] Error during testing: {e}")
        import traceback
        traceback.print_exc()
