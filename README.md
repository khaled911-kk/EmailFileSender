# Email File Sender

This Python project scans directories for image files, compresses them into ZIP archives, and sends them via email.

## Features:
- Searches for image files in a specified directory.
- Compresses files into ZIP archives if they exceed a size limit.
- Sends ZIP files to an email recipient using Gmail.

## How to Use:
1. Clone the repository:
   ```
   git clone https://github.com/khaled911-kk/EmailFileSender.git
   ```
2. Install the required dependencies manually:
   ```
   pip install os smtplib zipfile tqdm
   ```
3. Run the script:
   ```
   python main.py
   ```

## Requirements:
- Python 3.x
- Libraries: os, smtplib, zipfile, tqdm

## License:
This project is open-source and available under the MIT License.

