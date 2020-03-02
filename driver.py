import time
import os

def makeprog(nops):
    nops = "".join(["nop\n" for x in range(nops)])

    return """global    _start
    section   .text
    _start:   xor       rax, rax
          xor       rcx, rcx
          %s
    loop0:    add       rax, 1
          mov       rdx, rax
          and       rdx, 1
          add       rcx, rdx
          cmp       rcx, 100000000
          jne       loop0
                
          mov       rax, 60         ; system call for exit
          xor       rdi, rdi        ; exit code 0
          syscall                   ; invoke operating system to exit
    """%(nops)
    
    
def run():
    last=""
    lastcount=0
    for x in range(65):
        progtext = makeprog(x)
        f=open("prog.asm","w")
        f.write(progtext)
        f.close()
        if os.system("nasm -felf64 prog.asm && ld prog.o -o prog")!=0:
            print "build failed"
            return
        t0 = time.time()
        if os.system("./prog")!=0:
            print "call failed"
            return
        t1 = time.time()
        
        elapsed = t1-t0
        elapsed*=10.0
        outcome="other"
        if elapsed >= 0.4 and elapsed < 0.68:
            print "%d was fast"%x
            outcome="fast"
        elif elapsed >= 0.8 and elapsed < 1.3:
            print "%d was slow"%x
            outcome="slow"
        elif elapsed <0.4:
            print "%d was suspiciously fast"%x
        elif elapsed >1.1:
            print "%d was very slow"%x
        else:
            print "%d was in the middle"%x
        lastcount+=1
        if outcome!=last:
            last=outcome
            print " ^ This is %d in a row"%(lastcount)
            lastcount=0
        os.system("mv prog.asm prog%s%s.asm"%(x,outcome))
        os.system("mv prog.o prog%s%s.o"%(x,outcome))
        os.system("mv prog prog%s%s"%(x,outcome))
        


if __name__=='__main__':
    run()
    
