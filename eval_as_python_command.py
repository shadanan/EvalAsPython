# Make a bunch of packages available to eval
import os
import sys
import time
import subprocess

import re
import string

import struct
import codecs

import datetime
import calendar
import collections
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
import traceback
import sublime
import sublime_plugin

from . import requests


_cwd = os.path.expanduser('~')
def _set_cwd(cwd):
    global _cwd
    _cwd = cwd


def sh(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=_cwd)
    stdout, stderr = popen.communicate()
    return stdout.decode('utf-8'), stderr.decode('utf-8')


class AbstractEvalAsPython(sublime_plugin.TextCommand):
    def exec_and_eval(self, expr):
        folders = self.view.window().folders()
        if len(folders) > 0:
            _set_cwd(folders[0])
        else:
            _set_cwd(os.path.expanduser('~'))

        module = ast.parse(expr)

        if len(module.body) == 0:
            self.counts['empty'] += 1
            return None

        if type(module.body[-1]) != ast.Expr:
            self.counts['non_expression'] += 1
            return eval(compile(module, '<string>', 'exec'))

        eval(compile(ast.Module(module.body[:-1]), '<string>', 'exec'))
        result = eval(compile(ast.Expression(module.body[-1].value), '<string>', 'eval'))

        if result is None:
            self.counts['none'] += 1

        return result

    def write(self, edit, region, result):
        raise Exception("Method is abstract")

    def run(self, edit):
        try:
            self.counts = {'empty': 0, 'non_expression': 0, 'none': 0, 'total': len(self.view.sel())}
            results = [(self.exec_and_eval(self.view.substr(region)), region) 
                       for region in reversed(self.view.sel())]

            for result, region in results:
                if result is not None:
                    self.write(edit, region, result)

            status = []
            status.append('Evaluated {0} {1}'.format(
                self.counts['total'], 
                'region' if self.counts['total'] == 1 else 'regions'))
            if self.counts['none'] > 0:
                status.append('{0} returned None'.format(self.counts['none']))
            if self.counts['empty'] > 0:
                status.append('{0} were empty'.format(self.counts['empty']))
            if self.counts['non_expression'] > 0:
                status.append('{0} were not expressions'.format(self.counts['non_expression']))
            sublime.status_message('; '.join(status))
        except Exception as e:
            traceback.print_exc()
            sublime.error_message('Python Exception: {0}'.format(str(e)))


class EvalAsPythonCommand(AbstractEvalAsPython):
    def write(self, edit, region, result):
        self.view.insert(edit, region.end(), "\n" + str(result))


class ReplaceAsPythonCommand(AbstractEvalAsPython):
    def write(self, edit, region, result):
        self.view.replace(edit, region, str(result))
