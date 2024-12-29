---
title: Jupytext Refactor Script
create_time: 2024-12-28 21:25:16
update_time: 2024-12-28 21:31:13
conversation_id: 676fee2c-6c80-800f-9774-e8051e7bc752
---

# Jupytext Refactor Script

Creation Time: 2024-12-28 21:25:16

Update Time: 2024-12-28 21:31:13

## Assistant



## User

Please modify and refactor the following python3 code that can be convertible to the Jupyter Notebook format using the `jupytext` command:

~~~ keyword_occurrence_counter.py
#!/usr/bin/env python3

"""
Integrated script that does:
1) Count occurrences of AI/GenAI/Dx in year-based HTML directories,
   then produce a CSV file: "Year,AI,genAI,Dx"
2) Visualize an existing CSV file using matplotlib.

Usage examples:

# 1) To count matches across years and produce a CSV:
   python merged_word_counter.py count \
       --start-year 2000 \
       --end-year 2024 \
       --output-csv keyword_count.csv

# 2) To visualize an existing CSV file:
   python merged_word_counter.py visualize mydata.csv \
       --start-year 2014 \
       --output figure.pdf \
       --font-scale 2
"""

import os
import sys
import argparse
from typing import List, Set

# For HTML parsing
from bs4 import BeautifulSoup

# For CSV data visualization
import pandas as pd
import matplotlib.pyplot as plt


###############################################################################
# 1) COMMON FUNCTIONS (originally from common_functions.py)
###############################################################################
EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE",
    "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI",
    "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]


def write_results_to_file(filename: str, results: List[str]):
    """
    Write results to a file, prompt if overwrite.
    """
    if os.path.exists(filename):
        overwrite = input(f"{filename} exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("File not overwritten.")
            return

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"Results written to {filename}.")


def find_matches_in_html(
    filepath: str,
    scope: str,
    search_mode: str,
    show_lines: bool = False,
    seen_h1: Set[str] = None,
    line_checker_func=None
) -> List[str]:
    """
    Parse an HTML file and find occurrences based on search_mode and scope,
    using the provided line_checker_func to test each line.
    scope can be:
      - "title": only <h1> tags
      - "title_and_content": <h1> + <div class="rte-section">
    If show_lines is True, we return the actual lines matched.
    Otherwise, we return a placeholder "match".
    """
    if line_checker_func is None:
        return []

    results = []

    # Read and parse the HTML
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Decide which sections of the HTML to parse
    if scope == "title":
        sections = soup.find_all("h1")
    else:  # "title_and_content"
        title_tags = soup.find_all("h1")
        content_tags = soup.find_all("div", class_="rte-section")
        sections = title_tags + content_tags

    # Optionally check for duplicate H1 content
    if seen_h1 is not None:
        h1_texts = [tag.get_text(separator="\n").strip() for tag in soup.find_all("h1")]
        for h1_text in h1_texts:
            # From your original scripts: h1_text.replace("Day 2","Day 1")
            h1_text = h1_text.replace("Day 2", "Day 1")
            if h1_text in seen_h1:
                # skip processing entire file if this <h1> was already seen
                return []
            seen_h1.add(h1_text)

    # Extract text from each target section, split into lines, and check
    for tag in sections:
        text_block = tag.get_text(separator="\n")
        lines = text_block.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_checker_func(line_stripped, search_mode):
                if show_lines:
                    results.append(line_stripped)
                else:
                    results.append("match")

    return results


def count_html_files(
    directories: List[str],
    scope: str,
    search_mode: str,
    show_lines: bool = False,
    skip_duplicates: bool = False,
    line_checker_func=None
) -> List[str]:
    """
    Scan HTML files in multiple directories for lines containing the desired terms.
    Optionally skip files with duplicate <h1> content.
    Returns lines like:
      "filename.html: X occurrences"
    plus optionally the matched lines themselves if show_lines=True.
    """
    results = []
    seen_h1 = set() if skip_duplicates else None

    for directory in directories:
        if not os.path.isdir(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".html"):
                    filepath = os.path.join(root, file)
                    matches = find_matches_in_html(
                        filepath=filepath,
                        scope=scope,
                        search_mode=search_mode,
                        show_lines=show_lines,
                        seen_h1=seen_h1,
                        line_checker_func=line_checker_func
                    )
                    if matches:
                        results.append(f"{file}: {len(matches)} occurrences")
                        if show_lines:
                            results.extend(matches)

    return results


