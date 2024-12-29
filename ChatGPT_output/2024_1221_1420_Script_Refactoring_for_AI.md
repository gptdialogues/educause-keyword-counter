---
title: Script Refactoring for AI
create_time: 2024-12-21 14:20:17
update_time: 2024-12-21 14:55:16
conversation_id: 67665011-1eb8-800f-90d0-1fd84a8ac58c
---

# Script Refactoring for AI

Creation Time: 2024-12-21 14:20:17

Update Time: 2024-12-21 14:55:16

## Assistant



## User

Please refactor the following python3 script by separating the "generative_artificial_intelligence", "gen_AI", and "genAI" as a different script (please suggest script names), and generate a shared script for common functions:

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
      7) genAI => "GenAI" (case-insensitive for 'Gen', exact uppercase for 'AI')
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

    elif search_mode == "genAI":
        # Must contain "gen ai" in line_lower, then confirm uppercase "AI" in original line
        phrase = "genai"
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


def find_matches_in_html(filepath: str, scope: str, search_mode: str, show_lines: bool = False, seen_h1: set = None) -> List[str]:
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
      - "genAI"

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

    if seen_h1 is not None:
        # Check if <h1> content has been seen before
        h1_texts = [tag.get_text(separator="\n").strip() for tag in soup.find_all("h1")]
        for h1_text in h1_texts:
            if h1_text in seen_h1:
                return []  # Skip processing if duplicate <h1> content
            seen_h1.add(h1_text)

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


def count_html_files(directories: List[str], scope: str, search_mode: str, show_lines: bool = False, skip_duplicates: bool = False) -> List[str]:
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
                    matching_lines = find_matches_in_html(filepath, scope, search_mode, show_lines, seen_h1)

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
        "--skip-duplicates", action="store_true", help="Skip files with duplicate <h1> content."
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
            "AI",
            "artificial_intelligence",
            "both",
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
            "genAI",
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
            "- genAI (case-insensitive for 'gen', uppercase only for 'AI')\n"
            "Default is 'both'."
        )
    )

    args = parser.parse_args()

    results = count_html_files(
        args.directories, args.scope, args.search, args.show_lines, args.skip_duplicates
    )

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
~~~

## Assistant (o1)

**Mapping out the structure**

I’m planning to separate functions related to "generative_artificial_intelligence", "gen_AI", and "genAI" into a new script. Considering a script name like "generative_AI_modes.py" for these.

**Crafting suitable names**

I’m thinking "generative_search.py" or "generative_search_modes.py" might work well for the script. Splitting "generative_AI" from the main script seems crucial, with possibly "generative_ai_functions.py" as the dedicated name.

**Mapping common functions**

Piecing together a shared script for common functions like "line_contains_search_terms" seems crucial. This approach effectively keeps things organized and accessible for further integration.

**Organizing common functions**

I’m setting up "common_utils.py" to house shared functions like `EXCLUDED_WORDS` and `line_contains_search_terms`, while placing logic functions in specific scripts for clarity and ease of access.

**Distributing tasks**

I'm assigning `EXCLUDED_WORDS` and basic checks to common_utils.py. More specific checks like `check_ai` and `check_artificial_intelligence` will go into ai_search_utils.py, ensuring clarity and ease of access.

**Isolating generative logic**

I’m streamlining code by extracting "generative_artificial_intelligence" and similar logic into "generative_ai_checks.py". Functions like `check_generative_artificial_intelligence` simplify specific search modes, enhancing maintainability.

**Organizing the scripts**

I’m visualizing a clear structure: `common_utils.py` for shared functions, `generative_search.py` for generative AI logic, and `AI_word_counter.py` for the main file, ensuring a logical and scalable progression.

**Separating generative AI**

I’m thinking through the idea of splitting out `generative_AI` since it aligns closely with the other generative groups. This keeps the main script focused and well-organized.

**Organizing functions**

I’m planning to create a new script for generative AI logic, defining functions like `check_generative_artificial_intelligence`, and a shared script for common functions such as `EXCLUDED_WORDS`.

**Refining script structure**

I’m mapping out the scripts: `common_functions.py` for shared functions, `generative_ai_search.py` for generative AI logic, and updating `AI_word_counter.py` to incorporate these new scripts and functions.

## Assistant (o1)

Below is an example refactoring that moves the *generative* search logic (“generative_artificial_intelligence”, “generative_AI”, “gen_AI”, and “genAI”) into a **separate script**, along with creating a **shared script** for common helper functions (e.g., the exclusion words, the “already-excluded?” checker). The main **AI_word_counter.py** script remains the entry point, orchestrating the overall logic.

