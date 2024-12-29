---
title: AI word counter update
create_time: 2024-12-21 10:59:31
update_time: 2024-12-21 11:35:19
conversation_id: 67662103-1160-800f-97ea-af5e8f0f0c95
---

# AI word counter update

Creation Time: 2024-12-21 10:59:31

Update Time: 2024-12-21 11:35:19

## Assistant



## User

Please add options to the following code to find "AI" (i) only from the title of the presentation (specified by the "h1" tag) and (ii) from the title and content (specified by the tag "rte-section"). I attached an example HTML content.

~~~ AI_word_counter.py
#!/usr/bin/env python3

import os
import argparse
from typing import List

# List of words containing 'AI' that do not mean 'artificial intelligence'
EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE", "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI", "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]

def count_html_files_with_ai(directory: str, show_lines: bool = False) -> List[str]:
    """
    Count and optionally display lines containing "AI" in HTML files.
    Exclude lines with words from the EXCLUDED_WORDS list.

    Args:
        directory (str): Path to the directory containing HTML files.
        show_lines (bool): Whether to display the lines containing "AI".

    Returns:
        List[str]: Results showing file names and matching lines if requested.
    """
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                matching_lines = [
                    line.strip() for line in lines
                    if "AI" in line and not any(word in line for word in EXCLUDED_WORDS)
                ]

                if matching_lines:
                    results.append(f"{file}: {len(matching_lines)} occurrences")
                    if show_lines:
                        results.extend(matching_lines)

    return results