###############################################################################
# 2) AI WORD-COUNTER LOGIC (originally from AI_word_counter.py)
###############################################################################
def line_contains_search_terms_ai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains the desired search terms for
    'AI', 'artificial_intelligence', or 'both'.
    """
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI" (exact match in text)
        if "AI" in line:
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" in any case
        return "artificial intelligence" in line_lower

    elif search_mode == "both":
        # A line matches if it contains:
        # - "artificial intelligence" (case-insensitive), OR
        # - "AI" (uppercase only) not in EXCLUDED_WORDS
        has_artificial_intel = "artificial intelligence" in line_lower
        has_ai = (
            "AI" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        )
        return has_artificial_intel or has_ai

    return False


###############################################################################
# 3) DX WORD-COUNTER LOGIC (originally from Dx_word_counter.py)
###############################################################################
def line_contains_search_terms_dx(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains 'digital transformation',
    'Dx' (case-sensitive), or both.
    """
    line_lower = line.lower()
    dx_exclusions = ["F7lBDxwOe", "gs5xDx0ilF"]

    if search_mode == "dx":
        # Must contain "Dx" (exact case)
        if "Dx" in line:
            # Exclude lines containing any EXCLUDED_WORDS or dx_exclusions
            if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                if not any(excl in line for excl in dx_exclusions):
                    return True
        return False

    elif search_mode == "digital transformation":
        return "digital transformation" in line_lower

    elif search_mode == "all":
        has_digital_transformation = "digital transformation" in line_lower
        has_dx = (
            "Dx" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
            and not any(excl in line for excl in dx_exclusions)
        )
        return has_digital_transformation or has_dx

    return False


