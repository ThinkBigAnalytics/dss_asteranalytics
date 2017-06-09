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
            return ''