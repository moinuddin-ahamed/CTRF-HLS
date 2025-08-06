"""
HLS-Compatible BDS and OBDS Functions for hls4ml synthesis
Refactored to use fixed-size arrays and bitwise operations
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

class HLS_BDS_Functions:
    """
    HLS-compatible BDS (Binary Decision System) functions
    Using fixed-size arrays and bitwise operations
    """
    
    @staticmethod
    def fixed_size_bds_predict(features, thresholds, tree_features, tree_values, n_samples=100):
        """
        Fixed-size BDS prediction function compatible with HLS synthesis
        
        Args:
            features: Input features array [n_samples, MAX_FEATURES] (dtype: float32)
            thresholds: Decision thresholds [MAX_TREES, MAX_DEPTH] (dtype: float32)
            tree_features: Feature indices for each tree node [MAX_TREES, MAX_DEPTH] (dtype: int32)
            tree_values: Decision values [MAX_TREES, MAX_DEPTH] (dtype: float32)
            
        Returns:
            predictions: Class predictions [n_samples] (dtype: int32)
        """
        predictions = np.zeros(n_samples, dtype=np.int32)
        
        for sample_idx in range(n_samples):
            class_votes = np.zeros(N_CLASSES, dtype=np.int32)
            
            # Process each tree
            for tree_idx in range(MAX_TREES):
                # Traverse tree to get leaf prediction
                node_idx = 0
                
                # Fixed depth traversal (unrolled for HLS)
                for depth in range(MAX_DEPTH):
                    if node_idx < MAX_DEPTH:  # Bounds check
                        feature_idx = tree_features[tree_idx, node_idx]
                        threshold = thresholds[tree_idx, node_idx]
                        
                        # Bitwise comparison for HLS efficiency
                        if feature_idx < MAX_FEATURES:
                            if features[sample_idx, feature_idx] > threshold:
                                node_idx = 2 * node_idx + 1  # Left child
                            else:
                                node_idx = 2 * node_idx + 2  # Right child
                        else:
                            break  # Leaf node reached
                
                # Get leaf class prediction (simplified)
                leaf_class = tree_values[tree_idx, min(node_idx, MAX_DEPTH-1)].astype(np.int32)
                if 0 <= leaf_class < N_CLASSES:
                    class_votes[leaf_class] += 1
            
            # Majority vote using bitwise operations
            max_votes = 0
            predicted_class = 0
            for class_idx in range(N_CLASSES):
                if class_votes[class_idx] > max_votes:
                    max_votes = class_votes[class_idx]
                    predicted_class = class_idx
            
            predictions[sample_idx] = predicted_class
        
        return predictions

    @staticmethod 
    def bitwise_boolean_evaluation(features, boolean_terms, term_weights):
        """
        Evaluate boolean expressions using bitwise operations
        
        Args:
            features: Binary feature array [n_samples, MAX_FEATURES] (dtype: uint8)
            boolean_terms: Boolean term definitions [MAX_TERMS, MAX_FEATURES] (dtype: uint8)
            term_weights: Weights for each term [MAX_TERMS] (dtype: float32)
            
        Returns:
            result: Boolean evaluation result [n_samples] (dtype: uint8)
        """
        n_samples = features.shape[0]
        results = np.zeros(n_samples, dtype=np.uint8)
        
        for sample_idx in range(n_samples):
            term_results = np.zeros(MAX_TERMS, dtype=np.uint8)
            
            # Evaluate each boolean term
            for term_idx in range(MAX_TERMS):
                term_value = np.uint8(1)  # Initialize as True
                
                # AND operation across features in the term
                for feature_idx in range(MAX_FEATURES):
                    if boolean_terms[term_idx, feature_idx] > 0:
                        # Positive literal
                        term_value &= features[sample_idx, feature_idx]
                    elif boolean_terms[term_idx, feature_idx] < 0:
                        # Negative literal (NOT operation)
                        term_value &= (~features[sample_idx, feature_idx] & np.uint8(1))
                
                term_results[term_idx] = term_value
            
            # OR operation across terms (Sum of Products)
            final_result = np.uint8(0)
            for term_idx in range(MAX_TERMS):
                final_result |= term_results[term_idx]
            
            results[sample_idx] = final_result
        
        return results


class HLS_OBDS_Functions:
    """
    HLS-compatible OBDS (Optimized Binary Decision System) functions
    """
    
    @staticmethod
    def fixed_cluster_optimization(features, cluster_centers, feature_masks):
        """
        Fixed-size clustering optimization for OBDS
        
        Args:
            features: Input features [n_samples, MAX_FEATURES] (dtype: float32)
            cluster_centers: Cluster center values [MAX_FEATURES, 4] (dtype: float32)
            feature_masks: Binary masks for feature selection [MAX_FEATURES] (dtype: uint8)
            
        Returns:
            optimized_features: Optimized feature values [n_samples, MAX_FEATURES] (dtype: float32)
        """
        n_samples = features.shape[0]
        optimized_features = features.copy()
        
        for sample_idx in range(n_samples):
            for feature_idx in range(MAX_FEATURES):
                if feature_masks[feature_idx] > 0:
                    # Find closest cluster center
                    min_distance = np.float32(1e6)
                    closest_center = features[sample_idx, feature_idx]
                    
                    for center_idx in range(4):  # Fixed number of clusters
                        distance = abs(features[sample_idx, feature_idx] - 
                                     cluster_centers[feature_idx, center_idx])
                        if distance < min_distance:
                            min_distance = distance
                            closest_center = cluster_centers[feature_idx, center_idx]
                    
                    optimized_features[sample_idx, feature_idx] = closest_center
        
        return optimized_features

    @staticmethod
    def reduce_redundancy(boolean_matrix, threshold=0.5):
        """
        Remove redundant boolean terms using fixed-size operations
        
        Args:
            boolean_matrix: Boolean term matrix [MAX_TERMS, MAX_FEATURES] (dtype: uint8)
            threshold: Similarity threshold for redundancy detection (dtype: float32)
            
        Returns:
            reduced_matrix: Matrix with redundant terms removed [MAX_TERMS, MAX_FEATURES] (dtype: uint8)
            reduction_mask: Binary mask indicating kept terms [MAX_TERMS] (dtype: uint8)
        """
        reduced_matrix = boolean_matrix.copy()
        reduction_mask = np.ones(MAX_TERMS, dtype=np.uint8)
        
        # Pairwise comparison of terms
        for i in range(MAX_TERMS):
            if reduction_mask[i] == 0:
                continue
                
            for j in range(i + 1, MAX_TERMS):
                if reduction_mask[j] == 0:
                    continue
                
                # Calculate similarity using bitwise operations
                matches = np.uint8(0)
                total = np.uint8(0)
                
                for k in range(MAX_FEATURES):
                    if boolean_matrix[i, k] != 0 or boolean_matrix[j, k] != 0:
                        total += 1
                        if boolean_matrix[i, k] == boolean_matrix[j, k]:
                            matches += 1
                
                # Check similarity threshold
                if total > 0 and (matches / total) > threshold:
                    reduction_mask[j] = 0  # Mark as redundant
                    # Zero out the redundant row
                    for k in range(MAX_FEATURES):
                        reduced_matrix[j, k] = 0
        
        return reduced_matrix, reduction_mask


def create_bds_keras_model():
    """
    Create a Keras model wrapper for BDS function (hls4ml compatible)
    """
    def bds_layer(inputs):
        # Extract features from input tensor (simplified version)
        features = inputs[:, :MAX_FEATURES]  # First 16 features
        
        # Simplified BDS logic using fixed operations
        # Binary comparisons with fixed thresholds
        feature_0 = features[:, 0]  # First feature
        feature_1 = features[:, 1]  # Second feature
        
        # Fixed threshold comparisons
        decision_0 = tf.cast(feature_0 > 0.5, tf.float32)
        decision_1 = tf.cast(feature_1 > 0.3, tf.float32)
        
        # Combine decisions (simplified voting)
        class_0_score = (1.0 - decision_0) * (1.0 - decision_1)  # Both below threshold
        class_1_score = decision_0 + decision_1  # At least one above threshold
        
        # Normalize scores
        total_score = class_0_score + class_1_score
        class_0_score = class_0_score / (total_score + 1e-7)
        class_1_score = class_1_score / (total_score + 1e-7)
        
        # Stack scores and return argmax
        class_scores = tf.stack([class_0_score, class_1_score], axis=1)
        return tf.argmax(class_scores, axis=1, output_type=tf.int32)
    
    # Simplified input - just features for demonstration
    inputs = keras.Input(shape=(MAX_FEATURES,), dtype='float32', name='bds_input')
    outputs = keras.layers.Lambda(bds_layer, name='bds_logic')(inputs)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='BDS_Model')
    return model


def create_obds_keras_model():
    """
    Create a Keras model wrapper for OBDS function (hls4ml compatible)
    """
    def obds_layer(inputs):
        # Extract features
        features = inputs[:, :MAX_FEATURES]
        
        # Simplified OBDS logic
        # Apply fixed clustering and optimization
        optimized = features  # Placeholder for actual optimization
        
        # Boolean term evaluation (simplified)
        term_1 = tf.cast(optimized[:, 0] > 0.5, tf.float32)
        term_2 = tf.cast(optimized[:, 1] > 0.5, tf.float32)
        term_3 = tf.cast(optimized[:, 2] > 0.5, tf.float32)
        
        # Combine terms with bitwise OR (using addition and clipping)
        result = tf.clip_by_value(term_1 + term_2 + term_3, 0.0, 1.0)
        
        # Convert to class prediction
        class_0_score = 1.0 - result
        class_1_score = result
        
        class_scores = tf.stack([class_0_score, class_1_score], axis=1)
        return tf.argmax(class_scores, axis=1, output_type=tf.int32)
    
    inputs = keras.Input(shape=(MAX_FEATURES,), dtype='float32', name='obds_input')
    outputs = keras.layers.Lambda(obds_layer, name='obds_logic')(inputs)
    
    model = keras.Model(inputs=inputs, outputs=outputs, name='OBDS_Model')
    return model


def synthesize_with_hls4ml(model, model_name="bds_obds_model", target_device="xcu250-figd2104-2L-e"):
    """
    Convert Keras model to HLS and generate synthesis report
    
    Args:
        model: Keras model to synthesize
        model_name: Name for the HLS project
        target_device: FPGA target device
        
    Returns:
        hls_model: Compiled HLS4ML model
    """
    print(f"Converting {model_name} to HLS...")
    
    # Generate hls4ml config
    config = hls4ml.utils.config_from_keras_model(model, granularity='model')
    
    # Configure for optimal synthesis
    config['Model']['Precision'] = 'ap_fixed<16,8>'  # 16-bit fixed point
    config['Model']['ReuseFactor'] = 1
    config['Model']['Strategy'] = 'Latency'  # Optimize for latency
    config['Model']['BramFactor'] = 1000000
    config['Model']['UramFactor'] = 1000000
    
    # Set layer-specific configurations
    for layer in model.layers:
        if hasattr(layer, 'name'):
            config['LayerName'][layer.name] = {
                'Precision': 'ap_fixed<16,8>',
                'ReuseFactor': 1
            }
    
    # Convert model
    output_dir = f'hls_output_{model_name}'
    hls_model = hls4ml.converters.convert_from_keras_model(
        model,
        hls_config=config,
        output_dir=output_dir,
        part=target_device,
        clock_period=5,  # 5ns clock period (200MHz)
        io_type='io_parallel'
    )
    
    print("Compiling HLS model...")
    hls_model.compile()
    
    print("Building HLS project (synthesis)...")
    try:
        # Build with synthesis enabled
        hls_model.build(csim=False, synth=True, export=False, vsynth=False)
        print(f"Synthesis completed successfully for {model_name}!")
        
        # Try to get the synthesis report
        try:
            report = hls_model.read_report()
            print(f"\n=== SYNTHESIS REPORT for {model_name.upper()} ===")
            print(report)
        except Exception as e:
            print(f"Could not read synthesis report automatically: {e}")
            print(f"Check the report manually at: {output_dir}/myproject_prj/solution1/syn/report/")
        
    except Exception as e:
        print(f"Synthesis failed for {model_name}: {e}")
        print("This might be due to Vitis HLS not being installed or configured properly.")
    
    return hls_model


if __name__ == "__main__":
    print("Creating HLS-compatible BDS and OBDS models...")
    
    # Create models
    bds_model = create_bds_keras_model()
    obds_model = create_obds_keras_model()
    
    print("\nBDS Model Summary:")
    bds_model.summary()
    
    print("\nOBDS Model Summary:")
    obds_model.summary()
    
    # Test with dummy data
    print("\nTesting models with dummy data...")
    
    # BDS test
    bds_input_size = MAX_FEATURES + MAX_TREES * MAX_DEPTH
    dummy_bds_input = np.random.rand(1, bds_input_size).astype(np.float32)
    bds_output = bds_model.predict(dummy_bds_input)
    print(f"BDS prediction: {bds_output}")
    
    # OBDS test
    dummy_obds_input = np.random.rand(1, MAX_FEATURES).astype(np.float32)
    obds_output = obds_model.predict(dummy_obds_input)
    print(f"OBDS prediction: {obds_output}")
    
    # Synthesize models
    print("\n" + "="*50)
    print("Starting HLS synthesis...")
    print("="*50)
    
    bds_hls = synthesize_with_hls4ml(bds_model, "bds_model")
    obds_hls = synthesize_with_hls4ml(obds_model, "obds_model")
    
    print("\nSynthesis process completed!")
    print("Check the generated reports in the hls_output_* directories.")
