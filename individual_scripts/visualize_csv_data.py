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

    # Define different markers to cycle through
    markers = ['o', 's', '^', 'D', 'x', 'v', 'p', 'h']

    # Get all columns except 'Year'
    columns_to_plot = [col for col in data.columns if col != "Year"]

    # Plot the data
    plt.figure(figsize=(10, 6))

    for i, column in enumerate(columns_to_plot):
        # Select a marker by cycling through the list
        marker_index = i % len(markers)
        plt.plot(data["Year"], data[column],
                 marker=markers[marker_index],
                 label=column)

    plt.xlabel("Year")
    plt.ylabel("Count")
    #plt.title("Visualization of CSV Data")
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
