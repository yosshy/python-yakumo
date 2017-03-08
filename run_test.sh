#!/bin/bash

DIR=`dirname $0`

if [ -n "$1" ]; then
        TESTS=${DIR}/yakumo/smoketests/st$1*.py
else
        TESTS=${DIR}/yakumo/smoketests/st*.py
fi

export PYTHONPATH=${DIR}
for test in ${TESTS}; do
        case $test in
        *_admin.py) ${test} --os-cloud=packstack;;
        *) ${test} --os-cloud=packstackdemo;;
        esac
done
