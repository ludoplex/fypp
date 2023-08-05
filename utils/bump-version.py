#!/usr/bin/env python3
import sys
import re
import os

VERSION_PATTERN = r'\d+\.\d+(?:\.\d+)?(?:-\w+)?'
FILES_PATTERNS = [
    (
        'bin/fypp',
        f"""^VERSION\s*=\s*([\'"]){VERSION_PATTERN}\1""",
        "VERSION = '{version}'",
    ),
    (
        'docs/fypp.rst',
        f'Fypp Version[ ]*{VERSION_PATTERN}.',
        'Fypp Version {shortversion}.',
    ),
    (
        'setup.py',
        f"""version\s*=\s*([\'"]){VERSION_PATTERN}\1""",
        "version='{version}'",
    ),
    (
        'docs/conf.py',
        f"""version\s*=\s*([\'"]){VERSION_PATTERN}\1""",
        "version = '{shortversion}'",
    ),
    (
        'docs/conf.py',
        f"""release\s*=\s*([\'"]){VERSION_PATTERN}\1""",
        "release = '{version}'",
    ),
]

if len(sys.argv) < 2:
    print("Missing version string")
    sys.exit(1)


version = sys.argv[1]
shortversion = '.'.join(version.split('.')[:2])

match = re.match(VERSION_PATTERN, version)
if match is None:
    print("Invalid version string")
    sys.exit(1)

rootdir = os.path.join(os.path.dirname(sys.argv[0]), '..')
for fname, regexp, repl in FILES_PATTERNS:
    fname = os.path.join(rootdir, fname)
    print(f"Replacments in '{fname}': ", end='')
    with open(fname, 'r') as fp:
        txt = fp.read()
    replacement = repl.format(version=version, shortversion=shortversion)
    newtxt, nsub = re.subn(regexp, replacement, txt, flags=re.MULTILINE)
    print(nsub)
    with open(fname, 'w') as fp:
        fp.write(newtxt)
# Replace version number in Change Log and adapt decoration below
fname = os.path.join(rootdir, 'CHANGELOG.rst')
print(f"Replacments in '{fname}': ", end='')
with open(fname, 'r') as fp:
    txt = fp.read()
decoration = '=' * len(version)
newtxt, nsub = re.subn(
    '^Unreleased\s*\n=+', version + '\n' + decoration, txt, 
    count=1, flags=re.MULTILINE)
print(nsub)
with open(fname, 'w') as fp:
    fp.write(newtxt)
