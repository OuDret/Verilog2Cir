import re
import sys

verilog = "netlist.v"
powerpins = "VSS VDD"

cells = {}

def read_verilog(netlist_path):
    module_pattern = r'module\s+(\w+)\s*\((.*?)\);'
    cell_pattern = r'\b(\w+)\s+_(\w+)_\s*\('
    inout_pattern = r'\.(\w+)\((.*?)\)'
    
    with open(netlist_path, "r") as file:
        for line in file:
            match = re.search(module_pattern, line.strip())
            if (match):
                module_name = match.group(1)
                module_inout = match.group(2).replace(',', '').replace("[","_").replace("]","_")
                module = ".SUBCKT " + module_name + " " + powerpins + " " + module_inout
                print( module )

            elif (line.strip() == "endmodule"):
                print ("\n.ENDS")
 
            match = re.search(cell_pattern, line.strip())
            if (match != None):
                cell_type = match.group(1)
                cell_name = match.group(2).replace("[","_").replace("]","_")
                inout = ""

            match = re.search(inout_pattern, line.strip())
            if (match != None):
                inout += " " + match.group(2).replace("[","_").replace("]","_")

            if (line.strip() == ");"):
                print("X"+cell_name + " " + powerpins + inout + " " + cell_type)

                
def main():
    # read_lib(lib)
    with open('output.cir', 'w') as f:
        sys.stdout = f
        read_verilog(verilog)

main()