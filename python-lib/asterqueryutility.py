# -*- coding: utf-8 -*-
'''
Copyright © 2018 by Teradata.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# -*- coding: utf-8 -*-
try:
    from sets import Set
except ImportError:
    Set = set
import json

from asterargumentfactory import *

def areStringsEqual(a, b):
    return a.upper() == b.upper()

def isStringInList(astring, blist):
    return astring.upper() in [y.upper() for y in blist]

def isArgumentDictionaryEntry(argument, x):
    argumentname = argument.get('name', '')
    entryname = x.get('name', '')
    blist = x.get('alternateNames', [])
    return areStringsEqual(argumentname, entryname) or \
        isStringInList(argumentname, blist)
    
def getArgumentClause(cargument, arg_dict, inputTables):
    argumentdef  = next(iter(x for x in arg_dict if isArgumentDictionaryEntry(cargument, x)), {})
    asterarg = AsterArgumentFactory.createArg(cargument, argumentdef, inputTables)
    return asterarg.argumentclause

def getJoinedArgumentsString(cargumentslist, arg_dict, inputTables=[]):
    return ''.join(map(lambda x: getArgumentClause(x, arg_dict, inputTables), \
                         cargumentslist))

def getArgumentClausesFromJson(f):
    return f.get('argument_clauses',[])

try:
    from dataiku.customrecipe import *
    def getJson(function_name):
        try:
            return json.loads(open('%s/data/%s' % (get_recipe_resource(),
                                               function_name + '.json')).read())
        except:
            return ''

except ImportError:
    def getJson(function_name):
        try:
            return json.loads(open('%s/data/%s' % ('../resource', function_name + '.json')).read())
        except:
            return {}
