## Ground RISE Camp

This repository contains a small data file (`data.txt`) as well as a simple Python transformation script (`column_splitter.py`). The input data is currently a single column with three distinct values. The Python transformation script takes in the input file and splits it up into three separate columns. 

The `column_splitter.py` script is also instrumented to automatically publish lineage information to Ground. It creates a node & node version for the newly created and dataset and links the original dataset to the new via a lineage edge.