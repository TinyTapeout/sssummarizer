# sssummarizer

https://TinyTapeout.com cell summary tool

Makes nice markdown tables that summarize the cell usage of an ASIC design by reading its 
gate level verilog netlist.

# Usage

Print a markdown table of all cells with link to docs, description & cell count:

    sssummarizer --gl gate_level_verilog.v --print-summary

Print a markdown table of all cell categories with counts:

    sssummarizer --gl gate_level_verilog.v --print-category

Create the [defs.json](defs.json) file, only if using a different PDK to Sky130:

    sssummarizer --create-defs sky130_repo_directory

# Categories

See [tags.json](tags.json), for categories and my classification of the PDK.

      AND
      OR
      NAND
      NOR
      Clock
      Flip Flops
      Multiplexer
      Latch
      Inverter
      Buffer
      Fill
      Tap
      Diode
      Combo Logic
      Misc

# License

See [LICENSE](LICENSE)
