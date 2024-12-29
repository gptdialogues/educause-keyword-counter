---
title: HTML Content Extraction Script
create_time: 2024-10-14 12:24:46
update_time: 2024-10-14 12:27:18
conversation_id: 670c8efe-6908-800f-b82c-74dfd228153d
---

# HTML Content Extraction Script

Creation Time: 2024-10-14 12:24:46

Update Time: 2024-10-14 12:27:18

## Assistant



## User

I got `file.html` from the following command:
wget "https://events.educause.edu/annual-conference/2024/agenda/educause-executive-leaders-academy-by-invitation-only" -O file.html
I attached `file.html`. I would like to save the part of the HTML file shown below.

~~~ part_of_file.html
<section class="g-content-container">
<div class="breadcrumbs">
<ul>
<li class="breadcrumbs__crumb breadcrumbs__crumb--home">
<a href="https://events.educause.edu/annual-conference">EDUCAUSE Annual Conference 2024</a>
<svg role="img" aria-label="Right Arrow" class="icon icon-arrow-right">
<title>Right Arrow</title>
<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/assets/images/svg-defs.svg#icon-arrow-right"></use>
</svg>
</li>
<li class="breadcrumbs__crumb">
<a href="https://events.educause.edu/annual-conference/agenda">Agenda</a>
<svg role="img" aria-label="Right Arrow" class="icon icon-arrow-right">
<title>Right Arrow</title>
<use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="/assets/images/svg-defs.svg#icon-arrow-right"></use>
</svg>
</li>
<li class="breadcrumbs__crumb">EDUCAUSE Executive Leaders Academy (by invitation only)</li>
</ul>
</div>
<section class="g-content-container">
<div class="g-primary">
<h1>EDUCAUSE Executive Leaders Academy (by invitation only)</h1>
<div class="events-session__header">
<div class="events-session__header-info">
Sunday, October 20, 2024 | 1:00PM–5:00PM CT | Grand Hyatt San Antonio, Lone Star AB, Second Floor
</div>
<div class="events-session__header-info">
<strong>Session Type:</strong>
<span>
Meeting
</span>
</div>
</div>
<div class="rte-section">
<p>The newly designed EDUCAUSE Executive Leaders Academy is a hybrid, cohort-based, immersive, and applied learning experience for higher education executive leaders or those actively seeking executive positions. This seven-month program begins with an in-person component at the EDUCAUSE Annual Conference (included in registration fee) and continues online, featuring experts and thought leaders in key areas throughout.</p>
<p>NOTE: For EDUCAUSE Executive Leaders Academy accepted registrants only</p>
</div>
<div class="events-session__grids">
</div>
</div>
<div class="g-secondary" id="sidebar">
</div>
</section>
</section>
~~~

Please generate a python3 script to save the specified part of the HTML. I would like to add some additional specifications below.
- Add a help option using `argparse`.
- Add docstrings and type hints.
- Add an option to specify a URL.
- Add an option to specify a TXT file with URLs in each line as an argument of the script.
- Add an option to specify the output filename.
- Output the text to stdout if there is no specified output filename.
- Suggest some potential filenames for the script.
- Ask "(y)es/(n)o" before overwriting an existing file (default: no). 
- Add the following shebang.
```
#!/usr/bin/env python3
```

## Assistant (gpt-4o)


Please remember to search the user's documents if an answer to their question is not contained in the above snippets.


## Assistant (gpt-4o)

Here is a Python script that will extract the specified part of an HTML file, including options for help, specifying URLs, handling text files with multiple URLs, and outputting the result. It also includes confirmation for overwriting an existing file. The script uses the `argparse` library to handle command-line arguments and options.

```python
#!/usr/bin/env python3

import os
import sys
import argparse
from urllib.request import urlopen
from bs4 import BeautifulSoup

def extract_html_content(html: str) -> str:
    """Extract the content within the <section> tags that match the specified class."""
    soup = BeautifulSoup(html, 'html.parser')
    section = soup.find('section', class_='g-content-container')
    return section.prettify() if section else ''

def save_content(content: str, output_file: str):
    """Save content to a file, prompt user if overwriting."""
    if os.path.exists(output_file):
        overwrite = input(f"File {output_file} exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("Aborted.")
            return
    with open(output_file, 'w') as file:
        file.write(content)
    print(f"Content saved to {output_file}")

def process_url(url: str, output_file: str = None):
    """Fetch and process the HTML content from the URL."""
    response = urlopen(url)
    html = response.read().decode('utf-8')
    content = extract_html_content(html)
    if output_file:
        save_content(content, output_file)
    else:
        print(content)

def process_file(file_path: str, output_file: str = None):
    """Process each URL in the file."""
    with open(file_path, 'r') as f:
        for url in f:
            process_url(url.strip(), output_file)

def main():
    parser = argparse.ArgumentParser(description="Extract and save a specific part of an HTML file.")
    parser.add_argument('-u', '--url', type=str, help="URL of the HTML page to fetch")
    parser.add_argument('-f', '--file', type=str, help="File containing URLs (one per line)")
    parser.add_argument('-o', '--output', type=str, help="Output file to save the content")
    
    args = parser.parse_args()

    if args.url:
        process_url(args.url, args.output)
    elif args.file:
        process_file(args.file, args.output)
    else:
        print("Error: Either a URL or a file must be provided.")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### Suggested filenames for the script:
- `extract_html.py`
- `html_extractor.py`
- `html_content_saver.py`

### How the script works:
- The `extract_html_content` function extracts the desired `<section>` tag using BeautifulSoup.
- The script supports two primary input methods: 
  - A single URL (`--url` option).
  - A text file containing URLs, one per line (`--file` option).
- If an output filename (`--output`) is not provided, the script will print the extracted content to stdout.
- If an output file is provided and already exists, the user will be prompted to confirm overwriting it.

You can adjust the filename and try running the script as needed!

