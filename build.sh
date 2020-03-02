#!/bin/bash
echo Building and running slow:
nasm -felf64 slow.asm && ld slow.o -o slow && time ./slow
echo 

echo Building and running fast:
nasm -felf64 fast.asm && ld fast.o -o fast && time ./fast
echo




