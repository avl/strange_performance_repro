This repo contains a minimal reproduction of a performance issue originally reported at 

https://github.com/rust-lang/rust/issues/69593 .

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

The only significant difference between the two programs is that the alignment of the loop differs by one byte.



