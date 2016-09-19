from pwn import *
import re

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

sig=22611972523744021864587913335128267927131958989869436027132656215690137049354670157725347739806657939727131080334523442608301044203758495053729468914668456929675330095440863887793747492226635650004672037267053895026217814873840360359669071507380945368109861731705751166864109227011643600107409036145468092331
n=172794691472052891606123026873804908828041669691609575879218839103312725575539274510146072314972595103514205266417760425399021924101213043476074946787797027000946594352073829975780001500365774553488470967261307428366461433441594196630494834260653022238045540839300190444686046016894356383749066966416917513737L
g2p=[]
g2pv=[]
for i in range(1024):
        tmp = pow(2,(1<<i),n)
        g2p.append(tmp)
        g2pv.append(modinv(tmp,n))
ans = {}

#context.log_level = 'debug'
c = remote('crypto.chal.csaw.io',8002)
cnt=0
f = open('dlog','w')
for ii in range(100000):
        if ii % 100==0:
                print ii
        c.recvuntil(':')
        c.sendline('2')
        line = c.recvuntil('\n')
        (sig1,n1) = map(int,re.search('signature:(\d+), N:(\d+)',line).groups())
        if n1!=n:
                print 'N wrong'
                exit()
        if sig1!=sig:
                for i in range(1024):
                        if sig*g2p[i]%n==sig1:
                                if ans.get(i)==None:
                                        ans[i]=0
                                        cnt+=1
                                        f.write(str(i)+' 0\n')
                                        f.flush()
                        if sig*g2pv[i]%n==sig1:
                                if ans.get(i)==None:
                                        ans[i]=1
                                        cnt+=1
                                        f.write(str(i)+' 1\n')
                                        f.flush()
        c.recvuntil(':')
        c.sendline('yes')
        if cnt>1023:
                break
print ans
