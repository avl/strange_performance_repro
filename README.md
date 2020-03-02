This repo contains a minimal reproduction of a performance issue originally reported at [rust issue 69593](https://github.com/rust-lang/rust/issues/69593) .

There are minimal assembly programs in this repo, which differ only in one single nop-instruction.

The output of this program, on my machine, is:

```
Building and running slow:

real	0m0,899s
user	0m0,899s
sys	0m0,000s

Building and running fast:

real	0m0,450s
user	0m0,450s
sys	0m0,000s
```

The program is run on a machine with Ryzen 9 3900X, and linux ````Linux adesk 5.3.0-40-generic #32~18.04.1-Ubuntu SMP Mon Feb 3 14:05:59 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux```` 

The only significant difference between the two programs is that the alignment of the loop differs by one byte.

The fast program is [here](https://github.com/avl/strange_performance_repro/blob/master/fast.asm) .

The slow program is [here](https://github.com/avl/strange_performance_repro/blob/master/slow.asm) .



