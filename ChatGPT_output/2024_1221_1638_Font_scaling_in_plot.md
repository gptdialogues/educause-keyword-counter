---
title: Font scaling in plot
create_time: 2024-12-21 16:38:47
update_time: 2024-12-21 16:41:48
conversation_id: 67667087-b3ac-800f-aa54-cb51483671e8
---

# Font scaling in plot

Creation Time: 2024-12-21 16:38:47

Update Time: 2024-12-21 16:41:48

## Assistant



## User

Please give the option to specify the rate to magnify the font sizes of the texts in the plot.

~~~ visualize_csv_data.py
#!/usr/bin/env python3

"""
This script visualizes CSV data with a flexible approach to handle multiple columns. It offers options for specifying a starting year and an output filename.

Usage:
    python visualize_csv.py <CSV_FILE> [--start-year YEAR] [--output OUTPUT_FILE] [--ext EXTENSION]
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional

def main():
    parser = argparse.ArgumentParser(description="Visualize CSV data with flexible column support.")
    parser.add_argument("csv_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("--start-year", type=int, default=None, help="Specify the starting year for the plot.")
    parser.add_argument("--output", type=str, default=None, help="Specify the output filename.")
    parser.add_argument("--ext", type=str, choices=["pdf", "png", "jpg"], default="pdf", help="Specify the output image format (default: pdf).")

    args = parser.parse_args()

    # Load the CSV file
    data = pd.read_csv(args.csv_file)

    # Validate CSV structure
    if "Year" not in data.columns:
        raise ValueError("CSV file must have a 'Year' column.")

    # Filter by starting year if specified
    if args.start_year:
        data = data[data["Year"] >= args.start_year]

    # Plot the data
    plt.figure(figsize=(10, 6))
    for column in data.columns:
        if column != "Year":
            plt.plot(data["Year"], data[column], label=column)

    plt.xlabel("Year")
    plt.ylabel("Values")
    plt.title("Visualization of CSV Data")
    plt.legend()
    plt.grid(True)

    # Determine output filename
    output_file = args.output or generate_default_output_name(args.csv_file, args.ext)

    # Check for overwrite
    if os.path.exists(output_file):
        if not confirm_overwrite(output_file):
            print("Operation canceled.")
            return

    # Save the plot
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")


def generate_default_output_name(input_file: str, ext: str) -> str:
    """Generate a default output filename based on the input file and extension."""
    base_name, _ = os.path.splitext(input_file)
    return f"{base_name}_plot.{ext}"


def confirm_overwrite(file_path: str) -> bool:
    """Ask the user for confirmation before overwriting a file."""
    response = input(f"File {file_path} already exists. Overwrite? (y/n): ").strip().lower()
    return response == "y"

if __name__ == "__main__":
    main()
~~~

~~~ d1_count_words_2024_1221.csv
Year,AI,genAI
2000,0,0
2001,0,0
2002,0,0
2003,0,0
2004,0,0
2005,0,0
2006,0,0
2007,0,0
2008,0,0
2009,0,0
2010,0,0
2011,0,0
2012,0,0
2013,0,0
2014,0,0
2015,0,0
2016,1,0
2017,8,0
2018,15,0
2019,15,0
2020,24,0
2021,12,0
2022,5,0
2023,56,23
2024,115,39
~~~

## Assistant (o1)

**Adjusting font scaling**

The user aims to modify matplotlib font sizes through a command-line argument, proposing a scaling factor to adjust fonts.

**Refining font scaling**

I'm working through the command-line argument to adjust matplotlib fonts, ensuring precise control and maintaining moderating simplicity for easy scaling adjustments.

## Assistant (o1)

Below is an updated version of your script that adds a `--font-scale` argument. This argument lets you specify a scaling factor by which to magnify the font sizes in your plots. For example, if you pass `--font-scale 1.5`, then all the text (title, labels, ticks, legend, etc.) will be enlarged by 50%.

```python
#!/usr/bin/env python3

"""
This script visualizes CSV data with a flexible approach to handle multiple columns.
It offers options for specifying a starting year, an output filename, and
a font size scaling factor for the plot.

Usage:
    python visualize_csv.py <CSV_FILE> [--start-year YEAR] [--output OUTPUT_FILE]
                            [--ext EXTENSION] [--font-scale FLOAT]
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional

def main():
    parser = argparse.ArgumentParser(description="Visualize CSV data with flexible column support.")
    parser.add_argument("csv_file", type=str, help="Path to the input CSV file.")
    parser.add_argument("--start-year", type=int, default=None, help="Specify the starting year for the plot.")
    parser.add_argument("--output", type=str, default=None, help="Specify the output filename.")
    parser.add_argument("--ext", type=str, choices=["pdf", "png", "jpg"], default="pdf",
                        help="Specify the output image format (default: pdf).")
    parser.add_argument("--font-scale", type=float, default=1.0,
                        help="Scaling factor for magnifying font sizes in the plot (default: 1.0).")

    args = parser.parse_args()

    # Apply font scaling
    plt.rcParams.update({
        'font.size': 10 * args.font_scale,
        'axes.labelsize': 12 * args.font_scale,
        'axes.titlesize': 14 * args.font_scale,
        'legend.fontsize': 10 * args.font_scale,
        'xtick.labelsize': 10 * args.font_scale,
        'ytick.labelsize': 10 * args.font_scale
    })

    # Load the CSV file
    data = pd.read_csv(args.csv_file)

    # Validate CSV structure
    if "Year" not in data.columns:
        raise ValueError("CSV file must have a 'Year' column.")

    # Filter by starting year if specified
    if args.start_year:
        data = data[data["Year"] >= args.start_year]

    # Plot the data
    plt.figure(figsize=(10, 6))
    for column in data.columns:
        if column != "Year":
            plt.plot(data["Year"], data[column], label=column)

    plt.xlabel("Year")
    plt.ylabel("Values")
    plt.title("Visualization of CSV Data")
    plt.legend()
    plt.grid(True)

    # Determine output filename
    output_file = args.output or generate_default_output_name(args.csv_file, args.ext)

    # Check for overwrite
    if os.path.exists(output_file):
        if not confirm_overwrite(output_file):
            print("Operation canceled.")
            return

    # Save the plot
    plt.savefig(output_file)
    print(f"Plot saved to {output_file}")

def generate_default_output_name(input_file: str, ext: str) -> str:
    """Generate a default output filename based on the input file and extension."""
    base_name, _ = os.path.splitext(input_file)
    return f"{base_name}_plot.{ext}"

def confirm_overwrite(file_path: str) -> bool:
    """Ask the user for confirmation before overwriting a file."""
    response = input(f"File {file_path} already exists. Overwrite? (y/n): ").strip().lower()
    return response == "y"

if __name__ == "__main__":
    main()
```

**How to use the new option**:

1. Run the script as usual:
   ```bash
   python visualize_csv_data.py d1_count_words_2024_1221.csv
   ```
   The default font scale is `1.0`.

2. To enlarge the font (for example, by 50%), run:
   ```bash
   python visualize_csv_data.py d1_count_words_2024_1221.csv --font-scale 1.5
   ```

3. To shrink the font (for example, by half), run:
   ```bash
   python visualize_csv_data.py d1_count_words_2024_1221.csv --font-scale 0.5
   ```

Adjusting the `--font-scale` parameter will proportionally affect all titles, axis labels, and legend text in your plots.

