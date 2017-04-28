# Copyright 2014-2017 by Akira Yoshiyama <akirayoshiyama@gmail.com>.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Miscellaneous functions/decorators
"""

from __future__ import print_function
import atexit
import code
import inspect
import os
import readline
import rlcompleter
import re
import sys


class Completer(rlcompleter.Completer):

    PATTERN = re.compile(r"(\w+(\.\w+)*)\.(\w*)")
    PATTERN2 = re.compile(r"([\.\w]+)\($")
    METHOD_PATTERN = re.compile(r"^\s*(def .*?\):)", re.MULTILINE | re.DOTALL)

    def help(self):
        line = readline.get_line_buffer().rstrip()
        if line == '' or line[-1] != '(':
            return
        m = self.PATTERN2.search(line)
        if not m:
            return
        try:
            thisobject = eval(m.group(1), self.namespace)
        except Exception:
            return

        if not inspect.ismethod(thisobject):
            return
        m = self.METHOD_PATTERN.match(inspect.getsource(thisobject))
        if m:
            print("")
            print(m.group(1))
            print(inspect.getdoc(thisobject).strip())
            print(sys.ps1 + readline.get_line_buffer(), end='', flush=True)

    def complete(self, text, state):
        if self.use_main_ns:
            self.namespace = __main__.__dict__

        if text == "":
            self.help()
            return None

        if state == 0:
            if "." in text:
                self.matches = self.attr_matches(text)
            else:
                self.matches = self.global_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    def attr_matches(self, text):
        """
        Derived from rlcompleter.Completer.attr_matches()
        """
        m = self.PATTERN.match(text)
        if not m:
            return []
        expr, attr = m.group(1, 3)
        try:
            thisobject = eval(expr, self.namespace)
        except Exception:
            return []

        if attr == '' and inspect.ismethod(thisobject):
            m = self.METHOD_PATTERN.match(inspect.getsource(thisobject))
            if m:
                print("")
                print(m.group(1))
                print(inspect.getdoc(thisobject).strip())
                print(sys.ps1 + readline.get_line_buffer(), end='', flush=True)

        # get the content of the object, except __builtins__
        words = dir(thisobject)
        if "__builtins__" in words:
            words.remove("__builtins__")

        if hasattr(thisobject, '__class__'):
            words.append('__class__')
            words.extend(rlcompleter.get_class_members(thisobject.__class__))
        matches = []
        n = len(attr)
        for word in words:
            if attr == '' and word[0] == '_':
                continue
            if word[:n] == attr and hasattr(thisobject, word):
                val = getattr(thisobject, word)
                word = self._callable_postfix(val, "%s.%s" % (expr, word))
                matches.append(word)
        return matches


class Console(code.InteractiveConsole):
    def __init__(self, locals_=None, filename="<console>",
                 histfile=os.path.expanduser("~/.ossh-history")):
        code.InteractiveConsole.__init__(self, locals_, filename)
        print(histfile)
        self.init_history(histfile)
        readline.set_completer(Completer(locals_).complete)

    def init_history(self, histfile):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        readline.set_history_length(1000)
        readline.write_history_file(histfile)
