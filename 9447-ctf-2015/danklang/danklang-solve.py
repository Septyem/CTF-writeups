def isPrime(n):
    for i in xrange(2,int(n**0.5)+1):
        if n%i==0:
            return False

    return True


epic=0
such=2
bill=3
i=0
f1=1
f2=1
t=13379447
#t=10
while i<t:
    i+=1
    if i%1000000==0:
        print i
    
    if isPrime(i):
        nepic=bill+1
    else:
        nepic=such
    if i<=1:
        nepic=0

    
    if i<5:
        c=0
    else:
        c=i*(i-1)*(i-2)*(i-3)*(i-4)/5/4/3/2
    wow=c
    #print 'comb:',i,c
    if c%7==0:
        wew=bill
        wow+=1
    else:
        wew=epic
    nsuch=wow+wew

    if i<3:
        f3=1
    else:
        f3=(f1+f2)%987654321
        f1=f2
        f2=f3
    #print 'fib',i,f3
    wow=f3
    if f3%3==0:
        wew=such
        wow+=1
    else:
        wew=epic
    nbill=wow+wew

    epic=nepic
    such=nsuch
    bill=nbill
    #print i,epic,such,bill

print epic
        
