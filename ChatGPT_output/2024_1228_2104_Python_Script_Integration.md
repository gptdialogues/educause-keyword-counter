---
title: Python Script Integration
create_time: 2024-12-28 21:04:33
update_time: 2024-12-28 21:13:36
conversation_id: 676fe951-9690-800f-9de9-a000f5921324
---

# Python Script Integration

Creation Time: 2024-12-28 21:04:33

Update Time: 2024-12-28 21:13:36

## Assistant



## User

Please merge the functionalities of the following python3 scripts and bash scripts as an integrated python3 script.

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

~~~ 1_count_words_2024_1221.sh
#!/bin/bash
main(){
    file="keyword_count.csv"
    csv_output > $file
}

csv_output(){
    echo 'Year,AI,genAI,Dx'
    for year in {2000..2024}; do
        AI_count=`AI_counter $year`
        GenAI_count=`GenAI_counter $year`
        Dx_word_count=`Dx_word_counter $year`
        echo "$year,$AI_count,$GenAI_count,$Dx_word_count"
    done
}

AI_counter(){
    year=$1
    python3 AI_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
    | grep html | wc | awk '{print $1}'
}

GenAI_counter(){
    year=$1
    python3 GenAI_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
    | grep html | wc | awk '{print $1}'
}

Dx_word_counter(){
    year=$1
    python3 Dx_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
    | grep html | wc | awk '{print $1}'
}

main "$@"

~~~

~~~ 2_visualize_counts_2024_1221.sh
./visualize_csv_data.py --start-year 2014 --font-scale 2 d1_count_words_2024_1221.csv

~~~

## Assistant (o1)

**Integrating scripts**

I’m pulling together Python and Bash scripts into one Python file. The Python scripts count words for each year from 2000 to 2024, outputting results to a CSV file. The Bash script visualizes CSV data using "visualize_csv_data.py," which might also be integrated.

**Consolidating scripts**

I'm thinking through combining Python scripts into one, incorporating AI, GenAI, and Dx word counts for each year from 2000 to 2024, and storing results in a CSV file.

**Incorporating functionalities**

I'm mapping out "integrated.py" to include functions from "common_functions.py," "AI_word_counter.py," "Dx_word_counter.py," and "GenAI_word_counter.py," with an optional visualization step for CSV data.

**Piecing together the script**

I’m crafting "merged_word_counter.py" to scan directories for AI, GenAI, and Dx counts from 2000 to 2024, format results into CSV lines, and handle multiple years with an argument parser.

**Shaping the main function**

I'm thinking through the main function to parse arguments, replicate "1_count_words_2024_1221.sh," and generate a CSV file. This involves counting words for each year from 2000 to 2024.

**Tracking counts**

I’m focusing on generating a CSV file to track counts of AI, GenAI, and Dx for each year from 2000 to 2024 using the "1_count_words_2024_1221.sh" script logic.

**Counting matches**

I’m replicating the script's logic to count files with matches, ensuring precision by focusing on the number of lines that contain "html," similar to "grep html" "wc -l."

**Counting matched files**

I’m defining "count_matched_files" to tally files with matches, ensuring accuracy by counting lines ending in "occurrences." This method accurately replicates the grep and wc command logic.

## Assistant (o1)

Below is an example of how you can merge all the functionality from the four Python scripts plus the “loop over years and produce CSV” logic from the Bash scripts into a single integrated Python 3 script. The script:

1. Embeds the common functions (HTML parsing, writing to file, etc.).  
2. Includes the three different “line checker” functions for AI, Dx, and GenAI.  
3. Mimics the Bash script’s behavior of iterating over years and gathering counts (how many *files* match at least once).  
4. Outputs a CSV file of the form:  
   ```
   Year,AI,genAI,Dx
   2000,1,2,3
   ...
   2024,4,5,6
   ```  

Because the visualization script (`visualize_csv_data.py`) was not provided, this integrated script does not replicate the “visualize” step. You could, however, extend this script to add plotting functionality or to call an external visualization module if desired.

> **Save this as** `merged_word_counter.py` (or a name of your choice), make it executable (`chmod +x merged_word_counter.py`), and run it with `python3 merged_word_counter.py --help` to see usage.

---