def write_results_to_file(filename: str, results: List[str]):
    """
    Write the results to a file, with overwrite confirmation if necessary.

    Args:
        filename (str): The name of the output file.
        results (List[str]): The results to write.
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
    """
    Main function to parse arguments and process files.
    """
    parser = argparse.ArgumentParser(description="Count HTML files with 'AI' while excluding specific terms.")
    parser.add_argument("directory", type=str, help="Directory containing HTML files.")
    parser.add_argument("-o", "--output", type=str, help="Output filename.")
    parser.add_argument("-s", "--show-lines", action="store_true", help="Show lines containing 'AI' (filtered).")
    
    args = parser.parse_args()

    # Get results
    results = count_html_files_with_ai(args.directory, args.show_lines)

    # Output results
    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
~~~
~~~
<div class="g-primary">
 <h1>
  SEM01P-Save Time and Resources: Using Disruptive Technologies in Higher Education (separate registration is required)
 </h1>
 <div class="events-session__header">
  <div class="events-session__header-info">
   Tuesday, October 25, 2016 | 12:30PM–4:00PM | Meeting Room 208A/B, Level Two
  </div>
  <div class="events-session__header-info">
   <strong>
    Session Type:
   </strong>
   <span>
    Additional Fee Program
   </span>
  </div>
  <div class="events-session__header-type">
   <strong>
    Delivery Format:
   </strong>
   <span>
    Preconference Seminar
   </span>
  </div>
 </div>
 <div class="rte-section">
  The creative economy. The sharing economy. Makerspaces. Digital distribution. The cloud. Open source. Numerous disruptive technologies are radically changing the world. However, these same technologies can help faculty and others rapidly bring ideas to life, benefiting students while saving time and judiciously using resources. Learn how we used a few low-cost pieces to build an entire secure digital textbook.
  <p>
   <br/>
   <b>
    Outcomes:
   </b>
   Construct a secure digital textbook using no/low-cost parts * Understand the qualities of the digital/creative/sharing economy * Design a solution using the best disruptive technologies
  </p>
 </div>
 <div class="events-session__grids">
  <h3>
   Presenters
  </h3>
  <ul class="nth-up corner-card__container">
   <li>
    <article class="corner-card">
     <div class="corner-card__body">
      <img onerror=" this.style.display = 'none' " src="https://ams.educause.edu/eweb/upload/60288979.jpg"/>
      <h4 class="corner-card__title">
       Wil Davis
      </h4>
      <div class="corner-card__description">
       <span>
       </span>
      </div>
     </div>
     <a class="corner-card__link" href="https://events.educause.edu/annual-conference/2016/presenter-directory?netForumRecordNumber=60288979">
     </a>
    </article>
   </li>
   <li>
    <article class="corner-card">
     <div class="corner-card__body">
      <img onerror=" this.style.display = 'none' " src="https://ams.educause.edu/eweb/upload/60185105.jpg"/>
      <h4 class="corner-card__title">
       Jonathan Huer
      </h4>
      <div class="corner-card__description">
       <span>
        Sr. Solution Architect AI,
       </span>
       <span>
        AT&amp;T
       </span>
      </div>
     </div>
     <a class="corner-card__link" href="https://events.educause.edu/annual-conference/2016/presenter-directory?netForumRecordNumber=60185105">
     </a>
    </article>
   </li>
  </ul>
 </div>
</div>
~~~

## Assistant (o1)

**Refining script options**

I'm enhancing the script to allow specific searches within HTML. I’ll implement features to target "h1" tags or "h1" with "rte-section" content, using tools like BeautifulSoup for parsing.

**Evaluating strategies**

I’m assessing scanning HTML content with BeautifulSoup. For "title-only," I’ll extract and check "h1" tags. For "title-and-content," I’ll combine "h1" and "rte-section" and scan the text.

**Enhancing script functionalities**

I’m adding command-line flags to differentiate between scanning "title" (h1 tag) and "title_and_content" (h1 with rte-section tag) for better flexibility in HTML processing.

**Refining options**

Implementing a scope argument helps pinpoint HTML sections for "AI" scanning, fine-tuning with BeautifulSoup to classify it as "title" or "title_and_content". This approach ensures precise targeting.

**Focusing the search**

Using BeautifulSoup, I’m parsing HTML to extract text from "h1" and "rte-section" tags. Next, I’ll scan these texts for "AI" or exclude specific words.

**Enhancing text extraction**

I’m refining the script to scan extracted texts for "AI," while preserving the functionality to show lines of interest. This ensures a comprehensive search that remains focused and relevant.

**Enhancing functionality**

I’m refining the script to include `show_lines` for extracting and displaying matching lines. This enhances the `count_html_files_with_ai` function, making it more effective and user-friendly.

## Assistant (o1)

Below is one way you can modify your script to add two new options:

1. **Scan only the presentation title** (the text in the `<h1>` tag).  
2. **Scan both the presentation title** (the `<h1>` tag) **and main content** (the `<div class="rte-section">` tag).

This version uses [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) to parse the HTML, extract the relevant sections, and then count occurrences of "AI" in each of those sections (while still excluding any lines that contain the words in `EXCLUDED_WORDS`).  

## Updated Script

```python
#!/usr/bin/env python3

import os
import argparse
from typing import List

# You will need to install BeautifulSoup with:
#   pip install beautifulsoup4
from bs4 import BeautifulSoup

# List of words containing 'AI' that do not mean 'artificial intelligence'
EXCLUDED_WORDS = [
    "SAILS", "WebAIM", "CampusEAI", "MAIS", "Kuali", "FAIT", "RAI", "SAIT", "FAE", 
    "NAIR", "AIMS", "HAIL", "AIR", "CFAIT", "FAIM", "SAIR", "PAIR", "AIM", "OAAI", 
    "AITS", "AIP", "SUSTAIN", "EGlIAIHi31", "FAILURE", "AIF"
]


def find_ai_in_html(filepath: str, scope: str, show_lines: bool = False) -> List[str]:
    """
    Parse an HTML file and find occurrences of "AI" in specific sections:
        - 'title': only scan <h1> tags
        - 'title_and_content': scan <h1> and <div class="rte-section"> tags

    Args:
        filepath (str): The path to the HTML file.
        scope (str): Which sections to scan ('title' or 'title_and_content').
        show_lines (bool): Whether to return the matching lines.

    Returns:
        List[str]: A list of matching lines containing 'AI', excluding EXCLUDED_WORDS.
    """
    results = []

    # Open and parse the HTML file with BeautifulSoup
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Gather text based on the chosen scope
    if scope == "title":
        # Only get the <h1> title(s)
        sections = soup.find_all("h1")
    else:  # scope == "title_and_content"
        # Get <h1> plus <div class="rte-section">
        title_tags = soup.find_all("h1")
        content_tags = soup.find_all("div", class_="rte-section")
        sections = title_tags + content_tags

    # Combine the text from each relevant tag
    relevant_texts = [tag.get_text(separator="\n") for tag in sections]

    # Now split the text into lines and find "AI" while excluding lines with EXCLUDED_WORDS
    for text_block in relevant_texts:
        lines = text_block.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if "AI" in line_stripped:
                # Check if any excluded word is in this line
                if not any(excluded in line_stripped for excluded in EXCLUDED_WORDS):
                    # If we are showing lines, store the line itself
                    if show_lines:
                        results.append(line_stripped)
                    else:
                        # If not showing lines, store just a placeholder
                        results.append("AI found")

    return results


def count_html_files_with_ai(directory: str, scope: str, show_lines: bool = False) -> List[str]:
    """
    Scan HTML files in a directory for lines containing "AI" (excluding EXCLUDED_WORDS),
    restricted by the specified scope.

    Args:
        directory (str): Path to the directory containing HTML files.
        scope (str): Which parts of the HTML to scan ('title' or 'title_and_content').
        show_lines (bool): Whether to display the lines containing "AI".

    Returns:
        List[str]: A summary of occurrences and optional matching lines.
    """
    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".html"):
                filepath = os.path.join(root, file)

                matching_lines = find_ai_in_html(filepath, scope, show_lines)

                if matching_lines:
                    # Count how many lines matched in this file
                    results.append(f"{file}: {len(matching_lines)} occurrences")
                    if show_lines:
                        results.extend(matching_lines)
    return results


def write_results_to_file(filename: str, results: List[str]):
    """
    Write the results to a file, with overwrite confirmation if necessary.

    Args:
        filename (str): The name of the output file.
        results (List[str]): The results to write.
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
    """
    Main function to parse arguments and process files.
    """
    parser = argparse.ArgumentParser(
        description="Count 'AI' occurrences in HTML, excluding specific terms."
    )
    parser.add_argument("directory", type=str, help="Directory containing HTML files.")
    parser.add_argument(
        "-o", "--output", type=str, help="Output filename."
    )
    parser.add_argument(
        "-s", "--show-lines", action="store_true", help="Show lines containing 'AI' (filtered)."
    )
    parser.add_argument(
        "--scope", 
        choices=["title", "title_and_content"], 
        default="title_and_content", 
        help=(
            "Which part of the HTML to scan for 'AI'. "
            "'title' scans only <h1>, "
            "'title_and_content' scans <h1> and <div class='rte-section'>."
        )
    )

    args = parser.parse_args()

    # Get results
    results = count_html_files_with_ai(args.directory, args.scope, args.show_lines)

    # Output results
    if args.output:
        write_results_to_file(args.output, results)
    else:
        print("\n".join(results))


