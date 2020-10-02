#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

root = "/home/abel/Desktop/DB_dir_Test"
new_index = 0

for dir in os.listdir(root):
    if os.path.isdir(os.path.join(root, dir)):
        print(dir)
        os.rename(''.join([root, '/' + str(dir)]),
                  ''.join([root, '/' + str(new_index)]))
        new_index += 1

for dir in os.listdir(root):
    if os.path.isdir(os.path.join(root, dir)):
        print(dir)

shutil.copytree("/home/abel/Desktop/DB_dir_Test/1", "/home/abel/Desktop/1_Ca_marche")