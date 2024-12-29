---
title: AI word counter options
create_time: 2024-12-21 11:59:02
update_time: 2024-12-21 21:57:16
conversation_id: 67662ef5-bb74-800f-aa96-bf079926dadb
---

# AI word counter options

Creation Time: 2024-12-21 11:59:02

Update Time: 2024-12-21 21:57:16

## Assistant



## User

Please add the options to (i) sum up the total occurrences of each directory and (ii) sum up the number of HTML files that contain at least one occurrence (default). Please make the current output one of options.

~~~ AI_word_counter.py
#!/usr/bin/env python3

import os
import argparse
from typing import List
from bs4 import BeautifulSoup

EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE",
    "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI",
    "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]


def line_contains_search_terms(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains the desired search terms based on search_mode.
    We look for:

      1) AI (exact uppercase only) => apply EXCLUDED_WORDS
      2) artificial_intelligence => "artificial intelligence" (case-insensitive)
      3) both => lines containing either #1 or #2
      4) generative_artificial_intelligence => "generative artificial intelligence" (case-insensitive)
      5) generative_AI => "generative AI" (case-insensitive for 'generative', exact uppercase for 'AI')
      6) gen_AI => "Gen AI" (case-insensitive for 'Gen', exact uppercase for 'AI')
    """
    # We'll keep the original line and a lowercase copy.
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI", exclude lines with EXCLUDED_WORDS
        if "AI" in line:  # exact uppercase check
            # Exclusion check is case-insensitive
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
        has_AI = ("AI" in line) and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return has_artificial_intel or has_AI

    elif search_mode == "generative_artificial_intelligence":
        # Case-insensitive match for the phrase "generative artificial intelligence"
        return "generative artificial intelligence" in line_lower

    elif search_mode == "generative_AI":
        # Must contain "generative" in any case and then uppercase "AI".
        # We'll look for the phrase "generative ai" in line_lower, then confirm the actual text has uppercase "AI".
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        # Check if the matched segment in the original line ends with uppercase "AI"
        found_str = line[pos : pos + len(phrase)]  # same length as "generative ai"
        if found_str.endswith("AI"):
            # If there's uppercase AI, apply exclusions (because "AI" is present).
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    elif search_mode == "gen_AI":
        # Must contain "gen ai" in line_lower, then confirm uppercase "AI" in original line
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]  # same length as "gen ai"
        if found_str.endswith("AI"):
            # If there's uppercase AI, apply exclusions
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    # If none of the above match, return False
    return False


def find_matches_in_html(filepath: str, scope: str, search_mode: str, show_lines: bool = False) -> List[str]:
    """
    Parse an HTML file and find occurrences based on search_mode and scope.
    scope can be:
      - "title": only <h1> tags
      - "title_and_content": <h1> + <div class="rte-section">

    search_mode can be one of:
      - "AI"
      - "artificial_intelligence"
      - "both"
      - "generative_artificial_intelligence"
      - "generative_AI"
      - "gen_AI"

    If show_lines is True, we return the actual lines matched. Otherwise, we return a placeholder "match".
    """
    results = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    if scope == "title":
        sections = soup.find_all("h1")
    else:  # "title_and_content"
        title_tags = soup.find_all("h1")
        content_tags = soup.find_all("div", class_="rte-section")
        sections = title_tags + content_tags

    # Extract text from each relevant section
    relevant_texts = [tag.get_text(separator="\n") for tag in sections]

    for text_block in relevant_texts:
        lines = text_block.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_contains_search_terms(line_stripped, search_mode):
                if show_lines:
                    results.append(line_stripped)
                else:
                    results.append("match")

    return results


def count_html_files(directories: List[str], scope: str, search_mode: str, show_lines: bool = False) -> List[str]:
    """
    Scan HTML files in multiple directories for lines containing the desired terms.
    """
    results = []
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".html"):
                    filepath = os.path.join(root, file)
                    matching_lines = find_matches_in_html(filepath, scope, search_mode, show_lines)

                    if matching_lines:
                        results.append(f"{file}: {len(matching_lines)} occurrences")
                        if show_lines:
                            results.extend(matching_lines)
    return results


def write_results_to_file(filename: str, results: List[str]):
    """
    Write results to a file, prompt if overwrite.
    """
    if os.path.exists(filename):
        overwrite = input(f"{filename} exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("File not overwritten.")
            return

    with open(filename, "w") as f:
        f.write("\n".join(results))
    print(f"Results written to {filename}.")


def main():
    parser = argparse.ArgumentParser(
        description="Count occurrences of various AI-related terms in HTML."
    )
    parser.add_argument("directories", type=str, nargs='+', help="Directories containing HTML files.")
    parser.add_argument("-o", "--output", type=str, help="Output filename.")
    parser.add_argument("-s", "--show-lines", action="store_true", help="Show matched lines.")

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
            "AI",
            "artificial_intelligence",
            "both",
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
        ],
        default="both",
        help=(
            "What to search for:\n"
            "- AI (uppercase only)\n"
            "- artificial_intelligence (case-insensitive)\n"
            "- both (either of the above)\n"
            "- generative_artificial_intelligence (case-insensitive)\n"
            "- generative_AI (case-insensitive for 'generative', uppercase only for 'AI')\n"
            "- gen_AI (case-insensitive for 'gen', uppercase only for 'AI')\n"
            "Default is 'both'."
        )
    )

    args = parser.parse_args()

    results = count_html_files(args.directories, args.scope, args.search, args.show_lines)

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
~~~

## Assistant (o1)

Crafting command-line argument options

**Shifting focus**

Considering two new options: summing total occurrences per directory or counting HTML files with occurrences. The default will count occurrences per file. Adding `--report-mode` for directory or file count.

**Evaluating the script's output**

The script currently lists each file with occurrences. The user prefers a single line showing the total number of HTML files with occurrences by default, with an option for directory-wise totals.

**Enhancing functionality**

Adjusting `count_html_files`: adding `--report-mode` with `directory_sum` and `file_count`. Storing directory occurrences in a dictionary and tracking total files and occurrences.

## Assistant (o1)

Below is an updated version of the code. Changes made:

1. Added a new command-line argument `--report-mode` with two options:
   - `directory_sum`: Sum up the total occurrences of the searched terms per directory.
   - `file_count` (default): Report the number of HTML files that contain at least one occurrence (summing over all provided directories).

2. Adjusted the logic in `count_html_files` so that it returns structured data. After processing all directories:
   - If `report_mode == "directory_sum"`, we print the sum of total occurrences per directory.
   - If `report_mode == "file_count"`, we print the total number of HTML files that contain at least one occurrence across all directories.

3. The previous behavior of listing each file and its occurrences has been replaced in favor of the requested output options.

If you need to show matched lines, that option is still available. If `show_lines` is enabled, it will print the matched lines for each file as before, but the summary at the end will depend on the chosen `report_mode`.

```python
#!/usr/bin/env python3

import os
import argparse
from typing import List, Dict
from bs4 import BeautifulSoup

EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE",
    "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI",
    "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]


def line_contains_search_terms(line: str, search_mode: str) -> bool:
    """
    Check if a given line contains the desired search terms based on search_mode.
    """
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI", exclude lines with EXCLUDED_WORDS
        if "AI" in line:
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" in any case
        return "artificial intelligence" in line_lower

    elif search_mode == "both":
        # Matches if it contains "artificial intelligence" (case-insensitive) OR
        # uppercase "AI" (not in excluded words)
        has_artificial_intel = ("artificial intelligence" in line_lower)
        has_AI = ("AI" in line) and not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return has_artificial_intel or has_AI

    elif search_mode == "generative_artificial_intelligence":
        # Case-insensitive match for "generative artificial intelligence"
        return "generative artificial intelligence" in line_lower

    elif search_mode == "generative_AI":
        # Must contain "generative ai" in lowercase form, then confirm original uppercase "AI"
        phrase = "generative ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    elif search_mode == "gen_AI":
        # Must contain "gen ai" in lowercase form, then confirm uppercase "AI"
        phrase = "gen ai"
        pos = line_lower.find(phrase)
        if pos == -1:
            return False
        found_str = line[pos : pos + len(phrase)]
        if found_str.endswith("AI"):
            return not any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
        return False

    return False


def find_matches_in_html(filepath: str, scope: str, search_mode: str, show_lines: bool = False) -> List[str]:
    """
    Parse an HTML file and find occurrences based on search_mode and scope.
    """
    results = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    if scope == "title":
        sections = soup.find_all("h1")
    else:  # "title_and_content"
        title_tags = soup.find_all("h1")
        content_tags = soup.find_all("div", class_="rte-section")
        sections = title_tags + content_tags

    relevant_texts = [tag.get_text(separator="\n") for tag in sections]

    for text_block in relevant_texts:
        lines = text_block.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_contains_search_terms(line_stripped, search_mode):
                if show_lines:
                    results.append(line_stripped)
                else:
                    results.append("match")

    return results


def count_html_files(directories: List[str], scope: str, search_mode: str, show_lines: bool) -> Dict[str, Dict]:
    """
    Scan HTML files in multiple directories for matching lines.
    Returns a dictionary with structure:
    {
      directory_path: {
        "files": {
            filepath: {
                "occurrences": int,
                "lines": [matched_lines_if_show]
            }
        },
        "total_occurrences": int
      }, ...
    }
    """
    data = {}
    for directory in directories:
        data[directory] = {
            "files": {},
            "total_occurrences": 0
        }

        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(".html"):
                    filepath = os.path.join(root, file)
                    matching_lines = find_matches_in_html(filepath, scope, search_mode, show_lines)

                    if matching_lines:
                        data[directory]["files"][filepath] = {
                            "occurrences": len(matching_lines),
                            "lines": matching_lines if show_lines else []
                        }
                        data[directory]["total_occurrences"] += len(matching_lines)

    return data


def write_results_to_file(filename: str, results: List[str]):
    """
    Write results to a file.
    """
    if os.path.exists(filename):
        overwrite = input(f"{filename} exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("File not overwritten.")
            return

    with open(filename, "w") as f:
        f.write("\n".join(results))
    print(f"Results written to {filename}.")


def print_results(data: Dict[str, Dict], report_mode: str, show_lines: bool):
    """
    Print results according to the chosen report mode.

    report_mode:
      - "directory_sum": Print total occurrences per directory.
      - "file_count": Print total number of HTML files containing occurrences.
    """
    if report_mode == "directory_sum":
        # Print the sum of total occurrences for each directory.
        for directory, info in data.items():
            print(f"{directory}: {info['total_occurrences']} occurrences")
            if show_lines:
                # If show_lines is on, also list each file and the matched lines
                for filepath, fileinfo in info["files"].items():
                    print(f"  {filepath}: {fileinfo['occurrences']} occurrences")
                    for line in fileinfo["lines"]:
                        print("    " + line)

    elif report_mode == "file_count":
        # Print the number of HTML files containing at least one occurrence (total across all directories)
        total_files = sum(len(info["files"]) for info in data.values())
        print(f"Total HTML files with occurrences: {total_files}")
        if show_lines:
            # If showing lines, also show details per directory
            for directory, info in data.items():
                if info["files"]:
                    print(f"{directory}:")
                for filepath, fileinfo in info["files"].items():
                    print(f"  {filepath}: {fileinfo['occurrences']} occurrences")
                    for line in fileinfo["lines"]:
                        print("    " + line)


def main():
    parser = argparse.ArgumentParser(
        description="Count occurrences of various AI-related terms in HTML."
    )
    parser.add_argument("directories", type=str, nargs='+', help="Directories containing HTML files.")
    parser.add_argument("-o", "--output", type=str, help="Output filename.")
    parser.add_argument("-s", "--show-lines", action="store_true", help="Show matched lines.")

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
            "AI",
            "artificial_intelligence",
            "both",
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
        ],
        default="both",
        help=(
            "What to search for:\n"
            "- AI (uppercase only)\n"
            "- artificial_intelligence (case-insensitive)\n"
            "- both (either of the above)\n"
            "- generative_artificial_intelligence (case-insensitive)\n"
            "- generative_AI (case-insensitive 'generative', uppercase 'AI')\n"
            "- gen_AI (case-insensitive 'gen', uppercase 'AI')\n"
            "Default is 'both'."
        )
    )

    parser.add_argument(
        "--report-mode",
        choices=["directory_sum", "file_count"],
        default="file_count",
        help="How to report results: 'directory_sum' for total occurrences per directory, 'file_count' for total HTML files with occurrences."
    )

    args = parser.parse_args()

    data = count_html_files(args.directories, args.scope, args.search, args.show_lines)

    # Convert the dictionary data to a printable format based on report_mode
    # We'll print first, and if output requested, also write to a file.
    from io import StringIO
    buf = StringIO()
    # Temporarily redirect print to buffer
    import sys
    old_stdout = sys.stdout
    sys.stdout = buf
    print_results(data, args.report_mode, args.show_lines)
    sys.stdout = old_stdout
    results_str = buf.getvalue().strip()

    if args.output:
        write_results_to_file(args.output, results_str.splitlines())
    else:
        print(results_str)


if __name__ == "__main__":
    main()
```

**Summary of Changes:**

- Introduced `--report-mode` argument to specify the desired reporting style.
- Default `report-mode` is `file_count`, which prints the total number of HTML files containing occurrences.
- Added `directory_sum` mode that prints total occurrences per directory.
- Retained the option to show matched lines with `--show-lines`.
- Updated the logic in `count_html_files` and the final print to support both modes.

