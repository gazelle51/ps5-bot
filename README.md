# ps5-scalper

Scalping bot for a PS5.

I was hanging out on Discord one night with my friends. For the past few months I had been working on a Discord bot for them and they loved it. I had just been told I had to quarantine for 14 days and they said "you should make me a PS5 bot!". So I obliged.

I started by reading a few articles on the net and then dived right in to it.  
https://www.linkedin.com/pulse/building-scalper-bot-alex-g   
https://spltech.co.uk/how-to-make-a-python-bot/  

I decided to build in Python and here we are.

## Installation

To install the bot first ensure Python 3.9+ is installed on your machine. Then run

```bash
bash ./scripts/install.sh
```


## Chrome profile

1. Open Chrome
2. Click user icon and "Add" other profile.
3. Fill in details
4. Go to Big W, make sure you set a local store, log in to your account and the details are kept in cookies. You must have a saved payment method for this to work.
5. In browser go to chrome://version/
6. Note the profile path and navigate to that folder.
7. Copy the folder.
8. Create a new folder inside this repo called 'Chrome'.
9. Paste the profile folder inside the 'Chrome' folder. 
10. The folder name is the profile name
  e.g., Profile 2