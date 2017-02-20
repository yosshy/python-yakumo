#!/bin/sh
export PYTHONPATH=`dirname $0`
rm -r doc
epydoc -o doc --html yakumo/
