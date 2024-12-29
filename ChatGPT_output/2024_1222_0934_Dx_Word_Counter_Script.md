---
title: Dx Word Counter Script
create_time: 2024-12-22 09:34:24
update_time: 2024-12-22 09:35:07
conversation_id: 67675e90-a4c4-800f-ac2c-124b277b1b10
---

# Dx Word Counter Script

Creation Time: 2024-12-22 09:34:24

Update Time: 2024-12-22 09:35:07

## Assistant



## User

Please explain the purpose of the following program and find articles related to this task:

~~~ Dx_word_counter.py
#!/usr/bin/env python3

import argparse
from typing import List
from common_functions import (
    EXCLUDED_WORDS,
    write_results_to_file,
    count_html_files
)

def line_contains_search_terms_dx(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains 'digital transformation',
    'Dx' (case-sensitive), or other variants (or 'all' which is any of these),
    while excluding specific strings.
    """
    line_lower = line.lower()

    # Case-sensitive "Dx" check excludes specific strings
    dx_exclusions = ["F7lBDxwOe", "gs5xDx0ilF"]

    if search_mode == "dx":
        if "Dx" in line:
            # Exclude lines containing any EXCLUDED_WORDS or specific exclusions
            if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                if not any(excl in line for excl in dx_exclusions):
                    return True
        return False

    elif search_mode == "digital transformation":
        # Case-insensitive "digital transformation"
        return "digital transformation" in line_lower

    elif search_mode == "all":
        # Match "digital transformation" (case-insensitive) or "Dx" (case-sensitive)
        has_digital_transformation = "digital transformation" in line_lower
        has_dx = (
            "Dx" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
            and not any(excl in line for excl in dx_exclusions)
        )
        return has_digital_transformation or has_dx

    # If no match, return False
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Count occurrences of various digital transformation-related terms in HTML."
    )
    parser.add_argument(
        "directories",
        type=str,
        nargs='+',
        help="Directories containing HTML files."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Output filename."
    )
    parser.add_argument(
        "-s", "--show-lines",
        action="store_true",
        help="Show matched lines."
    )
    parser.add_argument(
        "--skip-duplicates",
        action="store_true",
        help="Skip files with duplicate <h1> content."
    )
    parser.add_argument(
        "--scope",
        choices=["title", "title_and_content"],
        default="title_and_content",
        help=(
            "Which part of the HTML to scan. "
            "'title' scans only <h1>, "
            "'title_and_content' scans <h1> + <div class='rte-section'>."
        )
    )
    parser.add_argument(
        "--search",
        choices=[
            "all",
            "digital transformation",
            "dx",
        ],
        default="all",
        help=(
            "What to search for:\n"
            "- all (any of the digital transformation terms)\n"
            "- Specific term from the list of variants.\n"
            "Default is 'all'."
        )
    )

    args = parser.parse_args()

    results = count_html_files(
        directories=args.directories,
        scope=args.scope,
        search_mode=args.search,
        show_lines=args.show_lines,
        skip_duplicates=args.skip_duplicates,
        line_checker_func=line_contains_search_terms_dx
    )

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))

if __name__ == "__main__":
    main()
~~~

## Assistant (gpt-4o)

The provided Python script, `Dx_word_counter.py`, is designed to analyze HTML files within specified directories to count occurrences of terms related to digital transformation, specifically "digital transformation" (case-insensitive) and "Dx" (case-sensitive). It offers flexibility through various command-line options, allowing users to customize the analysis based on their needs.

**Key Features:**

- **Directory Input:** The script accepts one or more directories containing HTML files for analysis.

- **Output Specification:** Users can specify an output file to save the results; if not provided, results are printed to the console.

- **Matched Lines Display:** An option to display lines containing the matched terms is available.

- **Duplicate Handling:** The script can skip files with duplicate `<h1>` content to avoid redundant counts.

- **Scope Definition:** Users can define whether to scan only the `<h1>` title or both the `<h1>` title and `<div class='rte-section'>` content within the HTML files.

- **Search Mode:** Three search modes are available:
  - `"all"`: Searches for both "digital transformation" and "Dx".
  - `"digital transformation"`: Searches exclusively for the term "digital transformation".
  - `"dx"`: Searches exclusively for the term "Dx", with specific exclusions to avoid false positives.

**Functionality:**

The script utilizes the `line_contains_search_terms_dx` function to determine if a line in the HTML content matches the search criteria based on the selected search mode. It also references external components from `common_functions`, such as `EXCLUDED_WORDS`, `write_results_to_file`, and `count_html_files`, to manage exclusions, handle output, and process HTML files, respectively.

**Usage Example:**

To run the script with specific parameters, you might use a command like:

```bash
python Dx_word_counter.py -o results.txt --show-lines --skip-duplicates --scope title_and_content --search all /path/to/html_directory
```

This command analyzes HTML files in `/path/to/html_directory`, searches for both "digital transformation" and "Dx" terms within the `<h1>` and `<div class='rte-section'>` sections, displays the matched lines, skips files with duplicate `<h1>` content, and writes the results to `results.txt`.

**Related Articles and Resources:**

For further reading on similar tasks and Python scripts for data analysis, you may find the following resources helpful:

- **Data Transformation with Python:** This resource provides insights into data transformation techniques using Python, which can be beneficial for understanding how to manipulate and analyze data effectively. citeturn0search8

- **Python Scripts for Data Analysis Using the Command Line:** A tutorial that delves into creating Python scripts for data analysis, emphasizing command-line usage, which aligns with the functionality of the provided script. citeturn0search4

- **Counting the Occurrences of One Item in a Sequence:** An example demonstrating how to count occurrences of an item in a list or tuple in Python, which is a fundamental aspect of the script's functionality. citeturn0search7

These resources offer valuable information on data analysis and manipulation using Python, complementing the functionalities implemented in the `Dx_word_counter.py` script. 

