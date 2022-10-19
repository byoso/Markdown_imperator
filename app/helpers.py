#! /usr/bin/env python3
# coding: utf-8

from silly_db.selections import Selection

def intersection(*args):
    args = [set(arg) for arg in args]
    inter = list(set.intersection(*args))
    return inter
