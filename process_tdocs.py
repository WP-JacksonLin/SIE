import argparse
import os
import subprocess
import zipfile
from pathlib import Path


def unzip_files(input_dir, extract_dir):
    input_path = Path(input_dir)
    extract_path = Path(extract_dir)
    extract_path.mkdir(parents=True, exist_ok=True)
    for zip_file in input_path.glob('*.zip'):
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(extract_path)


def convert_to_pdf(src_dir, pdf_dir):
    src_path = Path(src_dir)
    pdf_path = Path(pdf_dir)
    pdf_path.mkdir(parents=True, exist_ok=True)

    for doc in src_path.rglob('*'):
        if doc.suffix.lower() in {'.doc', '.docx', '.ppt', '.pptx'}:
            out_file = pdf_path / (doc.stem + '.pdf')
            cmd = [
                'libreoffice', '--headless', '--convert-to', 'pdf',
                str(doc), '--outdir', str(pdf_path)
            ]
            try:
                subprocess.run(cmd, check=True)
            except FileNotFoundError:
                raise RuntimeError('libreoffice is required for document conversion')
            # rename output to match TDoc name if needed
            converted = pdf_path / (doc.stem + '.pdf')
            if converted.exists():
                converted.rename(out_file)


def main():
    parser = argparse.ArgumentParser(description='Unzip and convert TDoc files to PDF')
    parser.add_argument('-i', '--input', default='downloads', help='Directory of downloaded zip files')
    parser.add_argument('-u', '--unzipped', default='unzipped', help='Directory for unzipped files')
    parser.add_argument('-p', '--pdf', default='pdf', help='Directory for output PDFs')
    args = parser.parse_args()

    unzip_files(args.input, args.unzipped)
    convert_to_pdf(args.unzipped, args.pdf)


if __name__ == '__main__':
    main()
