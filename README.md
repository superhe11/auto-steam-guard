# Auto-Steam-Guard
Python script that uses IMAP to access your mail and get Steam Guard code

## How-to guide

Download python, install pip, install the dependencies
```
pip install -r requirements.txt
```

**Configurate your credentials.txt**

• Go [here](https://support.google.com/accounts/answer/185833?hl=en&sjid=6853307571511828064-NA) and set up an app password.

• You will get it in a form like this - [*abcd efgh ijkl mnop*] - delete all spaces and paste it into .txt file. 

It should look like this - [*email:password*]

Now just start the script! It will automatically detect mails from Steam Support and copy your code to clipboard.

## Important notes

Code may not work in other languages, i cannot test all of them, if script parces something wrong, just open issue, i will fix it.