---

## Suggested File Layout

1. **`common_functions.py`**  
   Holds shared constants/functions, such as `EXCLUDED_WORDS` and any helper function(s) related to case-insensitive matching or checking exclusions.

2. **`generative_ai_search.py`**  
   Contains the logic for detecting “generative_artificial_intelligence”, “generative_AI”, “gen_AI”, and “genAI”. 

3. **`AI_word_counter.py`**  
   The main script, which still has:
   - The argument parser and `main()` function
   - The other non-generative search modes (`AI`, `artificial_intelligence`, `both`)
   - The scanning/HTML-parsing logic

You can tweak script names as you see fit. Below is one possible implementation.

---

## `common_functions.py`

```python
#!/usr/bin/env python3

# Shared script for common constants and functions

EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE",
    "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI",
    "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]


def is_excluded(line_lower: str) -> bool:
    """
    Return True if this line should be excluded based on EXCLUDED_WORDS.
    (We do a case-insensitive check for any excluded word in the line.)
    """
    return any(excl.lower() in line_lower for excl in EXCLUDED_WORDS)
```

---

## `generative_ai_search.py`

```python
#!/usr/bin/env python3
from common_functions import is_excluded

def check_generative_artificial_intelligence(line: str, line_lower: str) -> bool:
    """
    For 'generative_artificial_intelligence', we look for the phrase
    'generative artificial intelligence' (case-insensitive).
    """
    return "generative artificial intelligence" in line_lower


def check_generative_AI(line: str, line_lower: str) -> bool:
    """
    For 'generative_AI':
      - Must contain "generative" in any case AND "AI" in uppercase.
      - We'll first look for "generative ai" in line_lower, then confirm
        that in the original line it ends with uppercase "AI".
      - Also check exclusions (because 'AI' is present).
    """
    phrase = "generative ai"
    pos = line_lower.find(phrase)
    if pos == -1:
        return False
    found_str = line[pos : pos + len(phrase)]  # same length as "generative ai"
    if found_str.endswith("AI") and not is_excluded(line_lower):
        return True
    return False


def check_gen_AI(line: str, line_lower: str) -> bool:
    """
    For 'gen_AI':
      - Must contain "gen ai" in line_lower, then confirm uppercase "AI" in original line.
      - Also check exclusions (because 'AI' is present).
    """
    phrase = "gen ai"
    pos = line_lower.find(phrase)
    if pos == -1:
        return False
    found_str = line[pos : pos + len(phrase)]
    if found_str.endswith("AI") and not is_excluded(line_lower):
        return True
    return False


def check_genAI(line: str, line_lower: str) -> bool:
    """
    For 'genAI':
      - Must contain "genai" in line_lower, then confirm uppercase "AI" in original line.
      - Also check exclusions (because 'AI' is present).
    """
    phrase = "genai"
    pos = line_lower.find(phrase)
    if pos == -1:
        return False
    found_str = line[pos : pos + len(phrase)]
    if found_str.endswith("AI") and not is_excluded(line_lower):
        return True
    return False
```

---

## `AI_word_counter.py`

Below is the main script, updated to:

1. Import the shared functions from **`common_functions.py`** and the generative checks from **`generative_ai_search.py`**.
2. Remove the inline code for the generative search modes in `line_contains_search_terms` and delegate to the new “generative_ai_search” functions.
3. Keep the rest of the logic as-is (i.e., for `AI`, `artificial_intelligence`, `both`).

