⛏️ **Extract a hierarchical configuration from an RSI**

This script takes an RSI file and a resulting file name and sends all configuration to the resulting file.

The syntax is as follows:

```
python[3] <source-path-for-the-script> <source-path-for-the-rsi-file> <resulting-file-name>
```

For example (doing this on my Windows machine):

```
python3 "C:\Users\user\Documents\Coding\Python\script-to-extract-config-from-rsi\extract-config-script.py" "C:\Users\iser\Documents\Coding\Python\script-to-extract-config-from-rsi\test-rsi.txt" "config-file.txt"
```

The resulting file will always be created in the Downloads directory regardless of OS.