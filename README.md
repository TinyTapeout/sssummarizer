# sssummarizer

https://TinyTapeout.com cell summary tool

Makes nice markdown tables that summarize the cell usage of an ASIC design by reading its 
gate level verilog netlist.

# Usage

prints a markdown table of cells, cell count. include description and link for each cell

    sssummarizer --gl gate_level_verilog.v --print-summary

create the mapfile

    sssummarizer --create-defs sky130_repo_directory
