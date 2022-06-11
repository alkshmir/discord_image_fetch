#!/bin/bash

find original_html -name '*.html' -print0 | xargs -0 -n1 python -u image_fetch.py