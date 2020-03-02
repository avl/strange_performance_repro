global    _start

section   .text
         
_start:   xor       rax, rax
          xor       rcx, rcx
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop
          nop                       ;Removing this nop increases performance by a factor of 2x
          
loop0:    add       rax, 1
          mov       rdx, rax
          and       rdx, 1
          add       rcx, rdx
          cmp       rcx, 1000000000
          jne       loop0
                
          mov       rax, 60         ; system call for exit
          xor       rdi, rdi        ; exit code 0
          syscall                   ; invoke operating system to exit                    

