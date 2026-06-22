👓 **Parse and extract the most important diagnostic commands from an RSI**

This script takes an RSI file, parses it, and extracts all relevant commands into a single file.

It works as follows:

```
python[3] <source-path-for-the-script> <source-path-for-the-rsi-file> <resulting-file-name>
```

For example (doing this on my Windows machine):

```
python3 "C:\Users\user\Documents\Coding\Python\script-to-extract-config-from-rsi\extract-commands-script.py" "C:\Users\user\Documents\Coding\Python\script-to-extract-config-from-rsi\test-rsi.txt" "commands-file"
```

The resulting file will always be created in the Downloads directory regardless of the OS being used.

I think I'll create different versions of this script for the following platforms (if the platform has a ✅ it means there's already a script for it):

- EX
- QFX
- ACX
- PTX
- MX
- SRX (✅)