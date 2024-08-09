# MHTCET Cutoff PDF to Excel Converter

## Overview
This Python project scrapes raw PDF data containing MHT CET college and branch cutoffs, extracts the relevant information, and creates a JSON file. Additionally, it generates a "skipped" folder with `pageNo.txt` files for lines that couldn't be understood and are excluded from the JSON data. The final output is an Excel file (`output.xlsx`) containing organized cutoff data.

## Usage
1. Run `main.py`.
2. Provide the path to the MHT CET cutoff PDF file.
3. This will create data.json file
4. Next, run `DataMigrater.py` to create the final(`output.xlsx`) Excel file.

## Requirements
### Linux (Debian-based distributions)
```bash
sudo apt-get update
sudo apt-get install python3-pip
pip3 install pypdf openpyxl
```

### Windows
1. Install Python 3.x from the official website: [Python Downloads](https://www.python.org/downloads/).
2. Open a command prompt (cmd) or PowerShell.
3. Run the following commands:
   ```bash
   pip install pypdf openpyxl
   ```

### macOS
1. Install Python 3.x (if not already installed) using Homebrew or the official website.
2. Open Terminal.
3. Run the following commands:
   ```bash
   pip3 install pypdf openpyxl
   ```

Feel free to contribute or report issues on GitHub!

## Sample Data and Output

The `out` folder in this repository contains the following files:

1. **Sample PDF (2023 CET CAP Round 1 Cut-off):** You can find the raw PDF file containing MHT CET college and branch cutoffs for the 2023 CAP Round 1. This is the input file that the Python program processes.

2. **Final Output (output.xlsx):** After running the `main.py` script and executing the data extraction process, the program generates an Excel file named `output.xlsx`. This file contains organized and structured cutoff data for colleges and branches.