```python
#!/usr/bin/env python3

import os
import sys
import argparse
from typing import List, Set
from bs4 import BeautifulSoup

###############################################################################
# 1) COMMON FUNCTIONS (from common_functions.py)
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
            # Example line below addresses "Day 2" => "Day 1" from the original
            # (Retaining as-is from your scripts)
            h1_text = h1_text.replace("Day 2", "Day 1")
            if h1_text in seen_h1:
                # If we've seen this <h1> content already, skip processing
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
    Optionally skip files with duplicate <h1> content (i.e. skip entire file if
    an <h1> has already been seen).
    Returns a list of lines like "filename.html: X occurrences" for each file with matches.
    If 'show_lines' is True, includes extra lines for the content of each match.
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
                        # First line indicates "filename.html: X occurrences"
                        results.append(f"{file}: {len(matches)} occurrences")
                        # If show_lines was True, we also append each matched line
                        if show_lines:
                            results.extend(matches)

    return results


###############################################################################
# 2) AI WORD-COUNTER LOGIC (from AI_word_counter.py)
###############################################################################
def line_contains_search_terms_ai(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains the desired search terms for
    'AI', 'artificial_intelligence', or 'both'.
    """
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI" somewhere in the line,
        # and must not contain any of the EXCLUDED_WORDS
        if "AI" in line:  # note: exact uppercase check
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" in any case
        return "artificial intelligence" in line_lower

    elif search_mode == "both":
        # A line matches if it contains:
        #   - "artificial intelligence" (case-insensitive), OR
        #   - "AI" (uppercase only) not in EXCLUDED_WORDS
        has_artificial_intel = "artificial intelligence" in line_lower
        has_ai = (
            "AI" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        )
        return has_artificial_intel or has_ai

    # Fallback
    return False


###############################################################################
# 3) DX WORD-COUNTER LOGIC (from Dx_word_counter.py)
###############################################################################
def line_contains_search_terms_dx(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains 'digital transformation',
    'Dx' (case-sensitive), or both.
    """
    line_lower = line.lower()

    # Example strings to exclude for "Dx"
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
        # Case-insensitive check for "digital transformation"
        return "digital transformation" in line_lower

    elif search_mode == "all":
        has_digital_transformation = "digital transformation" in line_lower
        has_dx = (
            "Dx" in line
            and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
            and not any(excl in line for excl in dx_exclusions)
        )
        return has_digital_transformation or has_dx

    # Fallback
    return False


###############################################################################
# 4) GENAI WORD-COUNTER LOGIC (from GenAI_word_counter.py)
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
        # found_str should end with uppercase "AI" in the original
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
        # If it matches ANY of the above patterns, return True
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

    # Fallback
    return False


###############################################################################
# 5) FUNCTIONS THAT REPLICATE THE BASH SCRIPTS (1_count_words_2024_1221.sh)
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
    
    Then replicate the logic: 
        ... | grep html | wc | awk '{print $1}'
    i.e. count how many lines of the form "<filename>.html: X occurrences"
    are returned (which effectively is the number of *files* that had at least
    one match).
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

    # Each matched file is indicated by "filename.html: X occurrences"
    # So just count how many lines match that pattern.
    # A simple approach: check if it ends with "occurrences"
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
        # AI: line_contains_search_terms_ai, search_mode='both'
        ai_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_ai,
            search_mode="both"
        )
        # GenAI: line_contains_search_terms_genai, search_mode='all'
        genai_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_genai,
            search_mode="all"
        )
        # Dx: line_contains_search_terms_dx, search_mode='all'
        dx_count = count_files_for_search(
            year=year,
            line_checker_func=line_contains_search_terms_dx,
            search_mode="all"
        )
        csv_lines.append(f"{year},{ai_count},{genai_count},{dx_count}")

    return csv_lines


###############################################################################
# 6) MAIN: Command-line entry point that merges everything.
###############################################################################
def main():
    parser = argparse.ArgumentParser(
        description="Integrated script to count AI/GenAI/Dx occurrences across year-based HTML folders, then produce CSV."
    )
    parser.add_argument(
        "--start-year", 
        type=int, 
        default=2000,
        help="Earliest year to scan (default=2000)."
    )
    parser.add_argument(
        "--end-year", 
        type=int, 
        default=2024,
        help="Latest year to scan (default=2024)."
    )
    parser.add_argument(
        "--output-csv",
        type=str,
        default="keyword_count.csv",
        help="CSV filename for results (default=keyword_count.csv)."
    )
    parser.add_argument(
        "--only-csv",
        action="store_true",
        help="Only produce the CSV counts (do not do any other interactive prompting)."
    )

    args = parser.parse_args()

    # 1) Produce the CSV lines
    csv_data = produce_csv_output(args.start_year, args.end_year)

    # 2) Write them out
    if args.only_csv:
        # Print to stdout
        print("\n".join(csv_data))
    else:
        # Or write to file with an overwrite prompt
        write_results_to_file(args.output_csv, csv_data)


if __name__ == "__main__":
    main()
```

