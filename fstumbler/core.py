#
#   This file is part of the fstumbler library.
#   Copyright (C) 2024  Ferit Yiğit BALABAN
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#   
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#   
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#   USA.

import os

import shutil
from typing import Optional
from node import Node
from util import fast_forward


def tumble(root_directory: str) -> Optional[Node]:
    if not os.path.exists(root_directory):
        return None
    
    full_path = os.path.abspath(root_directory)
    name = os.path.basename(full_path)
    root = Node(os.path.dirname(full_path), name)
    pointer = root
    
    for rootname, dirnames, filenames in os.walk(full_path):
        for filename in filenames:
            node = Node(rootname, filename, False)
            pointer.next = node
            pointer = node
        
        for dirname in dirnames:
            node = Node(rootname, dirname)
            pointer.next = node
            pointer = node
    
    return root


def tree(node: Node):
    print(node.full_path)
    if node.next:
        tree(node.next)


