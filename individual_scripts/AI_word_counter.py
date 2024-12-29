#!/usr/bin/env python3

import argparse
from typing import List
from common_functions import (
    EXCLUDED_WORDS,
    write_results_to_file,
    count_html_files
)

def line_contains_search_terms_ai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains the desired search terms for
    'AI', 'artificial_intelligence', or 'both'.
    """
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI", exclude lines with EXCLUDED_WORDS
        if "AI" in line:  # exact uppercase check
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" in any case
        return "artificial intelligence" in line_lower

    elif search_mode == "both":
        # A line matches if it contains:
        #   - "artificial intelligence" (case-insensitive), OR
        #   - "AI" (uppercase only) not in EXCLUDED_WORDS
        has_artificial_intel = ("artificial intelligence" in line_lower)
        has_ai = (
            "AI" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        )
        return has_artificial_intel or has_ai

    # Not handled by this script
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Count occurrences of AI or 'artificial intelligence' in HTML."
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
        choices=["AI", "artificial_intelligence", "both"],
        default="both",
        help=(
            "What to search for:\n"
            "- AI (uppercase only)\n"
            "- artificial_intelligence (case-insensitive)\n"
            "- both (either of the above)\n"
            "Default is 'both'."
        )
    )

    args = parser.parse_args()

    results = count_html_files(
        directories=args.directories,
        scope=args.scope,
        search_mode=args.search,
        show_lines=args.show_lines,
        skip_duplicates=args.skip_duplicates,
        line_checker_func=line_contains_search_terms_ai
    )

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
