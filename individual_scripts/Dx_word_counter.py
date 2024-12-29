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
