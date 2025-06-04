# SIE

This repository provides utilities to download and process 3GPP TDoc files.

## Batch download

Use `batch_download.py` to fetch TDocs for a specific working group and meeting.

```bash
python batch_download.py tsg_ran/WG1_RAN1 TSGR1_92e -o downloads
```

The script parses the given FTP directory and downloads all `.zip` TDocs to the
specified directory.

## Processing TDocs

After downloading, `process_tdocs.py` can unzip all archives and convert any
Office documents to PDF (requires `libreoffice`).

```bash
python process_tdocs.py -i downloads -u unzipped -p pdf
```

Converted PDFs will keep the original TDoc file name with a `.pdf` extension.

