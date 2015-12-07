import Image

im=Image.open('flag.png')

row=283
col=20
mid=75/2
accu=14
data=[]
for i in xrange(row):
	for j in xrange(col):
		basex=j*80+15
		basey=i*80+15
		#print basex,basey
		if im.getpixel((basex,basey))[0]!=255:
			basex+=mid
			num=0
			for k in xrange(6):
				num=num*2
				if im.getpixel((basex,basey))[0]!=255:
					num+=1
				basey+=accu
			data.append(num)
		else:
			data.append(-1)
print data
'''
>>> f=open('/home/user/Desktop/fuli.txt')
>>> s=f.read()
>>> data=eval(s)

>>> d={}
>>> for i in range(64):
...     d[i]=0
... 
>>> d[-1]=0
>>> d
{0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0, 41: 0, 42: 0, 43: 0, 44: 0, 45: 0, 46: 0, 47: 0, 48: 0, 49: 0, 50: 0, 51: 0, 52: 0, 53: 0, 54: 0, 55: 0, 56: 0, 57: 0, 58: 0, 59: 0, 60: 0, 61: 0, 62: 0, 63: 0, -1: 0}
>>> for i in data:
...     d[i]+=1

>>> a=[]
>>> for i in range(64):
...     if d[i-1]!=0:
...             a.append((i,d[i]))
... 
>>> sorted(a,key=lambda x:x[1])
[(48, 2), (7, 3), (32, 4), (39, 7), (38, 32), (0, 45), (16, 70), (37, 70), (1, 83), (4, 97), (25, 100), (56, 111), (59, 118), (61, 125), (63, 125), (47, 149), (2, 214), (55, 295), (17, 298), (57, 298), (3, 306), (8, 339), (41, 354), (34, 388), (58, 435), (23, 585)]
>>> a1=sorted(a,key=lambda x:x[1])
>>> o='ETAONRISHDLUFWCMGYPBVKJQXZ'
>>> da={}
>>> for i in range(26):
...     da[a1[i][0]]=o[26-i]
... 
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
IndexError: string index out of range
>>> for i in range(26):
...     da[a1[i][0]]=o[25-i]
... 
>>> da={}
>>> for i in range(26):
...     da[a1[i][0]]=o[25-i]
... 
>>> da
{0: 'V', 1: 'Y', 2: 'D', 3: 'R', 4: 'G', 7: 'X', 8: 'N', 16: 'B', 17: 'S', 23: 'E', 25: 'M', 32: 'Q', 34: 'A', 37: 'P', 38: 'K', 39: 'J', 41: 'O', 47: 'L', 48: 'Z', 55: 'H', 56: 'C', 57: 'I', 58: 'T', 59: 'W', 61: 'F', 63: 'U'}
>>> ans=''
>>> for ch in data:
...     if ch==-1:
...             ans+=' '
...     else:
...             ans+=da[ch]
... 
>>> f=open('/home/user/Desktop/fulians.txt')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: [Errno 2] No such file or directory: '/home/user/Desktop/fulians.txt'
>>> f=open('/home/user/Desktop/fulians.txt','w')
>>> f.write(ans)
>>> f.close()
>>> da
{0: 'V', 1: 'Y', 2: 'D', 3: 'R', 4: 'G', 7: 'X', 8: 'N', 16: 'B', 17: 'S', 23: 'E', 25: 'M', 32: 'Q', 34: 'A', 37: 'P', 38: 'K', 39: 'J', 41: 'O', 47: 'L', 48: 'Z', 55: 'H', 56: 'C', 57: 'I', 58: 'T', 59: 'W', 61: 'F', 63: 'U'}
>>> da[57]='S'
>>> da[17]='I'
>>> da
{0: 'V', 1: 'Y', 2: 'D', 3: 'R', 4: 'G', 7: 'X', 8: 'N', 16: 'B', 17: 'I', 23: 'E', 25: 'M', 32: 'Q', 34: 'A', 37: 'P', 38: 'K', 39: 'J', 41: 'O', 47: 'L', 48: 'Z', 55: 'H', 56: 'C', 57: 'S', 58: 'T', 59: 'W', 61: 'F', 63: 'U'}
>>> ans=''
>>> for ch in data:
...     if ch==-1:
...             ans+=' '
...     else:
...             ans+=da[ch]
... 
>>> f=open('/home/user/Desktop/fulians.txt','w')
>>> f.write(ans)
>>> f.close()
>>> 
'''
