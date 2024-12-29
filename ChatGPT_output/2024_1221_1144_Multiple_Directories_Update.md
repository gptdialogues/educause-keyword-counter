---
title: Multiple Directories Update
create_time: 2024-12-21 11:44:27
update_time: 2024-12-21 11:44:56
conversation_id: 67662b8b-98b8-800f-b26c-5e2bcd506b85
---

# Multiple Directories Update

Creation Time: 2024-12-21 11:44:27

Update Time: 2024-12-21 11:44:56

## Assistant



## User

Please update the following code to accept multiple directories without any optional flags:
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


def count_html_files(directory: str, scope: str, search_mode: str, show_lines: bool = False) -> List[str]:
    """
    Scan HTML files in a directory for lines containing the desired terms.
    """
    results = []
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
    parser.add_argument("directory", type=str, help="Directory containing HTML files.")
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

    results = count_html_files(args.directory, args.scope, args.search, args.show_lines)

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
~~~

## Assistant (gpt-4o)

To enable the script to accept multiple directories without using optional flags, the script needs to modify the argument parsing logic to interpret multiple positional arguments as directories. Here's the updated code:

## Assistant (gpt-4o)

{"name": "ai_word_counter_update", "type": "code/python", "content": "#!/usr/bin/env python3\n\nimport os\nimport argparse\nfrom typing import List\nfrom bs4 import BeautifulSoup\n\nEXCLUDED_WORDS = [\n    \"SAILS\", \"WebAIM\", \"CampusEAI\", \"MAIS\", \"Kuali\", \"FAIT\", \"RAI\", \"SAIT\", \"FAE\",\n    \"NAIR\", \"AIMS\", \"HAIL\", \"AIR\", \"CFAIT\", \"FAIM\", \"SAIR\", \"PAIR\", \"AIM\", \"OAAI\",\n    \"AITS\", \"AIP\", \"SUSTAIN\", \"EGlIAIHi31\", \"FAILURE\", \"AIF\"\n]\n\ndef line_contains_search_terms(line: str, search_mode: str) -> bool:\n    # Same as before\n    ...\n\ndef find_matches_in_html(filepath: str, scope: str, search_mode: str, show_lines: bool = False) -> List[str]:\n    # Same as before\n    ...\n\ndef count_html_files(directories: List[str], scope: str, search_mode: str, show_lines: bool = False) -> List[str]:\n    \"\"\"\n    Scan HTML files in multiple directories for lines containing the desired terms.\n    \"\"\"\n    results = []\n    for directory in directories:\n        for root, _, files in os.walk(directory):\n            for file in files:\n                if file.lower().endswith(\".html\"):\n                    filepath = os.path.join(root, file)\n                    matching_lines = find_matches_in_html(filepath, scope, search_mode, show_lines)\n\n                    if matching_lines:\n                        results.append(f\"{file}: {len(matching_lines)} occurrences\")\n                        if show_lines:\n                            results.extend(matching_lines)\n    return results\n\ndef write_results_to_file(filename: str, results: List[str]):\n    # Same as before\n    ...\n\ndef main():\n    parser = argparse.ArgumentParser(\n        description=\"Count occurrences of various AI-related terms in HTML.\"\n    )\n    parser.add_argument(\"directories\", type=str, nargs='+', help=\"Directories containing HTML files.\")\n    parser.add_argument(\"-o\", \"--output\", type=str, help=\"Output filename.\")\n    parser.add_argument(\"-s\", \"--show-lines\", action=\"store_true\", help=\"Show matched lines.\")\n\n    parser.add_argument(\n        \"--scope\",\n        choices=[\"title\", \"title_and_content\"],\n        default=\"title_and_content\",\n        help=(\n            \"Which part of the HTML to scan. \"\n            \"'title' scans only <h1>, \"\n            \"'title_and_content' scans <h1> + <div class='rte-section'>.\"\n        )\n    )\n\n    parser.add_argument(\n        \"--search\",\n        choices=[\n            \"AI\",\n            \"artificial_intelligence\",\n            \"both\",\n            \"generative_artificial_intelligence\",\n            \"generative_AI\",\n            \"gen_AI\",\n        ],\n        default=\"both\",\n        help=(\n            \"What to search for:\\n\"\n            \"- AI (uppercase only)\\n\"\n            \"- artificial_intelligence (case-insensitive)\\n\"\n            \"- both (either of the above)\\n\"\n            \"- generative_artificial_intelligence (case-insensitive)\\n\"\n            \"- generative_AI (case-insensitive for 'generative', uppercase only for 'AI')\\n\"\n            \"- gen_AI (case-insensitive for 'gen', uppercase only for 'AI')\\n\"\n            \"Default is 'both'.\"\n        )\n    )\n\n    args = parser.parse_args()\n\n    results = count_html_files(args.directories, args.scope, args.search, args.show_lines)\n\n    if args.output:\n        write_results_to_file(args.output, results)\n    else:\n        print(\"\\n\".join(results))\n\nif __name__ == \"__main__\":\n    main()"}

## Assistant (gpt-4o)

{"result": "Successfully created text document 'ai_word_counter_update' which will be referenced in all future messages with the unique identifier textdoc_id: '67662ba112188191919a883708773c78'", "textdoc_id": "67662ba112188191919a883708773c78", "name": "ai_word_counter_update"}

## Assistant (gpt-4o)

### Key Changes:
1. **Positional Arguments for Multiple Directories**:
   - Replaced the single `directory` argument with `directories` using `nargs='+'` to allow multiple directories.
2. **Modified `count_html_files`**:
   - Adjusted to loop over multiple directories passed as a list.
3. **Updated Documentation**:
   - Reflected changes in the argument help text.

You can now run the script with multiple directories like this:
```bash
python AI_word_counter.py dir1 dir2 dir3 --scope title --search AI
```

