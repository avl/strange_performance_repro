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
    s = []
    try:
        os.mkdir("output")
    except: pass

    for x in range(365):
        loopstart = x+6
        loopend = x+0x1b+1
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
        s.append(elapsed)
        avg = sum(s)/len(s)
        outcome="other"
        if elapsed > avg:
            outcome="slow"
        else:		
            outcome="fast"
        single_cacheline=False
        if loopstart/64 == loopend/64:
            single_cacheline=True
        lastcount+=1
        if outcome!=last:
            last=outcome
            print " ^ This is %d in a row"%(lastcount)
            lastcount=0
        #print "Adding %d NOP-instructions gave a %s program (innerloop is %s)"%(x,outcome,"single cacheline" if single_cacheline else "spanning two cachelines")
        print "Adding %d NOP-instructions gave a %s program"%(x,outcome)
        os.system("mv prog.asm output/prog%s%s.asm"%(x,outcome))
        os.system("mv prog.o output/prog%s%s.o"%(x,outcome))
        os.system("mv prog output/prog%s%s"%(x,outcome))
        


if __name__=='__main__':
    run()
    
