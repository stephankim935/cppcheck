#!/usr/bin/env python3
#
# This script analyses Cppcheck dump files to locate threadsafety issues
# - warn about static local objects
#

import cppcheckdata
import sys


def reportError(token, severity, msg, id):
    cppcheckdata.reportError(token, severity, msg, 'threadsafety', id)


def checkstatic(data):
    for var in data.variables:
        if var.isStatic and var.isLocal:
            type = None
            if var.isClass:
                type = 'object'
            else:
                type = 'variable'
            if var.isConst:
                reportError(var.typeStartToken, 'warning', 'Local constant static ' + type + ' \'' + var.nameToken.str + '\', dangerous if it is initialized in parallel threads', 'threadsafety')
            else:
                reportError(var.typeStartToken, 'warning', 'Local static ' + type + ': ' + var.nameToken.str, 'threadsafety')


for arg in sys.argv[1:]:
    if arg.startswith('-'):
        continue
    print('Checking ' + arg + '...')
    data = cppcheckdata.parsedump(arg)
    for cfg in data.configurations:
        cfg = data.Configuration(cfg)
        if len(data.configurations) > 1:
            print('Checking ' + arg + ', config "' + cfg.name + '"...')
        checkstatic(cfg)
