---
title: Dx word counter update
create_time: 2024-12-21 21:15:14
update_time: 2024-12-21 21:16:20
conversation_id: 6766b151-d220-800f-a0a9-868cb819a229
---

# Dx word counter update

Creation Time: 2024-12-21 21:15:14

Update Time: 2024-12-21 21:16:20

## Assistant



## User

Please list "digital transformation" and its other expressions including "Dx". Based on the list, please rewrite the following script to find words for them instead of "generative AI" and others.

~~~ GenAI_word_counter.py
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
~~~

~~~ common_functions.py
#!/usr/bin/env python3

import os
from typing import List
from bs4 import BeautifulSoup

# Shared list of words to exclude
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
    seen_h1: set = None,
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

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Decide which sections of the HTML to parse
    if scope == "title":
        sections = soup.find_all("h1")
    else:  # "title_and_content"
        title_tags = soup.find_all("h1")
        content_tags = soup.find_all("div", class_="rte-section")
        sections = title_tags + content_tags

    # Check for duplicate H1 content if needed
    if seen_h1 is not None:
        h1_texts = [tag.get_text(separator="\n").strip() for tag in soup.find_all("h1")]
        for h1_text in h1_texts:
            h1_text = h1_text.replace("Day 2", "Day 1")
            if h1_text in seen_h1:
            #if h1_text in seen_h1:
                return []  # Skip processing if duplicate <h1> content
            seen_h1.add(h1_text)

    # Extract text, split into lines, and check each line
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
    """
    results = []
    seen_h1 = set() if skip_duplicates else None

    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".html"):
                    filepath = os.path.join(root, file)
                    matches = find_matches_in_html(
                        filepath,
                        scope,
                        search_mode,
                        show_lines,
                        seen_h1,
                        line_checker_func=line_checker_func
                    )
                    if matches:
                        results.append(f"{file}: {len(matches)} occurrences")
                        if show_lines:
                            results.extend(matches)

    return results
~~~

## Assistant (gpt-4o)

To adjust your script to focus on "digital transformation" and its variations, we need to identify and list expressions synonymous with "digital transformation." Here’s a quick list of expressions for "digital transformation," including abbreviations:

### Expressions for "Digital Transformation" (Dx)
- Digital transformation
- DX (abbreviation)
- Digital shift
- Digital evolution
- Digital transition
- Digital adaptation
- Digital innovation
- Digital overhaul
- Digital reengineering
- Digital restructuring
- Business digitalization
- Technological transformation
- Digital modernization
- IT-driven change
- Digital pivot
- Digitization of processes

### Updated Script
Below is a modified version of your script that searches for "digital transformation" and its variations instead of "generative AI":

#### `Dx_word_counter.py`
```python
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
        "digital transformation", "dx", "digital shift", "digital evolution",
        "digital transition", "digital adaptation", "digital innovation",
        "digital overhaul", "digital reengineering", "digital restructuring",
        "business digitalization", "technological transformation", 
        "digital modernization", "it-driven change", "digital pivot",
        "digitization of processes"
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
            "digital shift",
            "digital evolution",
            "digital transition",
            "digital adaptation",
            "digital innovation",
            "digital overhaul",
            "digital reengineering",
            "digital restructuring",
            "business digitalization",
            "technological transformation",
            "digital modernization",
            "it-driven change",
            "digital pivot",
            "digitization of processes"
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
```

### Key Adjustments
1. **List of Search Terms:**
   - Added `dx_variants` to include all variations of "digital transformation."
2. **Function Rename:**
   - Changed `line_contains_search_terms_genai` to `line_contains_search_terms_dx`.
3. **Search Variants:**
   - Updated the logic to check against the new list of terms.
4. **Argument Parsing:**
   - Updated the choices in the `--search` argument to match the new list of terms.

This version of the script will search for all terms related to "digital transformation" instead of "generative AI."

