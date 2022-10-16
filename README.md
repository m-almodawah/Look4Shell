# Look4Shell

This tool allows you to dump Java classes from memory dumps. You can use it to dump Java classes injected by exploiting Log4Shell vulnerability or any other Java vulnerability

```
usage: look4shell.py [-h] File Directory

Look4Shell V 1.0. Author: Mohammed Almodawah. This tool allows you to dump java classes from memory dumps.

positional arguments:
  File        Path to your memory dump file
  Directory   Path of where you want to dump the extracted java classes

optional arguments:
  -h, --help  show this help message and exit
```

Example:

```
user@host:~/# python look4shell.py YourMemDump.mem YourOutputFolder

Author: Mohammed Almodawah

Look4Shell V 1.0

Dumping Java Classes....

Class name: ExploitI1C2uUY3nF
Class size: 1244 bytes
MD5 hash: 0a713b1453e8dcd81f6fb42307d1af37
...
...
...
Total classes found: 14

```

