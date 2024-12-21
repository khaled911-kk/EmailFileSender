Email File Sender
This project allows you to scan a directory for image files, compress them into zip files, and send them via email.

    ## Requirements

    - Python 3.x

    - Libraries:

      - `smtplib`

      - `os`

      - `zipfile`

      - `time`

      - `tqdm` (for progress bar)


    ## How to Use

    1. Place the Python script in the desired folder.

    2. Edit the script to specify the root directory, sender email, sender password, and recipient email.

    3. Run the script:

       ```bash

       python main.py

       ```


    The script will search for image files, compress them, and send them as zip files via email.


    ## Important Notes

    - Ensure that the email and password are correctly configured for the sender.

    - This script is designed to handle a large number of image files and send them in parts.
