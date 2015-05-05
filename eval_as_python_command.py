# Make a bunch of packages available to eval
import os
import io
import sys
import time

import string
import re
import difflib
import textwrap
import unicodedata
import stringprep
import rlcompleter

import struct
import codecs

import datetime
import calendar
import collections
import heapq
import bisect
import types
import pprint

import numbers
import math
import cmath
import decimal
import fractions
import random

import itertools
import functools
import operator

import os
import stat
import glob
import fnmatch

import csv

import hashlib
import hmac

import json
import base64
import binhex
import binascii
import uu

import urllib

import ast
import sublime
import sublime_plugin

def exec_and_eval(expr):
    body = ast.parse(expr).body
    if len(body) > 0 and type(body[-1]) == ast.Expr:
        eval(compile(ast.Module(body[:-1]), '<string>', 'exec'))
        return eval(compile(ast.Expression(body[-1].value), '<string>', 'eval'))

class EvalAsPythonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            results = []
            for region in self.view.sel():
                result = exec_and_eval(self.view.substr(region))
                if result is not None:
                    results.append((result, region))

            if len(results) == 0:
                sublime.status_message('Nothing to evaluate')
            else:
                for result, region in results:
                    self.view.replace(edit, region, str(result))
                sublime.status_message('Successfully evaluated {} regions as Python'.format(len(results)))
        except Exception as e:
            sublime.error_message('Python Error: {}'.format(str(e)))