###############################################################################
# 4) GENAI WORD-COUNTER LOGIC (originally from GenAI_word_counter.py)
###############################################################################
def line_contains_search_terms_genai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains:
      - 'generative artificial intelligence'
      - 'generative AI'   (case-insensitive 'generative', uppercase 'AI')
      - 'gen AI'          (case-insensitive 'gen', uppercase 'AI')
      - 'genAI'           (case-insensitive 'gen', uppercase 'AI')
    or all of the above.
    """
    line_lower = line.lower()

    # 1) generative_artificial_intelligence
    if search_mode == "generative_artificial_intelligence":
        return "generative artificial intelligence" in line_lower

    # 2) generative_AI
    elif search_mode == "generative_AI":
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # 3) gen_AI
    elif search_mode == "gen_AI":
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # 4) genAI
    elif search_mode == "genAI":
        phrase = "genai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # 5) all
    elif search_mode == "all":
        # a) generative artificial intelligence
        if "generative artificial intelligence" in line_lower:
            return True

        # b) generative AI
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # c) gen AI
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # d) genAI
        phrase = "genai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        return False

    return False


###############################################################################
# 5) REPLICATE THE "loop over years and produce CSV" (from 1_count_words_2024_1221.sh)
###############################################################################
def count_files_for_search(
    year: int,
    line_checker_func,
    search_mode: str,
    scope: str = "title_and_content",
    skip_duplicates: bool = True
) -> int:
    """
    For a given year, call `count_html_files(...)` on directory 'html_{year}'
    with the specified line_checker_func and search_mode.
    Then count how many files had at least one match (like "grep html | wc -l").
    """
    directory = f"html_{year}"
    results = count_html_files(
        directories=[directory],
        scope=scope,
        search_mode=search_mode,
        show_lines=False,
        skip_duplicates=skip_duplicates,
        line_checker_func=line_checker_func
    )
    # Each matched file is indicated by a line "filename.html: X occurrences"
    count = sum(1 for line in results if line.endswith("occurrences"))
    return count


def produce_csv_output(start_year: int, end_year: int) -> List[str]:
    """
    Produce CSV lines of the form:
      Year,AI,genAI,Dx
    for each year in [start_year .. end_year].
    """
    csv_lines = []
    csv_lines.append("Year,AI,genAI,Dx")

    for year in range(start_year, end_year + 1):
        # AI => line_contains_search_terms_ai, search_mode='both'
        ai_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_ai,
            search_mode="both"
        )
        # GenAI => line_contains_search_terms_genai, search_mode='all'
        genai_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_genai,
            search_mode="all"
        )
        # Dx => line_contains_search_terms_dx, search_mode='all'
        dx_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_dx,
            search_mode="all"
        )
        csv_lines.append(f"{year},{ai_count},{genai_count},{dx_count}")

    return csv_lines


###############################################################################
# 6) VISUALIZATION LOGIC (from visualize_csv_data.py)
###############################################################################
def do_visualize(args):
    """
    Visualize CSV data with flexible column support, optionally filtering by a 
    starting year. 
    """
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

    # Cycle of markers
    markers = ['o', 's', '^', 'D', 'x', 'v', 'p', 'h']

    # Get all columns except 'Year'
    columns_to_plot = [col for col in data.columns if col != "Year"]

    # Plot the data
    plt.figure(figsize=(10, 6))

    for i, column in enumerate(columns_to_plot):
        marker_index = i % len(markers)
        plt.plot(data["Year"], data[column],
                 marker=markers[marker_index],
                 label=column)

    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True)

    # Determine output filename
    output_file = args.output or generate_default_output_name(args.csv_file, args.ext)

    # Check for overwrite
    if os.path.exists(output_file):
        if not confirm_overwrite(output_file):
            print("Operation canceled.")
            return

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


###############################################################################
# 7) MAIN: Use subcommands "count" vs "visualize" to unify all functionalities.
###############################################################################
def main():
    parser = argparse.ArgumentParser(
        description="Merged script to count AI/GenAI/Dx occurrences into CSV, or visualize CSV data."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # -----------------------------------------------------------------------
    # Sub-command: count
    # -----------------------------------------------------------------------
    parser_count = subparsers.add_parser("count", help="Count words across year-based HTML folders into a CSV.")
    parser_count.add_argument("--start-year", type=int, default=2000,
                              help="Earliest year to scan (default=2000).")
    parser_count.add_argument("--end-year", type=int, default=2024,
                              help="Latest year to scan (default=2024).")
    parser_count.add_argument("--output-csv", type=str, default="keyword_count.csv",
                              help="CSV filename for results (default=keyword_count.csv).")
    parser_count.add_argument("--only-csv", action="store_true",
                              help="Print CSV to stdout instead of writing to file (no overwrite prompt).")

    # -----------------------------------------------------------------------
    # Sub-command: visualize
    # -----------------------------------------------------------------------
    parser_viz = subparsers.add_parser("visualize", help="Visualize CSV data.")
    parser_viz.add_argument("csv_file", type=str, help="Path to the input CSV file.")
    parser_viz.add_argument("--start-year", type=int, default=None, help="Specify the starting year to include.")
    parser_viz.add_argument("--output", type=str, default=None, help="Output filename.")
    parser_viz.add_argument("--ext", type=str, choices=["pdf", "png", "jpg"], default="pdf",
                            help="Output image format (default=pdf).")
    parser_viz.add_argument("--font-scale", type=float, default=1.0,
                            help="Scaling factor for plot fonts (default=1.0).")

    # -----------------------------------------------------------------------
    # Parse and dispatch
    # -----------------------------------------------------------------------
    args = parser.parse_args()

    if args.command == "count":
        # Produce the CSV lines
        csv_data = produce_csv_output(args.start_year, args.end_year)

        if args.only_csv:
            # Print to stdout
            print("\n".join(csv_data))
        else:
            # Write to file with overwrite prompt
            write_results_to_file(args.output_csv, csv_data)

    elif args.command == "visualize":
        do_visualize(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

~~~

## Assistant (o1)

**Converting script**

I'm converting a Python script to a Jupyter Notebook with `jupytext`. The goal is to keep code and README docs in one script, with functional cells for a well-structured report.

**Structuring the notebook**

I’m organizing the notebook with a header for `jupytext`, clear markdown for usage instructions, and main code cells, ensuring compatibility for both Python and Jupyter Notebook.

**Refining script execution**

I’m ensuring the script works from the command line by keeping argument parsing and organizing the notebook. The script's name and jupytext configuration are tweaked for clarity and usability.

**Finalizing the structure**

I’m breaking down the code into logical parts: imports, constants, functions, AI word counter, DX word counter, GenAI word counter, counting logic, visualization logic, and the main block.

## Assistant (o1)

Below is a *refactored* version of your Python script, structured into cells that are compatible with **Jupytext** conversion (to and from Jupyter notebooks). You can save this as a `.py` file and convert it to a notebook (`.ipynb`) with commands such as:

```bash
# Convert Python script to notebook
jupytext --to ipynb keyword_occurrence_counter.py
```

> **Note**: The script is split into multiple cells using the `# %%` or `# %% [markdown]` directives. Jupytext will treat these as cells when converting to `.ipynb` format.

---

```python
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#   kernelspec:
#     name: python3
# ---

# %% [markdown]
"""
# Keyword Occurrence Counter

