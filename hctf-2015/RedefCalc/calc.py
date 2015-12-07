import re
import numpy as np
from pwn import *

def docalc(s,type):
	mod=1000000007
	if type==0:
		nums=re.split(r'[\+\-\*\\]',s)
		ops=re.split(r'[0-9]+',s)[1:-1]
	else:
		l=s.find('[')
		r=s.find(']')
		nums=s[l+1:r].split(',')
		ops=s[r+1:]
	if len(ops)+1 != len(nums):
		print 'strange thing!'
		exit()
	l=len(nums)
	context.log_level='info'
	c=process('/home/user/Desktop/calc.out')	
	c.sendline(str(l))
	for num in nums:
		c.send(num+' ')
	for op in ops:
		if op=='+':
			c.send('0 ')
		elif op=='-':
			c.send('1 ')
		elif op=='*':
			c.send('2 ')
	ans=c.recv().strip()
	c.close()
	context.log_level='debug'
	print ans
	return ans

	ans=np.zeros((l,l),dtype=np.int64)
	prob=np.zeros((l,l),dtype=np.int64)
	C=np.zeros((l+1,l+1),dtype=np.int64)
	C[1][1]=1
	for i in xrange(l+1):
		C[i][0]=1
		for j in range(i+1)[1:]:
			C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod
	for i in xrange(l):
		ans[i][0]=int(nums[i])
		prob[i][0]=1
	for i in xrange(l):
		if i==0:
			continue
		for j in xrange(l-i):
			for k in xrange(i):
				t2=(prob[j][k]*prob[j+k+1][i-k-1])%mod
				t2=(C[i-1][k]*t2)%mod
				prob[j][i]=(prob[j][i]+t2)%mod
				if ops[j+k]=='+':
					tmp=ans[j][k]*prob[j+k+1][i-k-1]+ans[j+k+1][i-k-1]*prob[j][k]
				elif ops[j+k]=='-':
					tmp=ans[j][k]*prob[j+k+1][i-k-1]-ans[j+k+1][i-k-1]*prob[j][k]
				elif ops[j+k]=='*':
					tmp=ans[j][k]*ans[j+k+1][i-k-1]
				tmp=tmp%mod
				tmp=(tmp*C[i-1][k])%mod
				ans[j][i]=(ans[j][i]+tmp)%mod
	return int(ans[0][l-1])

c=remote('120.55.113.21',4799)
context.log_level='debug'
c.recv()
c.sendline('12121')
c.recv()
c.sendline('a')
print '1',c.recv()
print '2',c.recv()
#print '3',c.recv()
#print '4',c.recv()
c.sendline('31')
c.recv()
d=c.recv()
d=d[:d.find('sum')]
print d
c.sendline(str(docalc(d,0)))
d=c.recv()
d=d[:d.find('sum')]
c.sendline(str(docalc(d,0)))
d=c.recv()
d=d[:d.find('sum')]
c.sendline(str(docalc(d,0)))
c.recv()
c.recv()
#c.recv()
#c.recv()
c.sendline('159001')
c.recv()
d=c.recv().strip()
c.sendline(str(docalc(d,1)))
print c.recv()
while True:
	d=c.recv().strip()
	if d.find('[')==-1:
		print d
		break
	c.sendline(str(docalc(d,1)))
while True:
	d=c.recvline().strip()
	if d.find('[')==-1:
		print d
		break
	c.sendline(str(docalc(d,1)))
c.recvline()
c.recvline()
while True:
	d=c.recvline().strip()
	if d.find('[')==-1:
		print d
		break
	c.sendline(str(docalc(d,1)))
print '1', c.recv()
print '2', c.recv()
