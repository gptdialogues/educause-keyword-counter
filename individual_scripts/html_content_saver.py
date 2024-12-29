#!/usr/bin/env python3.12

import argparse
import os
import time
import requests
from bs4 import BeautifulSoup
from typing import List

def sanitize_url(url: str) -> str:
    """
    Removes any unwanted characters (e.g., carriage return) from the URL.

    Args:
        url (str): The URL to sanitize.

    Returns:
        str: The sanitized URL.
    """
    return url.strip().replace('%0D', '')

def download_html(url: str) -> str:
    """
    Downloads the HTML content from the specified URL.

    Args:
        url (str): The URL to download the content from.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(html: str) -> str:
    """
    Extracts the specified portion of the HTML content.

    Args:
        html (str): The HTML content to parse.

    Returns:
        str: The extracted portion of the HTML content.
    """
    soup = BeautifulSoup(html, 'html.parser')
    target_div = soup.find('div', class_='g-primary')
    return target_div.prettify() if target_div else ""

def save_to_file(content: str, filename: str) -> None:
    """
    Saves the specified content to a file.

    Args:
        content (str): The content to save.
        filename (str): The file to save the content to.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

def confirm_overwrite(filename: str) -> bool:
    """
    Asks the user for confirmation before overwriting a file.

    Args:
        filename (str): The file to potentially overwrite.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    if os.path.exists(filename):
        response = input(f"File '{filename}' already exists. Overwrite? (y/n): ").lower()
        return response == 'y'
    return True

def process_urls(urls: List[str], output: str, interval: int) -> None:
    """
    Processes multiple URLs, extracting and saving HTML content.

    Args:
        urls (List[str]): List of URLs to process.
        output (str): Output filename pattern or None for stdout.
        interval (int): Interval between requests in seconds.
    """
    for idx, url in enumerate(urls):
        sanitized_url = sanitize_url(url)
        print(f"Processing URL: {sanitized_url}")

        try:
            html_content = download_html(sanitized_url)
            extracted_content = parse_html(html_content)

            if output:
                filename = output if len(urls) == 1 else f"{os.path.splitext(output)[0]}_{idx+1}.html"
                if confirm_overwrite(filename):
                    save_to_file(extracted_content, filename)
                    print(f"Content saved to '{filename}'")
                else:
                    print(f"Skipping '{filename}'")
            else:
                print(extracted_content)

        except requests.exceptions.RequestException as e:
            print(f"Error processing URL '{sanitized_url}': {e}")

        if idx < len(urls) - 1:
            time.sleep(interval)

def main() -> None:
    """
    Main function to parse arguments and process URLs.
    """
    parser = argparse.ArgumentParser(description="Download and extract specific HTML content from a URL.")
    parser.add_argument('-u', '--url', type=str, help="URL to download the HTML from.")
    parser.add_argument('-f', '--file', type=str, help="File containing URLs (one per line).")
    parser.add_argument('-o', '--output', type=str, help="Output filename. If not specified, prints to stdout.")
    parser.add_argument('-i', '--interval', type=int, default=5, help="Interval between multiple downloads in seconds (default: 5).")
    args = parser.parse_args()

    urls = []
    if args.url:
        urls.append(args.url)
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as file:
                urls.extend([line.strip() for line in file if line.strip()])
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found.")
            return

    if not urls:
        print("Error: No URL(s) provided. Use -u or -f to specify URLs.")
        return

    process_urls(urls, args.output, args.interval)

if __name__ == "__main__":
    main()
