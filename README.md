# TLDR

I have two programs which are almost identical (I copied them out of the compiler output for [rust issue 69593](https://github.com/rust-lang/rust/issues/69593) ). 

One of them is [fast](https://github.com/avl/strange_performance_repro/blob/master/fast.asm) .

The other is [slow](https://github.com/avl/strange_performance_repro/blob/master/slow.asm) .

On my machine the slow program takes twice the time of the fast one.


# Introduction

This repo contains a minimal reproduction of a performance issue originally reported at [rust issue 69593](https://github.com/rust-lang/rust/issues/69593) .

After looking at the assembly of the two programs (struct and trait) from that issue, it was evident that the actual inner loop was identical.
Reasonably, all the time had to be spent in that inner loop of six instructions:

````
loop0:    add       rax, 1
          mov       rdx, rax
          and       rdx, 1
          add       rcx, rdx
          cmp       rcx, 1000000000
          jne       loop0
```` 

On my machine (Ryzen 9 3900X), this exact loop sometimes takes 450 ms, sometimes 900 ms. I just had to know why! 

## Approach

I started by cutting out the inner loop and making an assembly program with only the loop. See [here](https://github.com/avl/strange_performance_repro/blob/master/fast.asm) . Compiling (eh, I mean 'assembling') the program requires the 'nasm' assembler, available in the package manager of all linux distros.

At first I experimented with adding nop-instructions before the loop0 part, to see if alignment of the loop would make a difference. Perhaps aligning the loop on a multiple of 8 bytes would help (no, that made no difference)?

After some trial and error I got fed up and wrote a python-program which tried generating programs with 0 nops, 1 nop, 2 nops, 3 nops etc.

See the program here: [here](https://github.com/avl/strange_performance_repro/blob/master/driver.py)

Running this program gave the following output:

(Initial warm-up as the program determines the average runtime skipped)

````
Adding 38 NOP-instructions gave a slow program
Adding 39 NOP-instructions gave a slow program
Adding 40 NOP-instructions gave a slow program
Adding 41 NOP-instructions gave a slow program
Adding 42 NOP-instructions gave a slow program
Adding 43 NOP-instructions gave a slow program
Adding 44 NOP-instructions gave a slow program
Adding 45 NOP-instructions gave a slow program
Adding 46 NOP-instructions gave a slow program
Adding 47 NOP-instructions gave a slow program
Adding 48 NOP-instructions gave a slow program
Adding 49 NOP-instructions gave a slow program
Adding 50 NOP-instructions gave a slow program
Adding 51 NOP-instructions gave a slow program
Adding 52 NOP-instructions gave a slow program
Adding 53 NOP-instructions gave a slow program
Adding 54 NOP-instructions gave a slow program
Adding 55 NOP-instructions gave a slow program
Adding 56 NOP-instructions gave a slow program
Adding 57 NOP-instructions gave a slow program
 ^ This is 22 in a row
Adding 58 NOP-instructions gave a fast program
Adding 59 NOP-instructions gave a fast program
Adding 60 NOP-instructions gave a fast program
Adding 61 NOP-instructions gave a fast program
Adding 62 NOP-instructions gave a fast program
Adding 63 NOP-instructions gave a fast program
Adding 64 NOP-instructions gave a fast program
Adding 65 NOP-instructions gave a fast program
Adding 66 NOP-instructions gave a fast program
Adding 67 NOP-instructions gave a fast program
Adding 68 NOP-instructions gave a fast program
Adding 69 NOP-instructions gave a fast program
Adding 70 NOP-instructions gave a fast program
Adding 71 NOP-instructions gave a fast program
Adding 72 NOP-instructions gave a fast program
Adding 73 NOP-instructions gave a fast program
Adding 74 NOP-instructions gave a fast program
Adding 75 NOP-instructions gave a fast program
Adding 76 NOP-instructions gave a fast program
Adding 77 NOP-instructions gave a fast program
Adding 78 NOP-instructions gave a fast program
Adding 79 NOP-instructions gave a fast program
Adding 80 NOP-instructions gave a fast program
Adding 81 NOP-instructions gave a fast program
Adding 82 NOP-instructions gave a fast program
Adding 83 NOP-instructions gave a fast program
Adding 84 NOP-instructions gave a fast program
Adding 85 NOP-instructions gave a fast program
Adding 86 NOP-instructions gave a fast program
Adding 87 NOP-instructions gave a fast program
Adding 88 NOP-instructions gave a fast program
Adding 89 NOP-instructions gave a fast program
Adding 90 NOP-instructions gave a fast program
Adding 91 NOP-instructions gave a fast program
Adding 92 NOP-instructions gave a fast program
Adding 93 NOP-instructions gave a fast program
Adding 94 NOP-instructions gave a fast program
Adding 95 NOP-instructions gave a fast program
Adding 96 NOP-instructions gave a fast program
Adding 97 NOP-instructions gave a fast program
Adding 98 NOP-instructions gave a fast program
Adding 99 NOP-instructions gave a fast program
 ^ This is 42 in a row
Adding 100 NOP-instructions gave a slow program
Adding 101 NOP-instructions gave a slow program
Adding 102 NOP-instructions gave a slow program
Adding 103 NOP-instructions gave a slow program
Adding 104 NOP-instructions gave a slow program
Adding 105 NOP-instructions gave a slow program
Adding 106 NOP-instructions gave a slow program
Adding 107 NOP-instructions gave a slow program
Adding 108 NOP-instructions gave a slow program
Adding 109 NOP-instructions gave a slow program
Adding 110 NOP-instructions gave a slow program
Adding 111 NOP-instructions gave a slow program
Adding 112 NOP-instructions gave a slow program
Adding 113 NOP-instructions gave a slow program
Adding 114 NOP-instructions gave a slow program
Adding 115 NOP-instructions gave a slow program
Adding 116 NOP-instructions gave a slow program
Adding 117 NOP-instructions gave a slow program
Adding 118 NOP-instructions gave a slow program
Adding 119 NOP-instructions gave a slow program
Adding 120 NOP-instructions gave a slow program
Adding 121 NOP-instructions gave a slow program
 ^ This is 22 in a row
Adding 122 NOP-instructions gave a fast program
Adding 123 NOP-instructions gave a fast program
Adding 124 NOP-instructions gave a fast program
Adding 125 NOP-instructions gave a fast program
Adding 126 NOP-instructions gave a fast program
Adding 127 NOP-instructions gave a fast program
Adding 128 NOP-instructions gave a fast program
Adding 129 NOP-instructions gave a fast program

````

The pattern repeats itself with a period of 64 bytes. After inspecting the actual generated programs, it became evident that the critical factor is whether the inner loop spans two cache lines or is located all in one cache line. Why this makes such a big difference I don't know, but I do find it fascinating.

The python-program puts each program it generates in a folder named ````output/```` where the programs can be inspected.



