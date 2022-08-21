#!/usr/bin/env python3
# http://zetcode.com/python/click/

# pip install colorama click

import ehh.cli

__author__ = "Lennard Voogdt"
__version__ = "1.1.1"

def main(source = None):
    ehh.cli.ls()
    
    pass

# main
if __name__ == "__main__":
    ehh.cli.ls()