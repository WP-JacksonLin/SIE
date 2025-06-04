import argparse
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def fetch_tdoc_links(base_url):
    """Return list of full URLs to TDoc zip files under base_url."""
    res = requests.get(base_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    links = []
    for a in soup.find_all('a'):
        href = a.get('href')
        if href and href.lower().endswith('.zip'):
            links.append(urljoin(base_url, href))
    return links


def download_file(url, out_dir):
    local_filename = os.path.join(out_dir, os.path.basename(url))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return local_filename


def main():
    parser = argparse.ArgumentParser(description="Download 3GPP TDocs in batch")
    parser.add_argument('working_group', help='3GPP working group path (e.g. tsg_ran/WG1_RAN1)')
    parser.add_argument('meeting', help='Meeting folder name (e.g. TSGR1_92e)')
    parser.add_argument('-o', '--output', default='downloads', help='Output directory')
    parser.add_argument('--root', default='https://ftp.3gpp.org', help='3GPP FTP root URL')
    args = parser.parse_args()

    base_url = f"{args.root}/{args.working_group}/{args.meeting}/Docs/"
    os.makedirs(args.output, exist_ok=True)

    links = fetch_tdoc_links(base_url)
    if not links:
        print('No TDocs found at', base_url)
        return

    print(f"Downloading {len(links)} files to {args.output}...")
    for url in tqdm(links):
        try:
            download_file(url, args.output)
        except Exception as e:
            print('Failed to download', url, e)


if __name__ == '__main__':
    main()
