from struct import unpack

f=open('code','rb')
size=unpack('I',f.read(4))[0]
print size
cmds=''
def makejmp(x):
    if x==size:
        return 'finish\n'
    else:
        return 'jmp %d\n' % x
for i in range(size):
    a,b,c,d=unpack('IIII',f.read(16))
    cmds+='---cmd: %d---\n' % i
    if a==0:
        cmds+='++regs[%d]\n' % b
        cmds+=makejmp(c)
    if a==1:
        cmds+='if regs[%d]\n' % b
        cmds+='\t--regs[%d]\n' % b
        cmds+='\t'+makejmp(c)
        cmds+='else\n'
        cmds+='\t'+makejmp(d)
    if a==2:
        cmds+='save regs all\n'
        cmds+='call %d\n' % c
        if b!=0:
            cmds+='store regs 0-%d\n'%(b-1)
        cmds+=makejmp(d)
print cmds