```python
#!/usr/bin/env python3

import os
import argparse
from typing import List
from bs4 import BeautifulSoup

# Import from our new scripts
from common_functions import EXCLUDED_WORDS, is_excluded
from generative_ai_search import (
    check_generative_artificial_intelligence,
    check_generative_AI,
    check_gen_AI,
    check_genAI,
)


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
      7) genAI => "GenAI" (case-insensitive for 'Gen', exact uppercase for 'AI')
    """
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI", exclude lines with EXCLUDED_WORDS
        if "AI" in line:  # exact uppercase check
            return not is_excluded(line_lower)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" in any case
        return "artificial intelligence" in line_lower

    elif search_mode == "both":
        # A line matches if it contains:
        #   - "artificial intelligence" (case-insensitive), OR
        #   - "AI" (uppercase only) not in EXCLUDED_WORDS
        has_artificial_intel = ("artificial intelligence" in line_lower)
        has_AI = ("AI" in line) and not is_excluded(line_lower)
        return has_artificial_intel or has_AI

    elif search_mode == "generative_artificial_intelligence":
        return check_generative_artificial_intelligence(line, line_lower)

    elif search_mode == "generative_AI":
        return check_generative_AI(line, line_lower)

    elif search_mode == "gen_AI":
        return check_gen_AI(line, line_lower)

    elif search_mode == "genAI":
        return check_genAI(line, line_lower)

    # If none of the above match, return False
    return False


def find_matches_in_html(
    filepath: str,
    scope: str,
    search_mode: str,
    show_lines: bool = False,
    seen_h1: set = None
) -> List[str]:
    """
    Parse an HTML file and find occurrences based on search_mode and scope.
    scope can be:
      - "title": only <h1> tags
      - "title_and_content": <h1> + <div class="rte-section">
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

    if seen_h1 is not None:
        # Check if <h1> content has been seen before
        h1_texts = [tag.get_text(separator="\n").strip() for tag in soup.find_all("h1")]
        for h1_text in h1_texts:
            if h1_text in seen_h1:
                return []  # Skip processing if duplicate <h1> content
            seen_h1.add(h1_text)

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


def count_html_files(
    directories: List[str],
    scope: str,
    search_mode: str,
    show_lines: bool = False,
    skip_duplicates: bool = False
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
                    matching_lines = find_matches_in_html(filepath, scope, search_mode, show_lines, seen_h1)

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
        "--skip-duplicates", action="store_true", help="Skip files with duplicate <h1> content."
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
            "AI",
            "artificial_intelligence",
            "both",
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
            "genAI",
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
            "- genAI (case-insensitive for 'gen', uppercase only for 'AI')\n"
            "Default is 'both'."
        )
    )

    args = parser.parse_args()

    results = count_html_files(
        args.directories,
        args.scope,
        args.search,
        args.show_lines,
        args.skip_duplicates
    )

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
```

---

### Notes & Customizations

1. **Script Names**  
   - Feel free to rename `common_functions.py` to `shared_utils.py` or something else.  
   - Likewise, `generative_ai_search.py` can be `generative_modes.py`, etc.

2. **Exclusions**  
   - We placed `EXCLUDED_WORDS` and the `is_excluded` checker in `common_functions.py` so that both non-generative and generative searches can reference them.

3. **Import Paths**  
   - Ensure that all three scripts are in the same directory (or otherwise adjust Python’s import paths accordingly).

With this refactoring, any future expansions to the generative search modes can simply be added to **`generative_ai_search.py`** without cluttering the main script. Meanwhile, the main script (`AI_word_counter.py`) stays focused on orchestrating file traversal, HTML parsing, and command-line argument handling.

## User

Please refactor the following python3 script by generating `GenAI_word_counter.py` extracting the functionality for the search_mode "generative_artificial_intelligence", "gen_AI", and "genAI" and generate a shared script `common_functions.py`. `AI_word_counter.py` and `GenAI_word_counter.py` should not be a parent and child relationship but should be in an equal level.

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
      7) genAI => "GenAI" (case-insensitive for 'Gen', exact uppercase for 'AI')
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

    elif search_mode == "genAI":
        # Must contain "gen ai" in line_lower, then confirm uppercase "AI" in original line
        phrase = "genai"
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


def find_matches_in_html(filepath: str, scope: str, search_mode: str, show_lines: bool = False, seen_h1: set = None) -> List[str]:
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
      - "genAI"

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

    if seen_h1 is not None:
        # Check if <h1> content has been seen before
        h1_texts = [tag.get_text(separator="\n").strip() for tag in soup.find_all("h1")]
        for h1_text in h1_texts:
            if h1_text in seen_h1:
                return []  # Skip processing if duplicate <h1> content
            seen_h1.add(h1_text)

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


def count_html_files(directories: List[str], scope: str, search_mode: str, show_lines: bool = False, skip_duplicates: bool = False) -> List[str]:
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
                    matching_lines = find_matches_in_html(filepath, scope, search_mode, show_lines, seen_h1)

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
        "--skip-duplicates", action="store_true", help="Skip files with duplicate <h1> content."
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
            "AI",
            "artificial_intelligence",
            "both",
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
            "genAI",
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
            "- genAI (case-insensitive for 'gen', uppercase only for 'AI')\n"
            "Default is 'both'."
        )
    )

    args = parser.parse_args()

    results = count_html_files(
        args.directories, args.scope, args.search, args.show_lines, args.skip_duplicates
    )

    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
~~~

## Assistant (o1)

**Refactoring the code**

I'm working through refactoring `AI_word_counter.py` by shifting generative AI functionalities to `GenAI_word_counter.py` and creating a `common_functions.py` for shared tasks.

**Revisiting search modes**