if __name__ == "__main__":
    main()
```

### How It Works

1. **`--scope` Argument**  
   - `--scope title` will parse only the `<h1>` tags in each HTML file.  
   - `--scope title_and_content` (the default) will parse both the `<h1>` tags and any `<div class="rte-section">`.

2. **BeautifulSoup Parsing**  
   - We use BeautifulSoup to parse the HTML file so that we can accurately extract text from the relevant tags.
   - `soup.find_all("h1")` gets all `<h1>` elements.
   - `soup.find_all("div", class_="rte-section")` gets all `<div>` elements whose `class` contains `rte-section`.

3. **Filtering Out Unwanted Lines**  
   - After splitting each extracted text by lines, the script checks whether `AI` is in the line.
   - It also checks that none of the terms in `EXCLUDED_WORDS` are present in the same line.
   - If it passes both checks, that line is counted as an occurrence.

4. **Showing Lines**  
   - If you use the option `-s` or `--show-lines`, the script will include each matching line in the output instead of just showing the count.

5. **Writing Results to a File**  
   - If you include the `-o FILENAME` parameter, the script will prompt before overwriting an existing file and then save the results there.

---

With these changes, you can now easily limit your search to just the title or to both the title and main content.

## User

Please modify the script to find "artificial intelligence" together with "AI" as a default, and add options to find each of (i) "AI" (current) and (ii) "artificial intelligence".

## Assistant (o1)



## Assistant (o1)

**Refining the search**

I’m adjusting the code to handle queries for both "AI" and "artificial intelligence" by adding a `--search` argument with options for `AI`, `artificial_intelligence`, or `both`, while ensuring exclusion criteria are met.

## Assistant (o1)

Below is an updated version of the script that allows you to:

- By default, search for both "AI" and "artificial intelligence".
- Use the `--search` option to specify searching only for:
  - "AI"
  - "artificial intelligence"
  - both "AI" and "artificial intelligence" (the default).

When searching for "AI," the script still excludes lines containing any words from the `EXCLUDED_WORDS` list. When searching for "artificial intelligence," no exclusions are applied. If "both" is selected, it applies the exclusions only to lines containing "AI."

**Note:** This code builds on the previously modified script that uses BeautifulSoup and includes the `--scope` option for choosing which parts of the HTML to scan. Make sure you have `beautifulsoup4` installed.

```python
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


