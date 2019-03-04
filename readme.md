# EC2 Instance Killer

This just stops all EC2 instances whose instance id is not in the whitelist.json file

This is how the whitelist.json file is formated.
```json
["i-1234567890abcdef0","i-0598c7d356eba48d7"]
```

As is this requires user intevention in order to work.
The program stopnonwhitelistedinstances.py requires the user to confirm they wish to stop the intances with a capital Y.