#!/usr/bin/python3

import sys
import re
import argparse

"""
Script to check for validity of copyright header in C files and similar.
See https://fpc-confluence.fingerprint.local/confluence/x/RQAx for details.

It is possible to create copyright year(s) that make no sense (descending
ranges, years in the future etc.) so a bit of common sense is still needed.
"""

# Non-doxygen style header
normalHeaderRgx = [
    "^/\*(",
    " \* .*",  # Optional title
    " \*)?",   # If title, then one blank line
    " \* Copyright \(c\) 20\d\d(-20\d\d)? Fingerprint Cards AB <tech@fingerprints.com>",
    " \*",
    " \* All rights are reserved.",
    " \* Proprietary and confidential.",
    " \* Unauthorized copying of this file, via any medium is strictly prohibited.",
    " \* Any use is subject to an appropriate license granted by Fingerprint Cards AB."
    # Optional description follows, we'll just stop checking here.
]

# ALGO style header with doxygen tag
doxygenHeaderRgx = [
    "^/\*\*",
    " \* @copyright",
    " \* Copyright \(c\) 20\d\d(-20\d\d)? Fingerprint Cards AB <tech@fingerprints.com>",
    " \* All rights are reserved.",
    " \* Proprietary and confidential.",
    " \* Unauthorized copying of this file, via any medium is strictly prohibited.",
    " \* Any use is subject to an appropriate license granted by Fingerprint Cards AB.",
    " \*/"
]


def decodeAscii(data):
    """ Test if data is ASCII. If so return decoded text otherwise None """
    try:
        decodeData = data.decode('ASCII')
    except UnicodeDecodeError:
        return None
    else:
        return decodeData


def isCopyrightOk(data):
    """ Check for copyright """

    # We try to match both, and one or the other should match.
    doxMatch = re.search(
        "(\n|\r\n?)".join(doxygenHeaderRgx), data, flags=re.MULTILINE)
    normalMatch = re.search(
        "(\n|\r\n?)".join(normalHeaderRgx), data, flags=re.MULTILINE)

    if doxMatch is None and normalMatch is None:
        return False
    else:
        return True


def checkFile(fileName):
    """ Check fileName for copyright and ASCII """

    # Read the file
    with open(fileName, "rb") as ff:
        data = ff.read()

    # Check that we have ASCII only
    decodeData = decodeAscii(data)

    if decodeData is None:
        # We have a ASCII failure
        print("--------------------------------------------")
        print(fileName + " contains not ASCII characters")
        failLines = []
        lineNumber = 0

        # Help the author to detect which lines are non-ASCII
        # This detailed analysis is done for hte first failing file
        # after that we know that we have a failure
        # This is done to speed up the general flow of the verifier
        for lineNumber, line in enumerate(data.split(b"\n")):
            try:
                line.decode('ASCII')
            except UnicodeDecodeError:
                failLines.append(str(lineNumber))

        # Print the detected lines
        print(" -> check line(s) " + str(",".join(failLines)))
        print("--------------------------------------------")
        # Exit
        sys.exit(1)

    checkCopyright = isCopyrightOk(decodeData)
    failed_file = ''
    if not checkCopyright:
        # print("--------------------------------------------")
        # print(fileName + " fails the copyright check")
        # print("--------------------------------------------")
        failed_file = fileName
    return failed_file

# Loop all file names given via stdin
# for fileName in sys.argv[1:]:
#     checkFile(fileName)
#
# # If we end here we are fine
# print("All " + str(len(sys.argv[1:])) + " files check ok")