Piecing together `AI_word_counter.py` and `GenAI_word_counter.py`, I’m considering which search modes to include for each. `Common_functions.py` will house shared code, possibly storing entire functions.

**Revisiting search modes**

I’m pulling different strategies to manage search modes in `GenAI_word_counter.py` and `common_functions.py`. Each mode might need dedicated functions for accurate handling. Progress is steady but ongoing.

**Mapping out script structure**

Balancing common functions, aligning search modes, and ensuring `AI_word_counter.py` and `GenAI_word_counter.py` focus on their respective search modes. Now we're aligning our strategies.

**Organizing shared logic**

Mapping out `common_functions.py` to host functions like `find_matches_in_html()` and `count_html_files()`. This setup simplifies imports in `AI_word_counter.py` and `GenAI_word_counter.py`.

**Building functions**

I’m focusing on `common_functions.py` to house `find_matches_in_html()`, `count_html_files()`, and `write_results_to_file()`, with a unified `line_contains_search_terms(line, search_mode)` function.

**Crafting separate scripts**

I’m working on `AI_word_counter.py` for AI modes and `GenAI_word_counter.py` for generative modes, ensuring precise argument parsing and function calls to maintain their functionalities.

**Breaking down the function**

I'm thinking through whether to split `line_contains_search_terms()` into AI and generative AI functions in `common_functions.py`. This approach ensures clarity and prevents code overlap.

**Clarifying function focus**

I’m working through crafting distinct functions for AI and generative AI modes in `common_functions.py`. This approach ensures precise search mode handling, simplifying maintenance and testing.

**Crafting separate functions**

I’m organizing `line_contains_search_terms_ai()` and `line_contains_search_terms_genAI()` to handle AI and generative AI codes. This will simplify management and ensure clear functional boundaries.

**Clarifying function hierarchy**

I'm ensuring `GenAI_word_counter.py` imports from `common_functions.py` and maintaining equal levels of functionality for both scripts. This keeps things organized and well-defined.

**Organizing code modules**

I’m focusing on creating `GenAI_word_counter.py` for generative modes, `AI_word_counter.py` for AI modes, and `common_functions.py` for shared code, ensuring clarity and functionality across scripts.

**Establishing equal hierarchy**

I'm setting up `AI_word_counter.py` and `GenAI_word_counter.py` as peers, with `common_functions.py` for shared functions. This ensures clear and balanced functionality across the board.

**Organizing search modes**

I'm working through splitting generative and AI search modes into separate codes, with shared functionality to ensure each area is distinctly and effectively represented.

**Mapping out shared code**

I’m crafting `common_functions.py` to boost modularity, incorporating HTML file functions and search terms. This setup simplifies `AI_word_counter.py` by passing a specific function for line analysis.

## Assistant (o1)

Below is an example refactoring into three files:

1. **`common_functions.py`**  
   A shared library containing:
   - The `EXCLUDED_WORDS` list (so both scripts stay consistent).  
   - A `find_matches_in_html` function that can accept a “line checker” function as a parameter.  
   - A `count_html_files` function that likewise accepts the checker function.  
   - A `write_results_to_file` utility.  

2. **`AI_word_counter.py`**  
   A script that includes:
   - A **restricted** set of search modes for “AI”-related text only (e.g., `AI`, `artificial_intelligence`, `both`).  
   - A `line_contains_search_terms_ai` function that handles only those modes.  
   - A `main` function and argument parsing.  
   - It imports from `common_functions.py` and passes `line_contains_search_terms_ai` into `count_html_files`.  

3. **`GenAI_word_counter.py`**  
   A script that includes:
   - The **generative** search modes (`generative_artificial_intelligence`, `generative_AI`, `gen_AI`, `genAI`).  
   - A `line_contains_search_terms_genai` function that handles only those modes.  
   - A `main` function and argument parsing.  
   - It imports from `common_functions.py` and passes `line_contains_search_terms_genai` into `count_html_files`.  

This way, **`AI_word_counter.py` and `GenAI_word_counter.py` are at the same level** and share no parent/child relationship. Both rely on `common_functions.py` for I/O and HTML parsing logic.  

---

## `common_functions.py`

```python
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
            if h1_text in seen_h1:
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
```

---

## `AI_word_counter.py`

```python
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
    # We'll keep the original line and a lowercase copy.
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
```

---

## `GenAI_word_counter.py`

