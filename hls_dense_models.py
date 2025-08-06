"""
Standard Keras Layer Implementation for HLS-Compatible BDS and OBDS Functions
Uses only hls4ml-supported layer types
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import hls4ml

# Fixed constants for HLS synthesis
MAX_TREES = 100
MAX_FEATURES = 16
MAX_TERMS = 8
MAX_DEPTH = 8
N_CLASSES = 2

def create_bds_dense_model():
    """
    Create BDS model using only Dense layers (fully supported by hls4ml)
    """
    inputs = keras.Input(shape=(MAX_FEATURES,), dtype='float32', name='bds_input')
    
    # Hidden layers for decision logic
    x = keras.layers.Dense(32, activation='relu', name='hidden_1')(inputs)
    x = keras.layers.Dense(16, activation='relu', name='hidden_2')(x)
    x = keras.layers.Dense(8, activation='relu', name='hidden_3')(x)
    
    # Output layer for binary classification
    outputs = keras.layers.Dense(N_CLASSES, activation='softmax', name='output')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='BDS_Dense_Model')
    return model

def create_obds_dense_model():
    """
    Create OBDS model using only Dense layers
    """
    inputs = keras.Input(shape=(MAX_FEATURES,), dtype='float32', name='obds_input')
    
    # Larger network to capture optimization logic
    x = keras.layers.Dense(64, activation='relu', name='opt_layer_1')(inputs)
    x = keras.layers.Dense(32, activation='relu', name='opt_layer_2')(x)
    x = keras.layers.Dense(16, activation='relu', name='opt_layer_3')(x)
    x = keras.layers.Dense(8, activation='relu', name='opt_layer_4')(x)
    
    # Output for binary classification
    outputs = keras.layers.Dense(N_CLASSES, activation='softmax', name='output')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='OBDS_Dense_Model')
    return model

def create_minimal_bds_model():
    """
    Create a minimal BDS model for testing
    """
    inputs = keras.Input(shape=(4,), dtype='float32', name='minimal_bds_input')
    
    # Very simple network
    x = keras.layers.Dense(8, activation='relu', name='simple_hidden')(inputs)
    outputs = keras.layers.Dense(2, activation='softmax', name='simple_output')(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='Minimal_BDS_Model')
    return model

def synthesize_dense_model(model, model_name="dense_model", target_device="xcu250-figd2104-2L-e"):
    """
    Convert Dense model to HLS and generate synthesis report
    """
    print(f"Converting {model_name} to HLS...")
    
    try:
        # Generate hls4ml config
        config = hls4ml.utils.config_from_keras_model(model, granularity='model')
        
        # Configure for optimal synthesis
        config['Model']['Precision'] = 'ap_fixed<16,8>'
        config['Model']['ReuseFactor'] = 1
        config['Model']['Strategy'] = 'Latency'
        
        # Set layer-specific configurations
        for layer in model.layers:
            if hasattr(layer, 'name') and layer.name != model.input.name.split('/')[0]:
                if layer.name not in config['LayerName']:
                    config['LayerName'][layer.name] = {}
                config['LayerName'][layer.name]['Precision'] = 'ap_fixed<16,8>'
                config['LayerName'][layer.name]['ReuseFactor'] = 1
        
        print("Configuration created successfully")
        
        # Convert model
        output_dir = f'hls_output_{model_name}'
        hls_model = hls4ml.converters.convert_from_keras_model(
            model,
            hls_config=config,
            output_dir=output_dir,
            part=target_device,
            clock_period=5,
            io_type='io_parallel'
        )
        
        print("Model converted to HLS successfully")
        
        # Compile the model
        hls_model.compile()
        print("HLS model compiled successfully")
        
        # Build with synthesis
        try:
            print("Starting synthesis...")
            hls_model.build(csim=False, synth=True, export=False, vsynth=False)
            print(f"Synthesis completed successfully for {model_name}!")
            
            # Try to get synthesis report
            try:
                report_dict = hls_model.read_report()
                print(f"\n=== SYNTHESIS REPORT for {model_name.upper()} ===")
                if isinstance(report_dict, dict):
                    for key, value in report_dict.items():
                        print(f"{key}: {value}")
                else:
                    print(report_dict)
                
                # Save individual report
                with open(f'{model_name}_synthesis_report.txt', 'w') as f:
                    f.write(f"Synthesis Report for {model_name}\n")
                    f.write("=" * 40 + "\n")
                    if isinstance(report_dict, dict):
                        for key, value in report_dict.items():
                            f.write(f"{key}: {value}\n")
                    else:
                        f.write(str(report_dict))
                
                print(f"Detailed report saved to: {model_name}_synthesis_report.txt")
                
            except Exception as e:
                print(f"Could not read synthesis report: {e}")
                print(f"Check the report manually at: {output_dir}/myproject_prj/solution1/syn/report/")
                
        except Exception as e:
            print(f"Synthesis failed for {model_name}: {e}")
            print("This might be due to Vitis HLS not being installed or configured properly.")
        
        return hls_model
        
    except Exception as e:
        print(f"Error in HLS conversion for {model_name}: {e}")
        return None

def train_simple_models():
    """
    Train the models with simple synthetic data to give them realistic weights
    """
    print("Training models with synthetic data...")
    
    # Generate synthetic training data
    n_samples = 1000
    
    # BDS training data
    X_bds = np.random.rand(n_samples, MAX_FEATURES).astype(np.float32)
    # Simple decision rule: class 1 if first two features sum > 1
    y_bds = (X_bds[:, 0] + X_bds[:, 1] > 1).astype(np.int32)
    y_bds_categorical = keras.utils.to_categorical(y_bds, N_CLASSES)
    
    # Minimal BDS training data (4 features)
    X_minimal = np.random.rand(n_samples, 4).astype(np.float32)
    y_minimal = (X_minimal[:, 0] + X_minimal[:, 1] > 1).astype(np.int32)
    y_minimal_categorical = keras.utils.to_categorical(y_minimal, N_CLASSES)
    
    # Create and train models
    bds_model = create_bds_dense_model()
    bds_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    obds_model = create_obds_dense_model()
    obds_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    minimal_model = create_minimal_bds_model()
    minimal_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    print("Training BDS model...")
    bds_model.fit(X_bds, y_bds_categorical, epochs=5, batch_size=32, verbose=0)
    
    print("Training OBDS model...")
    obds_model.fit(X_bds, y_bds_categorical, epochs=5, batch_size=32, verbose=0)
    
    print("Training minimal model...")
    minimal_model.fit(X_minimal, y_minimal_categorical, epochs=5, batch_size=32, verbose=0)
    
    print("Models trained successfully")
    
    return bds_model, obds_model, minimal_model

if __name__ == "__main__":
    print("Creating and testing HLS-compatible models with Dense layers...")
    
    # Train models first
    bds_model, obds_model, minimal_model = train_simple_models()
    
    print("\nModel summaries:")
    print("\nBDS Model:")
    bds_model.summary()
    
    print("\nOBDS Model:")  
    obds_model.summary()
    
    print("\nMinimal Model:")
    minimal_model.summary()
    
    # Test predictions
    print("\nTesting model predictions...")
    test_data = np.random.rand(5, MAX_FEATURES).astype(np.float32)
    test_data_minimal = np.random.rand(5, 4).astype(np.float32)
    
    bds_pred = bds_model.predict(test_data, verbose=0)
    obds_pred = obds_model.predict(test_data, verbose=0)
    minimal_pred = minimal_model.predict(test_data_minimal, verbose=0)
    
    print(f"BDS predictions shape: {bds_pred.shape}")
    print(f"OBDS predictions shape: {obds_pred.shape}")
    print(f"Minimal predictions shape: {minimal_pred.shape}")
    
    # Synthesize models
    print("\n" + "="*60)
    print("STARTING HLS SYNTHESIS")
    print("="*60)
    
    # Start with minimal model (most likely to succeed)
    print("\n--- Minimal Model Synthesis ---")
    minimal_hls = synthesize_dense_model(minimal_model, "minimal_bds")
    
    print("\n--- BDS Model Synthesis ---")  
    bds_hls = synthesize_dense_model(bds_model, "bds_dense")
    
    print("\n--- OBDS Model Synthesis ---")
    obds_hls = synthesize_dense_model(obds_model, "obds_dense")
    
    print("\n" + "="*60)
    print("SYNTHESIS COMPLETED")
    print("="*60)
    print("\nCheck the generated directories and report files:")
    print("- hls_output_minimal_bds/")
    print("- hls_output_bds_dense/")
    print("- hls_output_obds_dense/")
    print("\nIndividual reports:")
    print("- minimal_bds_synthesis_report.txt")
    print("- bds_dense_synthesis_report.txt")  
    print("- obds_dense_synthesis_report.txt")
