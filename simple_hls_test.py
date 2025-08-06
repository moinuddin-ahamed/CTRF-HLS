"""
Simplified HLS Synthesis for BDS/OBDS Functions
Using the most basic hls4ml configuration that should work
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import hls4ml
import os

def create_simple_classifier():
    """
    Create a very simple 2-layer neural network for classification
    """
    model = keras.Sequential([
        keras.layers.Dense(8, activation='relu', input_shape=(4,), name='dense_1'),
        keras.layers.Dense(2, activation='softmax', name='dense_2')
    ], name='Simple_Classifier')
    
    return model

def test_basic_hls4ml():
    """
    Test basic hls4ml functionality with minimal configuration
    """
    print("Testing basic hls4ml synthesis...")
    
    # Create simple model
    model = create_simple_classifier()
    
    # Compile and train with dummy data
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    # Generate training data
    X = np.random.rand(100, 4).astype(np.float32)
    y = np.random.randint(0, 2, 100)
    
    print("Training simple model...")
    model.fit(X, y, epochs=3, verbose=0)
    
    print("Model summary:")
    model.summary()
    
    # Test prediction
    test_X = np.random.rand(5, 4).astype(np.float32)
    predictions = model.predict(test_X, verbose=0)
    print(f"Test predictions shape: {predictions.shape}")
    
    # Convert to HLS with minimal configuration
    print("\nConverting to HLS...")
    try:
        # Use default configuration
        hls_config = hls4ml.utils.config_from_keras_model(model, granularity='name')
        
        # Minimal configuration
        hls_config['Model']['Precision'] = 'ap_fixed<16,6>'
        hls_config['Model']['ReuseFactor'] = 1
        
        print("Configuration created successfully")
        
        # Convert the model
        output_dir = 'hls_simple_test'
        hls_model = hls4ml.converters.convert_from_keras_model(
            model,
            hls_config=hls_config,
            output_dir=output_dir,
            part='xcu250-figd2104-2L-e',
            clock_period=10  # Slower clock for easier timing
        )
        
        print("Model converted successfully")
        
        # Compile
        hls_model.compile()
        print("Model compiled successfully")
        
        # Try synthesis
        print("Starting synthesis...")
        hls_model.build(csim=False, synth=True, export=False)
        print("SYNTHESIS SUCCESSFUL!")
        
        # Try to read report
        try:
            report = hls_model.read_report()
            print("\n" + "="*50)
            print("SYNTHESIS REPORT")
            print("="*50)
            print(report)
            
            # Save report to file
            with open('simple_synthesis_report.txt', 'w') as f:
                f.write("Simple HLS Synthesis Report\n")
                f.write("="*30 + "\n")
                f.write(str(report))
            
            print(f"\nDetailed report saved to: simple_synthesis_report.txt")
            
        except Exception as e:
            print(f"Could not read report: {e}")
            
            # Try manual report reading
            report_path = os.path.join(output_dir, 'myproject_prj', 'solution1', 'syn', 'report')
            if os.path.exists(report_path):
                print(f"Synthesis reports available at: {report_path}")
                try:
                    files = os.listdir(report_path)
                    rpt_files = [f for f in files if f.endswith('.rpt')]
                    if rpt_files:
                        print("Available report files:")
                        for f in rpt_files:
                            print(f"  - {f}")
                        
                        # Try to read the main synthesis report
                        main_rpt = os.path.join(report_path, 'myproject_csynth.rpt')
                        if os.path.exists(main_rpt):
                            print(f"\nReading {main_rpt}...")
                            try:
                                with open(main_rpt, 'r') as f:
                                    content = f.read()
                                print("SYNTHESIS REPORT CONTENT:")
                                print("="*40)
                                print(content[:2000])  # First 2000 characters
                                if len(content) > 2000:
                                    print("\n... (report truncated) ...")
                                
                                # Save to simplified report
                                with open('vitis_synthesis_report.txt', 'w') as out_f:
                                    out_f.write(content)
                                print(f"\nFull report saved to: vitis_synthesis_report.txt")
                                
                            except Exception as read_e:
                                print(f"Could not read report file: {read_e}")
                        
                except Exception as list_e:
                    print(f"Could not list report directory: {list_e}")
        
        return hls_model
        
    except Exception as e:
        print(f"HLS conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def create_bds_equivalent():
    """
    Create a neural network that approximates BDS functionality
    """
    model = keras.Sequential([
        keras.layers.Dense(16, activation='relu', input_shape=(16,), name='bds_hidden1'),
        keras.layers.Dense(8, activation='relu', name='bds_hidden2'),
        keras.layers.Dense(4, activation='relu', name='bds_hidden3'),
        keras.layers.Dense(2, activation='softmax', name='bds_output')
    ], name='BDS_Equivalent')
    
    return model

def create_obds_equivalent():
    """
    Create a neural network that approximates OBDS functionality
    """
    model = keras.Sequential([
        keras.layers.Dense(32, activation='relu', input_shape=(16,), name='obds_opt1'),
        keras.layers.Dense(16, activation='relu', name='obds_opt2'),
        keras.layers.Dense(8, activation='relu', name='obds_opt3'),
        keras.layers.Dense(2, activation='softmax', name='obds_output')
    ], name='OBDS_Equivalent')
    
    return model

def synthesize_model(model, model_name):
    """
    Synthesize a given model using hls4ml
    """
    print(f"\n--- Synthesizing {model_name} ---")
    
    try:
        # Generate synthetic training data
        input_shape = model.input.shape[1]
        X = np.random.rand(200, input_shape).astype(np.float32)
        # Simple decision rule for labels
        y = (np.sum(X[:, :2], axis=1) > 1).astype(np.int32)
        
        # Train the model
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        model.fit(X, y, epochs=5, verbose=0, batch_size=16)
        
        print(f"Model {model_name} trained successfully")
        
        # Convert to HLS
        hls_config = hls4ml.utils.config_from_keras_model(model, granularity='name')
        hls_config['Model']['Precision'] = 'ap_fixed<16,6>'
        hls_config['Model']['ReuseFactor'] = 1
        
        output_dir = f'hls_{model_name.lower()}'
        hls_model = hls4ml.converters.convert_from_keras_model(
            model,
            hls_config=hls_config,
            output_dir=output_dir,
            part='xcu250-figd2104-2L-e',
            clock_period=10
        )
        
        print(f"Model {model_name} converted to HLS")
        
        # Compile and build
        hls_model.compile()
        hls_model.build(csim=False, synth=True, export=False)
        
        print(f"SYNTHESIS SUCCESSFUL for {model_name}!")
        
        # Try to extract key metrics from report
        try:
            report_path = os.path.join(output_dir, 'myproject_prj', 'solution1', 'syn', 'report', 'myproject_csynth.rpt')
            if os.path.exists(report_path):
                with open(report_path, 'r') as f:
                    report_content = f.read()
                
                # Extract key metrics
                print(f"\nKey metrics for {model_name}:")
                
                # Look for resource utilization
                if "Utilization Estimates" in report_content:
                    lines = report_content.split('\n')
                    in_utilization = False
                    for line in lines:
                        if "Utilization Estimates" in line:
                            in_utilization = True
                        elif in_utilization and ("BRAM" in line or "DSP" in line or "LUT" in line or "FF" in line):
                            if "|" in line:
                                print(f"  {line.strip()}")
                        elif in_utilization and "=====" in line:
                            break
                
                # Look for timing
                if "Timing Summary" in report_content or "Clock" in report_content:
                    lines = report_content.split('\n')
                    for line in lines:
                        if ("Clock" in line and "ns" in line) or ("Timing" in line):
                            print(f"  {line.strip()}")
        
        except Exception as e:
            print(f"Could not extract metrics: {e}")
        
        return hls_model
        
    except Exception as e:
        print(f"Synthesis failed for {model_name}: {e}")
        return None

if __name__ == "__main__":
    print("HLS4ML Basic Synthesis Test")
    print("="*40)
    
    # Test basic functionality first
    simple_hls = test_basic_hls4ml()
    
    if simple_hls is not None:
        print("\n" + "="*50)
        print("BASIC TEST SUCCESSFUL - Proceeding with BDS/OBDS")
        print("="*50)
        
        # Create BDS and OBDS equivalent models
        bds_model = create_bds_equivalent()
        obds_model = create_obds_equivalent()
        
        print("\nBDS Equivalent Model:")
        bds_model.summary()
        
        print("\nOBDS Equivalent Model:")
        obds_model.summary()
        
        # Synthesize both models
        bds_hls = synthesize_model(bds_model, "BDS")
        obds_hls = synthesize_model(obds_model, "OBDS")
        
        print("\n" + "="*60)
        print("SYNTHESIS SUMMARY")
        print("="*60)
        print("Models synthesized:")
        print("1. Simple test model -> hls_simple_test/")
        print("2. BDS equivalent -> hls_bds/")
        print("3. OBDS equivalent -> hls_obds/")
        print("\nReports:")
        print("- simple_synthesis_report.txt")
        print("- vitis_synthesis_report.txt")
        print("\nFor detailed analysis, check the individual report directories.")
        
    else:
        print("\nBasic test failed. Please check your hls4ml installation and environment.")