def line_contains_search_terms(
    line: str, search_mode: str
) -> bool:
    """
    Check if a given line contains the desired search terms based on the search_mode.

    search_mode can be:
      - "AI": only find lines containing "AI" (excluding EXCLUDED_WORDS).
      - "artificial_intelligence": only find lines containing "artificial intelligence".
      - "both": find lines containing either "AI" (with exclusion) or "artificial intelligence".
    """
    line_lower = line.lower()

    # Conditions for each search mode
    if search_mode == "AI":
        # Must contain "AI" and pass exclusions
        if "ai" in line:
            # Check exclusions
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence"
        return "artificial intelligence" in line_lower

    else:  # search_mode == "both"
        # Line matches if it contains "artificial intelligence"
        # or if it contains "AI" and is not excluded.
        contains_ai = "ai" in line
        contains_artificial_intel = "artificial intelligence" in line_lower

        if contains_artificial_intel:
            return True
        if contains_ai:
            # Check exclusions for AI specifically
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False


def find_matches_in_html(filepath: str, scope: str, search_mode: str, show_lines: bool = False) -> List[str]:
    """
    Parse an HTML file and find occurrences of terms based on search_mode.
    Scope can be 'title' or 'title_and_content':
      - title: only <h1> tags
      - title_and_content: <h1> and <div class='rte-section'>

    search_mode can be:
      - "AI"
      - "artificial_intelligence"
      - "both" (default)

    Returns:
        List[str]: matched lines if show_lines=True, else a placeholder for counting occurrences.
    """
    results = []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")

    if scope == "title":
        sections = soup.find_all("h1")
    else:  # title_and_content
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


