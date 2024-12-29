---
title: Dx case sensitive update
create_time: 2024-12-21 21:40:20
update_time: 2024-12-21 21:40:51
conversation_id: 6766b734-5948-800f-8aca-6249c4a011ab
---

# Dx case sensitive update

Creation Time: 2024-12-21 21:40:20

Update Time: 2024-12-21 21:40:51

## Assistant



## User

Based on `AI_word_counter.py`, please update `Dx_word_counter.py` to make "Dx" case sensitive while excluding t"F7lBDxwOe" and "gs5xDx0ilF".

~~~ AI_word_counter.py
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
~~~

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
    'DX', or other variants (or 'all' which is any of these).
    """
    line_lower = line.lower()

    dx_variants = [
        "digital transformation", "dx", 
    ]

    if search_mode in dx_variants:
        # Exact match for the specific search mode
        return search_mode in line_lower

    elif search_mode == "all":
        # Match any of the variants
        for phrase in dx_variants:
            if phrase in line_lower:
                # Exclude lines containing any EXCLUDED_WORDS
                if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):
                    return True

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

To make `Dx_word_counter.py` case-sensitive for "Dx" while excluding the strings "F7lBDxwOe" and "gs5xDx0ilF," we will update the `line_contains_search_terms_dx` function to enforce case sensitivity for "Dx." Here's the updated script:

## Assistant (gpt-4o)

{"name": "Dx_word_counter", "type": "code/python", "content": "#!/usr/bin/env python3\n\nimport argparse\nfrom typing import List\nfrom common_functions import (\n    EXCLUDED_WORDS,\n    write_results_to_file,\n    count_html_files\n)\n\ndef line_contains_search_terms_dx(line: str, search_mode: str) -> bool:\n    \"\"\"\n    Check if a given line contains 'digital transformation',\n    'Dx' (case-sensitive), or other variants (or 'all' which is any of these),\n    while excluding specific strings.\n    \"\"\"\n    line_lower = line.lower()\n\n    # Case-sensitive \"Dx\" check excludes specific strings\n    dx_exclusions = [\"F7lBDxwOe\", \"gs5xDx0ilF\"]\n\n    if search_mode == \"dx\":\n        if \"Dx\" in line:\n            # Exclude lines containing any EXCLUDED_WORDS or specific exclusions\n            if not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS):\n                if not any(excl in line for excl in dx_exclusions):\n                    return True\n        return False\n\n    elif search_mode == \"digital transformation\":\n        # Case-insensitive \"digital transformation\"\n        return \"digital transformation\" in line_lower\n\n    elif search_mode == \"all\":\n        # Match \"digital transformation\" (case-insensitive) or \"Dx\" (case-sensitive)\n        has_digital_transformation = \"digital transformation\" in line_lower\n        has_dx = (\n            \"Dx\" in line\n            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)\n            and not any(excl in line for excl in dx_exclusions)\n        )\n        return has_digital_transformation or has_dx\n\n    # If no match, return False\n    return False\n\ndef main():\n    parser = argparse.ArgumentParser(\n        description=\"Count occurrences of various digital transformation-related terms in HTML.\"\n    )\n    parser.add_argument(\n        \"directories\",\n        type=str,\n        nargs='+',\n        help=\"Directories containing HTML files.\"\n    )\n    parser.add_argument(\n        \"-o\", \"--output\",\n        type=str,\n        help=\"Output filename.\"\n    )\n    parser.add_argument(\n        \"-s\", \"--show-lines\",\n        action=\"store_true\",\n        help=\"Show matched lines.\"\n    )\n    parser.add_argument(\n        \"--skip-duplicates\",\n        action=\"store_true\",\n        help=\"Skip files with duplicate <h1> content.\"\n    )\n    parser.add_argument(\n        \"--scope\",\n        choices=[\"title\", \"title_and_content\"],\n        default=\"title_and_content\",\n        help=(\n            \"Which part of the HTML to scan. \"\n            \"'title' scans only <h1>, \"\n            \"'title_and_content' scans <h1> + <div class='rte-section'>.\"\n        )\n    )\n    parser.add_argument(\n        \"--search\",\n        choices=[\n            \"all\",\n            \"digital transformation\",\n            \"dx\",\n        ],\n        default=\"all\",\n        help=(\n            \"What to search for:\\n\"\n            \"- all (any of the digital transformation terms)\\n\"\n            \"- Specific term from the list of variants.\\n\"\n            \"Default is 'all'.\"\n        )\n    )\n\n    args = parser.parse_args()\n\n    results = count_html_files(\n        directories=args.directories,\n        scope=args.scope,\n        search_mode=args.search,\n        show_lines=args.show_lines,\n        skip_duplicates=args.skip_duplicates,\n        line_checker_func=line_contains_search_terms_dx\n    )\n\n    if args.output:\n        write_results_to_file(args.output, results)\n    else:\n        print(\"\\n\".join(results))\n\nif __name__ == \"__main__\":\n    main()"}

## Assistant (gpt-4o)

{"result": "Successfully created text document 'Dx_word_counter' which will be referenced in all future messages with the unique identifier textdoc_id: '6766b74de1188191b6f9dd446040f4dd'", "textdoc_id": "6766b74de1188191b6f9dd446040f4dd", "name": "Dx_word_counter"}

## Assistant (gpt-4o)

This updated script ensures that:

1. **Case-Sensitivity for "Dx"**:
   - The search for "Dx" is explicitly case-sensitive.
   
2. **Exclusion of Specific Strings**:
   - Lines containing "F7lBDxwOe" or "gs5xDx0ilF" are excluded from matching.

3. **Exclusion of General EXCLUDED_WORDS**:
   - Any line containing words from the `EXCLUDED_WORDS` list is excluded.

Feel free to run the updated script and let me know if further refinements are needed!