This refactored script provides two main functions:

1. **Count** occurrences of AI/GenAI/Dx in year-based HTML directories, then produce a CSV file (format: "Year,AI,genAI,Dx").

2. **Visualize** an existing CSV file using matplotlib.

## Usage Examples

1) **Count matches across years and produce a CSV**:
```bash
python keyword_occurrence_counter.py count \
       --start-year 2000 \
       --end-year 2024 \
       --output-csv keyword_count.csv
```

2) **Visualize an existing CSV file**:
```bash
python keyword_occurrence_counter.py visualize mydata.csv \
       --start-year 2014 \
       --output figure.pdf \
       --font-scale 2
```
"""

# %% [markdown]
"""
## Imports and Global Constants
"""

# %%
import os
import sys
import argparse
from typing import List, Set

# For HTML parsing
from bs4 import BeautifulSoup

# For CSV data visualization
import pandas as pd
import matplotlib.pyplot as plt

# Excluded words that might appear like "AI" but are not relevant
EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE",
    "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI",
    "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]

# %% [markdown]
"""
## Common Functions

These utility functions support file reading/writing and searching through HTML content.
"""

# %%
def write_results_to_file(filename: str, results: List[str]):
    """
    Write results to a file, prompt if overwrite.
    """
    if os.path.exists(filename):
        overwrite = input(f"{filename} exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("File not overwritten.")
            return

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print(f"Results written to {filename}.")


def find_matches_in_html(
    filepath: str,
    scope: str,
    search_mode: str,
    show_lines: bool = False,
    seen_h1: Set[str] = None,
    line_checker_func=None
) -> List[str]:
    """
    Parse an HTML file and find occurrences based on search_mode and scope,
    using the provided line_checker_func to test each line.

    Parameters
    ----------
    scope: str
        "title" => only <h1> tags
        "title_and_content" => <h1> + <div class="rte-section">
    show_lines: bool
        If True, collect the matched lines themselves, else just record a "match".
    seen_h1: Set[str]
        If provided, used to detect duplicate <h1> content across multiple files.
    """
    if line_checker_func is None:
        return []

    results = []

    # Read and parse the HTML
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Decide which sections of the HTML to parse
    if scope == "title":
        sections = soup.find_all("h1")
    else:
        title_tags = soup.find_all("h1")
        content_tags = soup.find_all("div", class_="rte-section")
        sections = title_tags + content_tags

    # Optionally check for duplicate H1 content
    if seen_h1 is not None:
        h1_texts = [tag.get_text(separator="\n").strip() for tag in soup.find_all("h1")]
        for h1_text in h1_texts:
            # Original script logic: h1_text.replace("Day 2","Day 1")
            h1_text = h1_text.replace("Day 2", "Day 1")
            if h1_text in seen_h1:
                # Skip processing entire file if this <h1> was already seen
                return []
            seen_h1.add(h1_text)

    # Extract text from each target section, split into lines, and check
    for tag in sections:
        text_block = tag.get_text(separator="\n")
        lines = text_block.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_checker_func(line_stripped, search_mode):
                if show_lines:
                    results.append(line_stripped)
                else:
                    results.append("match")

    return results


def count_html_files(
    directories: List[str],
    scope: str,
    search_mode: str,
    show_lines: bool = False,
    skip_duplicates: bool = False,
    line_checker_func=None
) -> List[str]:
    """
    Scan HTML files in multiple directories for lines containing the desired terms.
    Optionally skip files with duplicate <h1> content.

    Returns lines like:
      "filename.html: X occurrences"
    plus optionally the matched lines themselves if show_lines=True.
    """
    results = []
    seen_h1 = set() if skip_duplicates else None

    for directory in directories:
        if not os.path.isdir(directory):
            continue
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".html"):
                    filepath = os.path.join(root, file)
                    matches = find_matches_in_html(
                        filepath=filepath,
                        scope=scope,
                        search_mode=search_mode,
                        show_lines=show_lines,
                        seen_h1=seen_h1,
                        line_checker_func=line_checker_func
                    )
                    if matches:
                        results.append(f"{file}: {len(matches)} occurrences")
                        if show_lines:
                            results.extend(matches)

    return results


# %% [markdown]
"""
## AI Word-Counter Logic
"""

# %%
def line_contains_search_terms_ai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains the desired search terms for
    'AI', 'artificial_intelligence', or 'both'.
    """
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI" (exact match in text),
        # excluding lines that contain known exceptions.
        if "AI" in line:
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" in any case
        return "artificial intelligence" in line_lower

    elif search_mode == "both":
        # A line matches if it contains:
        # - "artificial intelligence" (case-insensitive), OR
        # - "AI" (uppercase only) not in EXCLUDED_WORDS
        has_artificial_intel = "artificial intelligence" in line_lower
        has_ai = (
            "AI" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        )
        return has_artificial_intel or has_ai

    return False


