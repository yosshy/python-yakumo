#!/bin/bash

DIR=`dirname $0`

if [ -n "$1" ]; then
        TESTS=${DIR}/smoketests/$1*
else
        TESTS=${DIR}/smoketests/*
fi

export PYTHONPATH=${DIR}
for test in ${TESTS}; do
        case $test in
        *.admin.py) ${test} --os-cloud=packstack;;
        *) ${test} --os-cloud=packstackdemo;;
        esac
done
