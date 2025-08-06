"""
Setup and Synthesis Script for HLS-Compatible BDS/OBDS Funct        print(f"[OK] Created test data: {n_samples} samples, {n_features} features")ons
This script sets up the environment and runs the complete synthesis flow
"""

import os
import subprocess
import sys
import numpy as np

# Import constants from hls_bds_obds
from hls_bds_obds import MAX_FEATURES, MAX_TREES, MAX_TERMS, MAX_DEPTH, N_CLASSES

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    try:
        import tensorflow as tf
        print(f"[OK] TensorFlow version: {tf.__version__}")
        if tf.__version__.startswith('2.13'):
            print("[OK] TensorFlow 2.13 - Compatible with hls4ml")
        else:
            print("[WARN] Warning: TensorFlow version may not be optimal for hls4ml")
    except ImportError:
        print("[ERROR] TensorFlow not found")
        return False
    
    try:
        import keras
        print(f"[OK] Keras version: {keras.__version__}")
    except ImportError:
        print("[ERROR] Keras not found")
        return False
    
    try:
        import hls4ml
        print(f"[OK] hls4ml version: {hls4ml.__version__}")
    except ImportError:
        print("[ERROR] hls4ml not found")
        return False
    
    try:
        import qkeras
        print(f"[OK] QKeras available")
    except ImportError:
        print("[WARN] QKeras not found (optional for some features)")
    
    return True

def create_test_data():
    """Create test data for validation"""
    print("\nGenerating test data...")
    
    # Create test input data
    n_samples = 100
    n_features = 16
    
    # Random test features
    test_features = np.random.rand(n_samples, n_features).astype(np.float32)
    
    # Random binary features for boolean operations
    test_binary_features = (np.random.rand(n_samples, n_features) > 0.5).astype(np.uint8)
    
    # Save test data
    np.save('test_features.npy', test_features)
    np.save('test_binary_features.npy', test_binary_features)
    
    print(f"✅ Created test data: {n_samples} samples, {n_features} features")
    return test_features, test_binary_features

def run_synthesis():
    """Run the HLS synthesis process"""
    print("\n" + "="*60)
    print("STARTING HLS SYNTHESIS PROCESS")
    print("="*60)
    
    try:
        # Import and run the HLS synthesis
        from hls_bds_obds import (
            create_bds_keras_model, 
            create_obds_keras_model, 
            synthesize_with_hls4ml,
            HLS_BDS_Functions,
            HLS_OBDS_Functions
        )
        
        print("\n1. Creating Keras models...")
        bds_model = create_bds_keras_model()
        obds_model = create_obds_keras_model()
        
        print("[OK] Models created successfully")
        
        print("\n2. Testing models with sample data...")
        test_features, test_binary_features = create_test_data()
        
        # Test BDS model
        dummy_bds_input = np.random.rand(10, MAX_FEATURES).astype(np.float32)
        bds_predictions = bds_model.predict(dummy_bds_input, verbose=0)
        print(f"[OK] BDS model test - predictions shape: {bds_predictions.shape}")
        
        # Test OBDS model
        dummy_obds_input = np.random.rand(10, 16).astype(np.float32)
        obds_predictions = obds_model.predict(dummy_obds_input, verbose=0)
        print(f"[OK] OBDS model test - predictions shape: {obds_predictions.shape}")
        
        print("\n3. Converting to HLS...")
        
        # Synthesize BDS model
        print("\n--- BDS Model Synthesis ---")
        bds_hls_model = synthesize_with_hls4ml(bds_model, "bds_model")
        
        # Synthesize OBDS model
        print("\n--- OBDS Model Synthesis ---")
        obds_hls_model = synthesize_with_hls4ml(obds_model, "obds_model")
        
        print("\n4. Testing HLS-specific functions...")
        
        # Test HLS-compatible functions directly
        print("\nTesting HLS_BDS_Functions...")
        thresholds = np.random.rand(100, 8).astype(np.float32)
        tree_features = np.random.randint(0, 16, (100, 8)).astype(np.int32)
        tree_values = np.random.rand(100, 8).astype(np.float32)
        
        bds_direct_predictions = HLS_BDS_Functions.fixed_size_bds_predict(
            test_features[:10], thresholds, tree_features, tree_values, n_samples=10
        )
        print(f"[OK] Direct BDS predictions: {bds_direct_predictions}")
        
        print("\nTesting HLS_OBDS_Functions...")
        cluster_centers = np.random.rand(16, 4).astype(np.float32)
        feature_masks = np.ones(16, dtype=np.uint8)
        
        optimized_features = HLS_OBDS_Functions.fixed_cluster_optimization(
            test_features[:10], cluster_centers, feature_masks
        )
        print(f"[OK] Optimized features shape: {optimized_features.shape}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Synthesis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_synthesis_report():
    """Generate a comprehensive synthesis report"""
    print("\n" + "="*60)
    print("SYNTHESIS REPORT GENERATION")
    print("="*60)
    
    report_content = []
    report_content.append("HLS Synthesis Report for BDS/OBDS Functions")
    report_content.append("=" * 50)
    report_content.append("")
    
    # Check for generated directories
    output_dirs = ['hls_output_bds_model', 'hls_output_obds_model']
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            report_content.append(f"[OK] Generated HLS project: {output_dir}")
            
            # Look for synthesis reports
            report_path = os.path.join(output_dir, 'myproject_prj', 'solution1', 'syn', 'report')
            if os.path.exists(report_path):
                report_content.append(f"[OK] Synthesis report directory: {report_path}")
                
                # List report files
                try:
                    report_files = os.listdir(report_path)
                    for file in report_files:
                        if file.endswith('.rpt'):
                            report_content.append(f"   FILE: {file}")
                except:
                    report_content.append("   (Unable to list report files)")
            else:
                report_content.append(f"[WARN] Synthesis report not found at: {report_path}")
        else:
            report_content.append(f"[ERROR] HLS project not generated: {output_dir}")
    
    report_content.append("")
    report_content.append("Key Features of HLS-Compatible Implementation:")
    report_content.append("- Fixed-size arrays for deterministic memory usage")
    report_content.append("- Bitwise operations for boolean logic")
    report_content.append("- Bounded loops for synthesis optimization")
    report_content.append("- TensorFlow/Keras model wrappers for hls4ml compatibility")
    report_content.append("- Support for Xilinx Vitis HLS 2023.2")
    report_content.append("")
    
    report_content.append("Next Steps:")
    report_content.append("1. Review synthesis reports in the generated directories")
    report_content.append("2. Run 'vitis_hls -f run_hls_synthesis.tcl' for detailed synthesis")
    report_content.append("3. Implement in Vivado for full FPGA deployment")
    report_content.append("")
    
    # Save report with proper encoding
    with open('synthesis_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))
    
    # Print report
    for line in report_content:
        print(line)
    
    print(f"[FILE] Full report saved to: synthesis_report.txt")

def main():
    """Main execution function"""
    print("HLS BDS/OBDS Setup and Synthesis Tool")
    print("="*40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n[ERROR] Please install missing dependencies first")
        print("Run: pip install tensorflow==2.13 keras==2.13 qkeras numpy hls4ml")
        return False
    
    # Run synthesis
    synthesis_success = run_synthesis()
    
    # Generate report
    generate_synthesis_report()
    
    if synthesis_success:
        print("\n[SUCCESS] Setup and synthesis completed successfully!")
        print("\nTo run Vitis HLS synthesis (if Vitis is installed):")
        print("   vitis_hls -f run_hls_synthesis.tcl")
    else:
        print("\n[WARN] Setup completed with some issues. Check the logs above.")
    
    return synthesis_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