def count_html_files(directory: str, scope: str, search_mode: str, show_lines: bool = False) -> List[str]:
    """
    Scan HTML files in a directory for lines containing the desired terms.

    Args:
        directory (str): Directory with HTML files.
        scope (str): Which part of HTML to scan: 'title' or 'title_and_content'.
        search_mode (str): Which term(s) to search: 'AI', 'artificial_intelligence', 'both'.
        show_lines (bool): Whether to display the lines.

    Returns:
        List[str]: Summaries of occurrences and optional matching lines.
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
        description="Count occurrences of 'AI' and/or 'artificial intelligence' in HTML."
    )
    parser.add_argument("directory", type=str, help="Directory containing HTML files.")
    parser.add_argument("-o", "--output", type=str, help="Output filename.")
    parser.add_argument("-s", "--show-lines", action="store_true", help="Show lines containing the matched terms.")

    parser.add_argument(
        "--scope",
        choices=["title", "title_and_content"],
        default="title_and_content",
        help=(
            "Which part of the HTML to scan. "
            "'title' scans only <h1>, "
            "'title_and_content' scans <h1> and <div class='rte-section'>."
        )
    )

    parser.add_argument(
        "--search",
        choices=["AI", "artificial_intelligence", "both"],
        default="both",
        help=(
            "What to search for: 'AI', 'artificial_intelligence', or 'both'. "
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
```

### Summary of Changes

- Added a new `--search` argument with choices: `AI`, `artificial_intelligence`, and `both`.
- Default search mode is now `both`, meaning it will search for lines containing either "AI" (excluding `EXCLUDED_WORDS`) or "artificial intelligence" (no exclusions).
- If `--search AI` is used, only lines containing "AI" are found (with exclusions).
- If `--search artificial_intelligence` is used, only lines containing the phrase "artificial intelligence" are found (no exclusions).
- If `--search both` (or omitted), the script finds lines containing either "AI" (with exclusions) or "artificial intelligence" (no exclusions).
- The logic for checking line matches is centralized in `line_contains_search_terms` function.

This should fulfill the requested enhancements.

## User

For the word "AI", please only accept upper cases (reject ai, Ai, and aI).

## Assistant (o1)



## Assistant (o1)

Below is an updated version of the script. The main change is in how we check for "AI". Previously, we converted the line to lowercase to check for presence. Now, we specifically look for uppercase "AI" without altering the line's case. Lines that contain "AI" in uppercase will be counted, while variations like "Ai", "aI", or "ai" will not be counted.

**Key Changes:**
- When `--search` is set to `AI` or `both`, we now check for the exact string "AI" (uppercase) in the original line.
- We still do lowercase checks for exclusions, but only after confirming the exact uppercase "AI" is present.

```python
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

    search_mode can be:
      - "AI": only find lines containing uppercase "AI"
      - "artificial_intelligence": only find lines containing "artificial intelligence"
      - "both": find lines containing either "AI" (uppercase only, excluding EXCLUDED_WORDS) 
                or "artificial intelligence"
    """
    # Keep original case for "AI" check
    line_lower = line.lower()

    if search_mode == "AI":
        # Must contain uppercase "AI"
        if "AI" in line:  
            # Check exclusions (case-insensitive)
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
        return False

    elif search_mode == "artificial_intelligence":
        # Must contain "artificial intelligence" (case-insensitive)
        return "artificial intelligence" in line_lower

    else:  # search_mode == "both"
        # Check for "artificial intelligence"
        contains_artificial_intel = "artificial intelligence" in line_lower
        
        # Check for uppercase "AI"
        contains_AI = "AI" in line  # exact uppercase check

        if contains_artificial_intel:
            return True
        if contains_AI:
            # Check exclusions for AI lines
            return not any(excluded.lower() in line_lower for excluded in EXCLUDED_WORDS)
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
    else:  # title_and_content
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
        description="Count occurrences of 'AI' (uppercase only) and/or 'artificial intelligence' in HTML."
    )
    parser.add_argument("directory", type=str, help="Directory containing HTML files.")
    parser.add_argument("-o", "--output", type=str, help="Output filename.")
    parser.add_argument("-s", "--show-lines", action="store_true", help="Show lines containing the matched terms.")

    parser.add_argument(
        "--scope",
        choices=["title", "title_and_content"],
        default="title_and_content",
        help=(
            "Which part of the HTML to scan. "
            "'title' scans only <h1>, "
            "'title_and_content' scans <h1> and <div class='rte-section'>."
        )
    )

    parser.add_argument(
        "--search",
        choices=["AI", "artificial_intelligence", "both"],
        default="both",
        help=(
            "What to search for: 'AI' (uppercase only), 'artificial_intelligence', or 'both'. "
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
```

### Explanation
- We now strictly look for uppercase `"AI"` by checking `if "AI" in line:`. Since Python string matching is case-sensitive, this will only match the exact uppercase "AI".
- Variations like `"Ai"`, `"aI"`, or `"ai"` will not be matched.
- When searching for `"artificial intelligence"`, we still do a lowercase check to be case-insensitive.
- When searching for `"both"`, a line is considered a match if it either contains `"artificial intelligence"` (case-insensitive) or the exact uppercase `"AI"` (with exclusions).

## User

Please add options to find (i) "generative artificial intelligence" (case insensitive), (ii) "generative AI" (case insensitive for "generative" and case sensitive for "AI"), and (iii) "Gen AI" (case insensitive for "Gen" and case sensitive for "AI").

## Assistant (o1)



## Assistant (o1)

**Enhancing search options**

I’m thinking about refining the search script by integrating "generative_artificial_intelligence", "generative_AI", and "gen_AI". This involves tweaking `--search` options to boost search modes, possibly adjusting the script's name and default choices.

**Mapping out search logic**

I’m working on logic to locate "generative artificial intelligence", "generative AI", and "Gen AI" in text. This involves identifying "generative" and "AI" together, considering case sensitivity and order, and ensuring they appear consecutively.

**Enhancing search methods**

I’m refining ways to identify "generative ai" by checking for "generative" in lowercase and "AI" in the original line, ensuring they appear consecutively and with correct case sensitivity.

**Refining the search**

I’m refining the search logic to ensure "generative AI" is identified by using regular expressions for case-insensitivity and exact uppercase matching for "AI" in the original line.

**Crafting a precise regex**

I’m developing a regex to track "generative AI" by employing case-insensitive matching for "generative" and exact uppercase matching for "AI" in the original line.

**Confirming uppercase accuracy**

I’m refining the search logic to ensure "generative ai", "generative AI", and "gen ai" are identified with precise case sensitivity checks, confirming "AI" as uppercase in the original line.

**Synthesizing search methods**

I’m planning to define new search modes like `generative_artificial_intelligence`, `generative_AI`, and `gen_AI`, while retaining old methods. This way, all options will be available for diverse user needs.

**Strategizing search modes**

I’m considering incorporating separate search modes for "generative artificial intelligence", "generative AI", and "Gen AI". This approach respects the user's need for diverse search options, following case sensitivity and previous guidelines for "AI".

**Assessing inclusion criteria**

OK, let me see: I'm mapping out if "generative artificial intelligence", "generative AI", or "gen AI" should be subject to EXCLUDED_WORDS. Ultimately, excluding uppercase "AI" lines seems prudent.

**Mapping the assessment**

Piecing together an approach to confirm new phrases exclude uppercase "AI" in lines, ensuring originality and consistent alignment with guidelines. Progress is steady and methodical.

**Crafting search strategies**

I’m crafting search strategies for "generative AI" and "Gen AI", ensuring these phrases exclude uppercase "AI" in lines and checking for any exclusion terms.

## Assistant (o1)

Below is an updated version of the script that adds **three** new search options:

1. `generative_artificial_intelligence` (case-insensitive)  
2. `generative_AI` (case-insensitive for “generative” but **must** match `AI` in uppercase)  
3. `gen_AI` (case-insensitive for “gen” but **must** match `AI` in uppercase)

> **Note**  
> - We keep the old modes (`AI`, `artificial_intelligence`, `both`) so the script remains backward-compatible.  
> - If a phrase includes uppercase `AI`, we apply the same exclusion check (via `EXCLUDED_WORDS`) that we do for the `AI` search mode.  
> - When searching for phrases without `AI` (e.g., “generative artificial intelligence”), **no** exclusions apply, because there is no literal `AI` substring to exclude.

Make sure you have **BeautifulSoup** installed (`pip install beautifulsoup4`). Save the script as, for example, `AI_word_counter.py`:

```python
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
```

### Usage Examples

1. **Search only in `<h1>` tags** for **“generative AI”** lines:
   ```bash
   python3 AI_word_counter.py /path/to/html/files --scope title --search generative_AI
   ```

2. **Search in titles and content** for **“Gen AI”** lines, and display the actual lines:
   ```bash
   python3 AI_word_counter.py /path/to/html/files --search gen_AI --show-lines
   ```

3. **Search for “generative artificial intelligence”** (case-insensitive) in default scope (`title_and_content`), writing results to a file:
   ```bash
   python3 AI_word_counter.py /path/to/html/files --search generative_artificial_intelligence -o output.txt
   ```

4. **Search for uppercase “AI”** (excluding lines with `EXCLUDED_WORDS`) or case-insensitive “artificial intelligence” (the default `--search both`):
   ```bash
   python3 AI_word_counter.py /path/to/html/files
   ```

This version should meet your requirement to detect those three new phrases while still preserving the original functionality for detecting uppercase `"AI"` or `"artificial intelligence"` lines.

