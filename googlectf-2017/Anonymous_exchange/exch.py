from pwn import *
import json

context.log_level='debug'

def newacc():
    c.sendline('newacc')
    #c.recvline()

def newcard():
    c.sendline('newcard')
    #c.recvline()

def assoc(card,account):
    c.sendline('assoc %s %s'% (card,account))
    #c.recvline()

c = remote('anon.ctfcompetition.com', 1337)
c.recvuntil('emojified backup.\n')
newcard()
for i in range(3):
    newacc()
    assoc("ccard0x1",'uaccount0x%x'%(i+1))
    assoc("ucard0x1",'uaccount0x%x'%(i+1))
newcard()
assoc('ucard0x2','uaccount0x1')
assoc('ucard0x2','uaccount0x2')
assoc('ccard0x2','uaccount0x3')
for i in range(3,0x41):
    newacc()
    assoc("ccard0x%x"%(i-1),'uaccount0x%x'%(i+1))
    assoc("ccard0x%x"%(i),'uaccount0x%x'%(i+1))
c.recvuntil("Card ccard0x40 associated with account uaccount0x41.\n")
c.sendline('backup')
t=c.recvuntil('\n\n')
dat=json.loads(t)
print len(dat)
print '---'
mcards={}
mflag={}
macc={}
for ele in dat:
    macc[ele["account"]]=len(ele["cards"])
    for item in ele["cards"]:
        if item.has_key("flagged"):
            assert item["flagged"]=='1'
            if mflag.get(item["card"])==None:
                mflag[item["card"]]=1
            else:
                mflag[item["card"]]+=1
        if mcards.get(item["card"])==None:
            mcards[item["card"]]=[ele["account"]]
        else:
            mcards[item["card"]].append(ele["account"])
print len(macc)
print len(mcards)
print len(mflag)
cnt={}
for i in range(6):
    cnt[i]=0
for k in mcards:
    cnt[len(mcards[k])]+=1
print cnt

cands=[]
for k in mcards:
    if len(mcards[k])==3:
        cand=True
        for a in mcards[k]:
            if macc[a]!=3:
                cand=False
                break
        if cand:
            cands.append(k)

'''
print cands
for i in cands:
    print i in mflag
    print mcards[i]
'''
head=''
ans=''
ltmp=[]
for i in range(len(cands)):
    for j in range(i+1,len(cands)):
        mtmp={}
        for a in mcards[cands[i]]:
            mtmp[a]=1
        for a in mcards[cands[j]]:
            mtmp[a]=1
        if len(mtmp)==3:
            print cands[i],cands[j],cands[i] in mflag, cands[j] in mflag
            if cands[i] in mflag or cands[j] in mflag:
                ans+='1'
            else:
                ans+='0'
            assert len(ltmp)==0
            for a in mtmp:
                ltmp.append(a)


assert len(ltmp)!=0
assert len(ans)==1
mcnt={}
for ele in dat:
    if ele["account"] in ltmp:
        for item in ele["cards"]:
            if mcnt.get(item["card"])==None:
                mcnt[item["card"]]=1
            else:
                mcnt[item["card"]]+=1
for a in mcnt:
    if mcnt[a]==1:
        assert head==""
        head=a
print head
visited = {}
for a in ltmp:
    visited[a]=1
for i in range(1,0x40):
    if head in mflag:
        ans+='1'
    else:
        ans+='0'
    for a in mcards[head]:
        if visited.get(a)==None:
            curacc=a
            visited[a]=1
            break
    for ele in dat:
        if ele["account"] == curacc:
            assert macc[curacc]==2
            for item in ele["cards"]:
                if item["card"]!=head:
                    nexthead=item["card"]
                    break
    head = nexthead
        
print ans
c.recvuntil('no spaces.\n')
c.sendline(ans)
c.recv()
c.interactive()