---

### How this integrated script works

- **`count_html_files`** is the core routine that:
  - Recursively scans each directory (like `html_2024`) for `.html` files,
  - Parses HTML with BeautifulSoup,
  - Extracts either `<h1>` or `<h1> + <div class="rte-section">` text (depending on `scope`),
  - Uses a “line checker” function (e.g. `line_contains_search_terms_ai`) to decide if a line matches,
  - Returns a list of strings of the form `["some_file.html: 2 occurrences", ...]` if a file matched.

- **`count_files_for_search(year, line_checker_func, search_mode)`** replicates the Bash scripts’ pattern of:
  
  ```bash
  python3 AI_word_counter.py --scope title_and_content --skip-duplicates html_${year} \
      | grep html | wc | awk '{print $1}'
  ```
  
  i.e. it counts how many *files* had at least one match.

- **`produce_csv_output(start_year, end_year)`** loops over each year in `[start_year..end_year]`, calls the AI, GenAI, and Dx “file counters,” and collects the results into a CSV list of strings.

- **`main()`** ties it all together, providing command-line arguments for selecting the year range and the CSV filename, plus an option (`--only-csv`) to simply emit the CSV lines to stdout.

This single script thus merges:

- *common_functions.py*  
- *AI_word_counter.py*  
- *Dx_word_counter.py*  
- *GenAI_word_counter.py*  
- The Bash script that loops from 2000 to 2024, runs each counter, and writes CSV  

Feel free to modify or extend (e.g., add logging or integrate your own visualization steps).

## User

Please continue merging.

~~~ visualize_csv_data.py
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

~~~

## Assistant (o1)

**Integrating script components**

I'm working through merging the code from `visualize_csv_data.py` into a single integrated Python script, adding visualization capabilities. This includes creating an optional parameter like `--visualize` to output charts.

**Mapping out integration**

I'm thinking through how to embed `visualize_csv_data.py` by defining a `visualize_csv_data` function. Parsing parameters in the main script will trigger chart generation with optional CSV input.

**Preserving options**

I'm working through how to maintain the script's capability for CSV generation while introducing visualization features. This involves expanding the parser to support subcommands, ensuring a seamless user experience.

**Setting up subcommands**

I'm implementing a parser with subcommands for counting and visualizing CSV data. Each subcommand will trigger specific functions, ensuring a smooth user experience with clear functionalities.

**Integrating functionality**

Now I’m merging code from `visualize_csv_data.py` into `do_visualize(args)`. It involves parsing CSV, checking columns, defining markers, and adding helper functions for file management.

## Assistant (o1)

Below is **one** way to merge **all** of the functionality—HTML scanning, word counting (AI, GenAI, Dx), CSV generation over a range of years, **and** CSV data visualization—into a **single** Python script. It uses **subcommands** so you can either:

1. **Generate the CSV** with the “count” subcommand, or  
2. **Visualize** an existing CSV with the “visualize” subcommand.

Feel free to adjust details (e.g., default argument values, prompts, etc.) as needed.

---

```python
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
```

---

### How to Use This Single Script

1. **Make it executable** (optional, on Unix-like systems):
   ```bash
   chmod +x merged_word_counter.py
   ```

2. **Count** matches across your `html_YEAR` directories (e.g. `html_2020`, `html_2021`, etc.), then produce `keyword_count.csv`:
   ```bash
   ./merged_word_counter.py count \
       --start-year 2000 \
       --end-year 2024 \
       --output-csv keyword_count.csv
   ```
   - Or just print CSV to terminal:
     ```bash
     ./merged_word_counter.py count --only-csv
     ```

3. **Visualize** an existing CSV file:
   ```bash
   ./merged_word_counter.py visualize keyword_count.csv \
       --start-year 2014 \
       --output counts_plot.pdf \
       --font-scale 2
   ```
   - This filters rows to years >= 2014, and produces a “counts_plot.pdf” with larger fonts.  

Thus, everything (HTML scanning, counting AI/GenAI/Dx, CSV output, and plotting) is combined into a single integrated Python script. Enjoy!