# %% [markdown]
"""
## Dx Word-Counter Logic
"""

# %%
def line_contains_search_terms_dx(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains 'digital transformation',
    'Dx' (case-sensitive), or both.
    """
    line_lower = line.lower()
    dx_exclusions = ["F7lBDxwOe", "gs5xDx0ilF"]

    if search_mode == "dx":
        # Must contain "Dx" (exact case)
        if "Dx" in line:
            # Exclude lines containing any EXCLUDED_WORDS or dx_exclusions
            if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                if not any(excl in line for excl in dx_exclusions):
                    return True
        return False

    elif search_mode == "digital transformation":
        return "digital transformation" in line_lower

    elif search_mode == "all":
        has_digital_transformation = "digital transformation" in line_lower
        has_dx = (
            "Dx" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
            and not any(excl in line for excl in dx_exclusions)
        )
        return has_digital_transformation or has_dx

    return False


# %% [markdown]
"""
## GenAI Word-Counter Logic
"""

# %%
def line_contains_search_terms_genai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains:
      - 'generative artificial intelligence'
      - 'generative AI'   (case-insensitive 'generative', uppercase 'AI')
      - 'gen AI'          (case-insensitive 'gen', uppercase 'AI')
      - 'genAI'           (case-insensitive 'gen', uppercase 'AI')
    or all of the above, depending on the chosen search_mode.
    """
    line_lower = line.lower()

    # (1) generative_artificial_intelligence
    if search_mode == "generative_artificial_intelligence":
        return "generative artificial intelligence" in line_lower

    # (2) generative_AI
    elif search_mode == "generative_AI":
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # (3) gen_AI
    elif search_mode == "gen_AI":
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # (4) genAI
    elif search_mode == "genAI":
        phrase = "genai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # (5) all
    elif search_mode == "all":
        # a) generative artificial intelligence
        if "generative artificial intelligence" in line_lower:
            return True

        # b) generative AI
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # c) gen AI
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # d) genAI
        phrase = "genai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        return False

    return False


# %% [markdown]
"""
## Counting Logic

Replicate the process of scanning across year-labeled directories (e.g., `html_2020/`, `html_2021/`, etc.) 
and producing a CSV with columns: Year,AI,genAI,Dx.
"""

# %%
def count_files_for_search(
    year: int,
    line_checker_func,
    search_mode: str,
    scope: str = "title_and_content",
    skip_duplicates: bool = True
) -> int:
    """
    For a given year, call `count_html_files(...)` on directory 'html_{year}'
    with the specified line_checker_func and search_mode.
    Then count how many files had at least one match.
    """
    directory = f"html_{year}"
    results = count_html_files(
        directories=[directory],
        scope=scope,
        search_mode=search_mode,
        show_lines=False,
        skip_duplicates=skip_duplicates,
        line_checker_func=line_checker_func
    )
    # Each matched file is indicated by a line "filename.html: X occurrences"
    count = sum(1 for line in results if line.endswith("occurrences"))
    return count


def produce_csv_output(start_year: int, end_year: int) -> List[str]:
    """
    Produce CSV lines of the form:
      Year,AI,genAI,Dx
    for each year in [start_year .. end_year].
    """
    csv_lines = ["Year,AI,genAI,Dx"]
    for year in range(start_year, end_year + 1):
        ai_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_ai,
            search_mode="both"
        )
        genai_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_genai,
            search_mode="all"
        )
        dx_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_dx,
            search_mode="all"
        )
        csv_lines.append(f"{year},{ai_count},{genai_count},{dx_count}")

    return csv_lines


