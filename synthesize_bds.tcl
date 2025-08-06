# Vitis HLS 2023.2 Synthesis Script for BDS Model
# This script performs complete synthesis and generates detailed reports

# Create and open BDS project
open_project hls_simple_bds_synthesis -reset
set_top myproject

# Add source files
add_files hls_simple_bds/firmware/myproject.cpp
add_files hls_simple_bds/firmware/myproject.h
add_files hls_simple_bds/firmware/defines.h
add_files hls_simple_bds/firmware/parameters.h

# Add testbench files (if available)
if {[file exists hls_simple_bds/tb_data]} {
    add_files -tb hls_simple_bds/tb_data/ -cflags "-Ihls_simple_bds/firmware"
}

# Open solution with target device
open_solution "solution1" -flow_target vivado -reset
set_part {xcu250-figd2104-2L-e}

# Set clock period (10ns = 100MHz)
create_clock -period 10 -name default

# Configuration for export
config_export -format ip_catalog -rtl verilog -version "1.0.0"
config_compile -name_max_length 80

# Run C synthesis
puts "Starting C synthesis for BDS model..."
csynth_design

# Export design as IP
export_design -format ip_catalog

# Generate reports
puts "BDS Synthesis completed!"
puts "Reports available at: hls_simple_bds_synthesis/solution1/syn/report/"

close_project
