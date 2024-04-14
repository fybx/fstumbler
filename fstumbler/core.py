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


def tumble(root_directory: str) -> Node:
    """Tumbles down from the root directory, essentially mapping all subdirectories and files.

    Args:
        root_directory (str): Root directory to start from

    Returns:
        Node: The root directory's node
    
    Raises:
        FileNotFoundError: if the root_directory is not an existing file 
    """
    if not os.path.exists(root_directory):
        raise FileNotFoundError(root_directory)
    
    root = Node(os.path.dirname(root_directory), os.path.basename(root_directory), directory=True)
    pointer = root
    
    first = True
    for rootname, _, filenames in os.walk(os.path.abspath(root_directory)):
        if first:
            first = False
        else:
            node = Node(os.path.dirname(rootname), os.path.basename(rootname), directory=True)
            pointer.next = node
            pointer = node
        
        for name in filenames:
            node = Node(rootname, name, directory=False)
            pointer.next = node
            pointer = node
    
    return root


def tree(node: Node):
    """Prints the full names of files and directories in a linked list.

    Args:
        node (Node): Start node
    """
    pointer = node
    while pointer:
        print(pointer.full_path)
        pointer = pointer.next


def dry_cp(source: Node, destination: Node):
    if not source.directory:
        select = fast_forward(destination, True)
        keep = select.next
        select.next = source.copyWith(select.parent, select.name, False)
        select.next.next = keep
        return
    
    pSrc, pDst = source, fast_forward(destination)
    while pSrc:
        pDst.next = pSrc.copyWith(pDst.full_path if pDst.directory else pDst.parent,
                                  pSrc.name, pSrc.directory)
        pSrc, pDst = pSrc.next, pDst.next


def cp(source: Node, destination: Node):
    if not source.directory:
        select = fast_forward(destination, True)
        keep = select.next
        select.next = source.copyWith(select.parent, select.name, False)
        select.next.next = keep
        shutil.copy(source.full_path, select.next.full_path)
        return
    
    pSrc, pDst = source, fast_forward(destination)
    while pSrc:
        pDst.next = pSrc.copyWith(pDst.full_path if pDst.directory else pDst.parent,
                                  pSrc.name, pSrc.directory)
        
        if pSrc.directory:
            os.makedirs(pDst.next.full_path, exist_ok=True)
        else:
            shutil.copy(pSrc.full_path, pDst.next.full_path)
        pSrc, pDst = pSrc.next, pDst.next
    