```python
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
    'generative AI', 'gen AI', or 'genAI'.
    """
    line_lower = line.lower()

    if search_mode == "generative_artificial_intelligence":
        # Case-insensitive match for the phrase "generative artificial intelligence"
        return "generative artificial intelligence" in line_lower

    elif search_mode == "generative_AI":
        # Must contain "generative" in any case and then uppercase "AI".
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
            "generative_artificial_intelligence",
            "generative_AI",
            "gen_AI",
            "genAI"
        ],
        default="generative_artificial_intelligence",
        help=(
            "What to search for:\n"
            "- generative_artificial_intelligence\n"
            "- generative_AI (case-insensitive for 'generative', uppercase 'AI')\n"
            "- gen_AI (case-insensitive for 'gen', uppercase 'AI')\n"
            "- genAI (case-insensitive for 'gen', uppercase 'AI')\n"
            "Default is 'generative_artificial_intelligence'."
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
```

---

### How This Refactoring Works

- **`common_functions.py`**:  
  - Houses shared code for parsing HTML, iterating directories, checking for duplicates, writing output, and holding the global `EXCLUDED_WORDS` list.  
  - Uses a `line_checker_func` parameter so that either `AI_word_counter.py` or `GenAI_word_counter.py` can inject their own line-checking logic for relevant search modes.

- **`AI_word_counter.py`**:  
  - Implements `line_contains_search_terms_ai`, which only knows about the “AI” (uppercase), “artificial intelligence,” or “both” search modes.  
  - Has its own `argparse` logic restricting the `--search` argument to those modes.  
  - Passes `line_contains_search_terms_ai` to `count_html_files`.

- **`GenAI_word_counter.py`**:  
  - Implements `line_contains_search_terms_genai`, which only knows about “generative artificial intelligence,” “generative AI,” “gen AI,” and “genAI.”  
  - Has its own `argparse` logic restricting the `--search` argument to those modes.  
  - Passes `line_contains_search_terms_genai` to `count_html_files`.

This separation keeps **`AI_word_counter.py`** and **`GenAI_word_counter.py`** at the same level (siblings), sharing common logic but each specializing in its own set of search modes.

## User

Please add "all" for the default option of `--search` which includes the search_modes "generative_artificial_intelligence", "generative_AI", "gen_AI", and "genAI" to `GenAI_word_counter.py`.

## Assistant (o1)

**Weighing options**

I'm considering modifying line_contains_search_terms_genai to handle the new "all" mode, which supports variants like generative_artificial_intelligence, generative_AI, gen_AI, or genAI. This approach seems straightforward and efficient.

**Updating the parser**

I'm updating the parser to include a new "all" search mode, which methodically checks for each variant of generative intelligence terms, ensuring comprehensive coverage.

**Updating the parser**

I’m adding an "all" search mode to the parser and noting that `line_contains_search_terms_genai` should sequentially check for each generative intelligence term to ensure comprehensive coverage.

**Piecing together the strategy**

I’m digging into a method to check for all generative intelligence terms without recursion. This involves inlining the logic for each term, ensuring clarity and consistency with existing code.

## Assistant (o1)

Below is an updated version of **`GenAI_word_counter.py`** which adds a **new** search mode called `"all"` for the default option. When `"all"` is chosen, it will flag **any line** that matches **any** of the following four patterns:

1. `"generative artificial intelligence"`  
2. `"generative AI"`  
3. `"gen AI"`  
4. `"genAI"`

You can simply replace your existing **`GenAI_word_counter.py`** with the one below. The rest of your codebase (**`common_functions.py`** and **`AI_word_counter.py`**) remain the same.

---

```python
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
```

---

### What Changed?

1. **New Search Mode**:  
   We added `"all"` to the `--search` argument, making it the **default**. This means if no specific search mode is passed, the script will look for **all** generative-related terms:  
   - `"generative artificial intelligence"` (case-insensitive)  
   - `"generative AI"` (case-insensitive for “generative,” exact uppercase “AI”)  
   - `"gen AI"` (case-insensitive for “gen,” exact uppercase “AI”)  
   - `"genAI"` (case-insensitive for “gen,” exact uppercase “AI”)  

2. **Line-Checking Logic**:  
   For `"all"`, we explicitly check each possible pattern in a single combined block. If **any** of them matches, we immediately return `True`. Otherwise, we return `False`.

3. **Default Behavior**:  
   By setting the default to `"all"`, running the script without `--search` now searches for every kind of “generative AI” term in a single pass.

## User

Please update `AI_word_counter.py` to make "both" the default option for `--search`.

## Assistant (o1)



## Assistant (o1)

Below is an updated snippet for **`AI_word_counter.py`** with `"both"` set as the default option for `--search`.  

```python
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
        default="both",  # <-- "both" is now the default
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
```

