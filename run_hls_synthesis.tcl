# Vitis HLS 2023.2 synthesis script for BDS/OBDS models
# Usage: vitis_hls -f run_hls_synthesis.tcl

# BDS Model Synthesis
open_project hls_output_bds_model/myproject_prj -reset
set_top myproject
add_files hls_output_bds_model/firmware/myproject.cpp
add_files -tb hls_output_bds_model/tb_data/tb_input_features.dat
add_files -tb hls_output_bds_model/tb_data/tb_output_predictions.dat
open_solution "solution1" -flow_target vivado -reset
set_part {xcu250-figd2104-2L-e}
create_clock -period 5 -name default
config_export -format ip_catalog -rtl verilog
config_compile -name_max_length 80
csynth_design
export_design -format ip_catalog
close_project

# OBDS Model Synthesis  
open_project hls_output_obds_model/myproject_prj -reset
set_top myproject
add_files hls_output_obds_model/firmware/myproject.cpp
add_files -tb hls_output_obds_model/tb_data/tb_input_features.dat
add_files -tb hls_output_obds_model/tb_data/tb_output_predictions.dat
open_solution "solution1" -flow_target vivado -reset
set_part {xcu250-figd2104-2L-e}
create_clock -period 5 -name default
config_export -format ip_catalog -rtl verilog
config_compile -name_max_length 80
csynth_design
export_design -format ip_catalog
close_project

puts "Synthesis completed for both BDS and OBDS models"
puts "Reports available at:"
puts "  BDS: hls_output_bds_model/myproject_prj/solution1/syn/report/"
puts "  OBDS: hls_output_obds_model/myproject_prj/solution1/syn/report/"

exit
