#!/usr/bin/env python3

import argparse
from typing import List
from common_functions import (
    EXCLUDED_WORDS,
    write_results_to_file,
    count_html_files
)

def line_contains_search_terms_genai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains 'generative artificial intelligence',
    'generative AI', 'gen AI', or 'genAI' (or 'all' which is any of these).
    """
    line_lower = line.lower()

    # -----------------------------------------
    # 1) generative_artificial_intelligence
    # -----------------------------------------
    if search_mode == "generative_artificial_intelligence":
        # Case-insensitive match for the phrase "generative artificial intelligence"
        return "generative artificial intelligence" in line_lower

    # -----------------------------------------
    # 2) generative_AI
    # -----------------------------------------
    elif search_mode == "generative_AI":
        # Must contain "generative" (case-insensitive) and then uppercase "AI".
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        # Check if the matched segment in the original line ends with uppercase "AI"
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            # Exclude lines containing any EXCLUDED_WORDS
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # -----------------------------------------
    # 3) gen_AI
    # -----------------------------------------
    elif search_mode == "gen_AI":
        # Must contain "gen ai" in line_lower, then confirm uppercase "AI" in original line
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # -----------------------------------------
    # 4) genAI
    # -----------------------------------------
    elif search_mode == "genAI":
        # Must contain "genai" in line_lower, then confirm uppercase "AI" in original line
        phrase = "genai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # -----------------------------------------
    # ALL: default to match any of the above
    # -----------------------------------------
    elif search_mode == "all":
        # We'll combine all checks. If any of them is True => return True
        # 1) generative_artificial_intelligence
        if "generative artificial intelligence" in line_lower:
            return True

        # 2) generative_AI
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # 3) gen_AI
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # 4) genAI
        phrase = "genai"
        pos = line_lower.find(phrase)
        if pos != -1:
            found_str = line[pos : pos + len(phrase)]
            if found_str.endswith("AI"):
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

        # None of the generative checks matched
        return False

    # If none of the above match, return False
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Count occurrences of various generative AI-related terms in HTML."
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
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
            "genAI"
        ],
        default="all",
        help=(
            "What to search for:\n"
            "- all (any of the generative AI terms)\n"
            "- generative_artificial_intelligence\n"
            "- generative_AI (case-insensitive for 'generative', uppercase 'AI')\n"
            "- gen_AI (case-insensitive for 'gen', uppercase 'AI')\n"
            "- genAI (case-insensitive for 'gen', uppercase 'AI')\n"
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
        line_checker_func=line_contains_search_terms_genai
    )

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