# %% [markdown]
"""
## Visualization Logic

Loads a CSV and plots each column (except 'Year') versus time.
"""

# %%
def do_visualize(args):
    """
    Visualize CSV data with flexible column support, optionally filtering by a 
    starting year.
    """
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

    # Cycle of markers
    markers = ['o', 's', '^', 'D', 'x', 'v', 'p', 'h']
    columns_to_plot = [col for col in data.columns if col != "Year"]

    # Plot the data
    plt.figure(figsize=(10, 6))
    for i, column in enumerate(columns_to_plot):
        marker_index = i % len(markers)
        plt.plot(data["Year"], data[column],
                 marker=markers[marker_index],
                 label=column)

    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True)

    # Determine output filename
    output_file = args.output or generate_default_output_name(args.csv_file, args.ext)

    # Check for overwrite
    if os.path.exists(output_file):
        if not confirm_overwrite(output_file):
            print("Operation canceled.")
            return

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


# %% [markdown]
"""
## Main Function

This parses CLI arguments and executes either "count" or "visualize" functionality.
"""

# %%
def main():
    parser = argparse.ArgumentParser(
        description="Merged script to count AI/GenAI/Dx occurrences into CSV, or visualize CSV data."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    # -----------------------------------------------------------------------
    # Sub-command: count
    # -----------------------------------------------------------------------
    parser_count = subparsers.add_parser(
        "count", 
        help="Count words across year-based HTML folders into a CSV."
    )
    parser_count.add_argument(
        "--start-year", 
        type=int, 
        default=2000,
        help="Earliest year to scan (default=2000)."
    )
    parser_count.add_argument(
        "--end-year", 
        type=int, 
        default=2024,
        help="Latest year to scan (default=2024)."
    )
    parser_count.add_argument(
        "--output-csv", 
        type=str, 
        default="keyword_count.csv",
        help="CSV filename for results (default=keyword_count.csv)."
    )
    parser_count.add_argument(
        "--only-csv", 
        action="store_true",
        help="Print CSV to stdout instead of writing to file (no overwrite prompt)."
    )

    # -----------------------------------------------------------------------
    # Sub-command: visualize
    # -----------------------------------------------------------------------
    parser_viz = subparsers.add_parser(
        "visualize", 
        help="Visualize CSV data."
    )
    parser_viz.add_argument(
        "csv_file", 
        type=str, 
        help="Path to the input CSV file."
    )
    parser_viz.add_argument(
        "--start-year", 
        type=int, 
        default=None, 
        help="Specify the starting year to include."
    )
    parser_viz.add_argument(
        "--output", 
        type=str, 
        default=None, 
        help="Output filename."
    )
    parser_viz.add_argument(
        "--ext", 
        type=str, 
        choices=["pdf", "png", "jpg"], 
        default="pdf",
        help="Output image format (default=pdf)."
    )
    parser_viz.add_argument(
        "--font-scale", 
        type=float, 
        default=1.0,
        help="Scaling factor for plot fonts (default=1.0)."
    )

    args = parser.parse_args()

    if args.command == "count":
        # Produce the CSV lines
        csv_data = produce_csv_output(args.start_year, args.end_year)

        if args.only_csv:
            # Print to stdout
            print("\n".join(csv_data))
        else:
            # Write to file with overwrite prompt
            write_results_to_file(args.output_csv, csv_data)

    elif args.command == "visualize":
        do_visualize(args)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

---

### How to Convert with Jupytext

1. **Install Jupytext (if not already installed)**:
   ```bash
   pip install jupytext
   ```

2. **Convert from `.py` to `.ipynb`**:
   ```bash
   jupytext --to ipynb keyword_occurrence_counter.py
   ```
   This will create `keyword_occurrence_counter.ipynb`.

3. **Convert back from `.ipynb` to `.py`** (if you edited the notebook and want to synchronize changes):
   ```bash
   jupytext --to py keyword_occurrence_counter.ipynb
   ```

You can then open `keyword_occurrence_counter.ipynb` in Jupyter Notebook or JupyterLab to run the cells interactively.

