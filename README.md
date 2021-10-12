# ps5-buying-bot

Automated buying bot for a PS5. This code can be used to check for a PS5 in stock at Big W and then buy it.

To create this Python script I started by reading the articles listed below:
* https://www.linkedin.com/pulse/building-scalper-bot-alex-g   
* https://spltech.co.uk/how-to-make-a-python-bot/  

This script uses Google Chrome and assumes you are already logged in to the Big W website and have saved credit card details. The script will run every X minutes until it has successfully bought a PS5, then it will stop.

## Installation

To install the script first ensure Python 3.9+ and Google Chrome is installed on your machine (this was built in Python 3.9.7). 

To install a virtual environment and dependencies run `bash ./scripts/install.sh` on Mac/Linux or double click `./scripts/install.cmd` on Windows.

To activate the virtual environment run `bash ./scripts/activate.sh` on Mac/Linux or double click `./scripts/activate.cmd` on Windows.

## Set up

### Environment variables

Duplicate the `.sample-env` file and rename it `.env`. Fill out the variables as described below.
* CVV - The CVV of your saved credit card
* PROFILE_NAME - Folder name of Chrome profile to use (see next section) 
* WAIT_TIME_MINS - Number of minutes to wait between each stock check

### Chrome profile

To create and configure a custom Chrome profile to use with this script:
1. Open Chrome
2. Click user icon and "Add" other profile.
3. Fill in details.
4. Go to the Big W website, make sure you set a local store, log in to your account and the details are kept in cookies. You must have a saved payment method for this to work.
5. Go to [chrome://version/](chrome://version/).
6. Note the profile path and navigate to that folder.
7. Copy the folder.
8. Create a new folder inside this repo called `Chrome`.
9. Paste the profile folder inside the `Chrome` folder. 
10. The folder name is the profile name, e.g., `Profile 1`.

### Test set up

To test the Selenium set up run `bash ./scripts/test_set_up.sh` on Mac/Linux or double click `./scripts/test_set_up.cmd` on Windows.

To test the repeating job run `bash ./scripts/test.sh` on Mac/Linux or double click `./scripts/test.cmd` on Windows.

## Run

To run the script run `bash ./scripts/run.sh` on Mac/Linux or double click `./scripts/run.cmd` on Windows.

## Potential issues

* The Chrome driver binary version make not be compatible with your version of Chrome. You can check available versions at https://pypi.org/project/chromedriver-binary/#history, make sure it aligns (or is as close to) the version mentioned at [chrome://version/](chrome://version/).