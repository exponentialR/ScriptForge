# Utility Scripts Repository

## Overview
This repository is a collection of utility scripts that I use frequently for various tasks. Each script serves a specific purpose, designed to streamline and automate processes that are otherwise repetitive or cumbersome. 

---

## Scripts in This Repository

### 1. gdrive_upload.py

#### Description
`gdrive_upload.py` is a Python script for uploading files to Google Drive. It integrates with the Google Drive API, allowing for automated uploads directly from the command line. The script includes features like OAuth2 authentication and a progress bar to visually track the upload process.
Could be useful as part of an ML workflow. 

#### Setting Up

##### Prerequisites
- Python 3.x
- Google account with access to Google Drive
- `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`, and `tqdm` libraries installed in Python

##### Installation
1. Clone the repository to your local machine.
2. Install the required Python libraries using pip:

    `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib tqdm`

##### Google Drive API and Credentials
Before using the script, you need to set up Google Drive API access and obtain credentials:

1. **Google Cloud Console Setup**:
- Go to [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project.
- Enable the Google Drive API for your project.

2. **Creating OAuth 2.0 Client ID**:
- In the API & Services dashboard, navigate to “Credentials”.
- Click “Create credentials” and choose “OAuth client ID”.
- Set the application type to “Desktop app” and provide a name.
- Download the JSON file containing your credentials.

3. **Prepare the Credentials**:
- Rename the downloaded JSON file to `credentials.json`.
- Place `credentials.json` in the same directory as the `gdrive_upload.py` script.

#### Usage
To use the script for uploading a file to Google Drive:

1. Navigate to the directory containing `gdrive_upload.py`.
2. Run the script with the path to the file you want to upload:

`python gdrive_upload.py -ie myemail@myemail.com -passwd mypassword -rec receiveremail@email.com -fp path/to/your/file`

3. Ensure you change `myemail@email.com`, `mypassword` accordingly, and replace `receiveremail@email.com` with the recipient email address.

3. Follow the on-screen instructions to authenticate and complete the upload.

The first time you run the script, it will prompt you to log into your Google account and grant the necessary permissions. This process will create a `token.pickle` file in the same directory, storing your authentication tokens for future use.

---

## Contributing
Contributions to this repository are welcome. Please feel free to fork the repository, make changes, and submit pull requests. For major changes or new scripts, please open an issue first to discuss what you would like to change.

---

## License
[MIT](https://choosealicense.com/licenses/mit/)

---

This README provides a general guide to the utility scripts in this repository. It is advisable to regularly update it as new scripts are added or existing ones are modified.
