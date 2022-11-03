# sssummarizer

https://TinyTapeout.com cell summary tool

Makes nice markdown tables that summarize the cell usage of an ASIC design by reading its 
gate level verilog netlist.

The tags.json file was created by hand.

# Usage

print a markdown table of all cells with link to docs, description & cell count

    sssummarizer --gl gate_level_verilog.v --print-summary

print a markdown table of all cells categories with counts

    sssummarizer --gl gate_level_verilog.v --print-category

create the defs file

    sssummarizer --create-defs sky130_repo_directory

# License

See [LICENSE](LICENSE)
