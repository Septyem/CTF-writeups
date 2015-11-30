import os
import base64
import hashlib
from itertools import product
from pwn import *


def cycleLen(place):
	global next
	global clen
	seen={}
	count=0
	while not place in seen:
		if next[place]==-1:
			count+=clen[place]
			break
		seen[place]=1
		count+=1
		place=next[place]
	return count

def dosign():
	res=1
	for i in xrange(256):
		res*=cycleLen(i)
	return res

def dotest(node,top):
	global basenow
	global next
	global tree
	global testcase
	if top==0:
		for p in testcase:
			for j in range(128):
				next[128+j]=ord(p[0][j])
			ans=dosign()
			next[128+node]=128+node
			ansbase=dosign()
			if ans*basenow!=p[1]*ansbase:
				#print ans
				#print p[1]
				#print next
				return False	
		return True
	upperl=len(tree[top])
	lowerl=len(tree[top-1])
	for iter in product(range(lowerl),repeat=upperl):
		for j in range(upperl):
			next[tree[top][j]]=tree[top-1][iter[j]]
		find=dotest(node,top-1)
		if find:
			return True

def docalc(s,len):
	global proof
	if len==20:
		if hashlib.sha1(s).digest().endswith('\x00\x00\x00'):
			proof=s
			return True
		else:
			return False
	for i in xrange(256):
		if docalc(s+chr(i),len+1):
			return True

c=remote('wob-key-e1g2l93c.9447.plumbing',9447)
#c=remote('127.0.0.1',9447)
res=c.recv()
proof='sth\n'
docalc(res,12)
c.send(proof)
c.recv()
t=128
msg=''
for i in range(126):
	t+=1
	msg+=chr(t)
msg+=chr(128)
msg+=chr(255)
c.sendline('1')
c.send(base64.b64encode(msg))
base=int(c.recvline())
#print base
c.recv()
clen=[-1]*128
next=[-1]*256
final=[-1]*128
for i in xrange(128):
	msg=msg[:127]+chr(i)
	#print msg
	c.sendline('1')
	c.send(base64.b64encode(msg))
	ans=int(c.recvline())
	c.recv()
	clen[i]=ans/base-1
	if clen[i]>256:
		print 'failed lalala!'
		exit()
print clen
msg=msg[:126]+chr(254)+chr(255)
c.sendline('1')
c.send(base64.b64encode(msg))
base=int(c.recvline())
#print base
c.recv()
for i in xrange(128):
	for j in xrange(128):
		if clen[j]==128+i:
			msg=msg[:127]+chr(j)
			#print msg
			c.sendline('1')
			c.send(base64.b64encode(msg))
			ans=int(c.recvline())
			c.recv()
			tmp=257+i-ans/base
			final[j]=tmp
			if i==0:
				next[j]=tmp
son=[-1]*128
for i in range(128):
	son[i]=i
for i in xrange(128):
	tree=[]
	for j in xrange(128):
		tree.append([])
	for j in xrange(128):
		if final[j]==i+128:
			tree[clen[j]-128].append(j)
	top=127
	while top>=0 and len(tree[top])==0:
		top-=1
	if top<=0:
		continue
	print tree
	msg=''
	for j in xrange(128):
		nextj=(j+1)%128
		if nextj==i:
			msg+=chr(128+(nextj+1)%128)
		elif j==i:
			msg+=chr(128+j)
		else:
			msg+=chr(128+nextj)
				
	c.sendline('1')
	c.send(base64.b64encode(msg))
	basenow=int(c.recvline())
	c.recv()
	testcase=[]
	savetop=top
	while top>0:
		upperl=len(tree[top])
		lowerl=len(tree[top-1])
		for j in xrange(lowerl-1):
			aa=tree[top-1][j]
			c.sendline('1')
			msg1=msg[:i]+chr(aa)+msg[i+1:]
			c.send(base64.b64encode(msg1))
			ans=int(c.recvline())
			c.recv()
			testcase.append((msg1,ans))
		top-=1
	find=dotest(i,savetop)
	if not find:
		print 'WTF!!!'
		exit()
	'''
	while top>0:
		upperl=len(tree[top])
		lowerl=len(tree[top-1])
		find=False
		link=[]
		for iter in permutations(range(lowerl),upperl):
			tmpfind=True
			basetmp=basenow*2
			for k in xrange(top-1):
				for leaf in tree[k]:
					basetmp=basetmp/(k+2)*(k+3)
			for j in xrange(lowerl-1):
				basetmp=basetmp/(top+1)*(top+2)
			for j in xrange(lowerl-1):
				aa=tree[top-1][j]
				c.sendline('1')
				msg1=msg[:i]+chr(aa)+msg[i+1:]
				c.send(base64.b64encode(msg1))
				ans=int(c.recvline())
				c.recv()
				basetmp1=basetmp
				k=top
				while len(tree[k])!=0:
					for leaf in tree[k]:
						ind=tree[top].index(son[leaf])
						if iter[ind]!=j:
							basetmp1=basetmp1/(k+2)*(k+3)
					k+=1
				if basetmp1!=ans:
					print iter
					print top
					print ans
					print basetmp1
					print basetmp
					tmpfind=False
					break
			if tmpfind:
				find=True
				link=iter
				break
		
		if not find:
			print 'WTF!!!!'
			exit()
				
		for j in xrange(upperl):
			son[tree[top][j]]=tree[top-1][link[j]]
			next[tree[top][j]]=tree[top-1][link[j]]
			
		for leaf in tree[top]:
			k=top+1
			while len(tree[k])!=0:
				for leaf2 in tree[k]:
					if son[leaf2]==leaf:
						son[leaf2]=son[leaf]	
				k+=1
		top-=1
	'''

print next
context.log_level='debug'
c.sendline('2')
for i in range(0x11):
	c.recvline()
	req=base64.b64decode(c.recvline())
	for j in range(128):
		next[128+j]=ord(req[j])
	ans=str(dosign())
	c.send(ans+'\x20'*(620-len(ans)))
c.recv()
c.recv()


