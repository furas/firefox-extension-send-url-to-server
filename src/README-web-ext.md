#!/bin/bash

# author: Bartlomiej "furas" Burek (https://blog.furas.pl)
# date: 2024.11.21

# --- run in Firefox for test/debug ---

```
$ cd firefox-extension

$ web-ext run --verbose
```

# --- build .zip file ---

```
$ cd firefox-extension

$ web-ext build
```

# --- create .xpi file (it sends data to Mozilla Server ---

// environment values defined in .bashrc 

FIREFOX_KEY="user:xxxxxx:xxx"
FIREFOX_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

```
$ cd firefox-extension

$ web-ext sign \
  --api-key="${FIREFOX_KEY}" \
  --api-secret="${FIREFOX_SECRET}" \
  --channel 'unlisted' \
  --verbose
```
