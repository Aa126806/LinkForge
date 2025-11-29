import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import deque


def get_refs(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')
        return [a.get('href') for a in soup.find_all('a', href=True)]
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []


def load_skip_extensions():
    try:
        with open('config.txt', 'r', encoding='utf-8') as file:
            extensions = []
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    extensions.append(line)
            return extensions
    except FileNotFoundError:
        return [
            '.pdf', '.doc', '.docx', '.zip', '.rar', '.7z', '.tar', '.gz',
            '.exe', '.msi', '.dmg', '.pkg', '.jpg', '.jpeg', '.png', '.gif',
            '.mp4', '.avi', '.mov', '.mp3', '.wav', '.txt', '.csv', '.xls',
            '.xlsx', '.ppt', '.pptx'
        ]


def should_skip_url(url, skip_extensions):
    clean_url = url.split('?')[0].split('#')[0]

    for ext in skip_extensions:
        if ext in clean_url.lower():
            return True
    return False


if __name__ == "__main__":
    url = input("Enter URL: ")

    try:
        max_links = int(input("Enter maximum number of links to collect (0 for unlimited): "))
    except ValueError:
        print("Invalid input. Using unlimited links.")
        max_links = 0

    visited = set()
    to_process = deque([url])
    result = []
    skip_extensions = load_skip_extensions()

    while to_process:
        if max_links > 0 and len(result) >= max_links:
            print(f"Reached maximum limit of {max_links} links. Stopping...")
            break

        current_url = to_process.popleft()

        if current_url in visited:
            continue

        print(f"Processing: {current_url}")

        visited.add(current_url)
        result.append(current_url)

        new_refs = get_refs(current_url)

        for ref in new_refs:
            if "http" not in ref:
                full_url = urljoin(url, ref)
            else:
                full_url = ref

            if should_skip_url(full_url, skip_extensions):
                continue

            if url in full_url and full_url not in visited and full_url not in to_process:
                to_process.append(full_url)

    with open("links.txt", "w", encoding="utf-8") as file:
        for link in result:
            file.write(link + "\n")

    print(f"\nFound {len(result)} links. Result saved to links.txt")