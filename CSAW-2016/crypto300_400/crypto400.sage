# copy from http://inaz2.hatenablog.com/entry/2016/01/20/022936
# 之前完全没想到small_roots的beta参数还可以这么用……或者说根本没注意到有这个参数好吧

def partial_p(p0, kbits, n):
    PR.<x> = PolynomialRing(Zmod(n))
    nbits = n.nbits()

    f = 2^kbits*x + p0
    f = f.monic()
    roots = f.small_roots(X=2^(nbits//2-kbits), beta=0.3)  # find root < 2^(nbits//2-kbits) with factor >= n^0.3
    if roots:
        x0 = roots[0]
        p = gcd(2^kbits*x0 + p0, n)
        return ZZ(p)

def find_p(d0, kbits, e, n):
    X = var('X')

    for k in xrange(1, e+1):
        results = solve_mod([e*d0*X - k*X*(n-X+1) + k*n == X], 2^kbits)
        for x in results:
            p0 = ZZ(x[0])
            p = partial_p(p0, kbits, n)
            if p:
                return p


if __name__ == '__main__':
    n = 123541066875660402939610015253549618669091153006444623444081648798612931426804474097249983622908131771026653322601466480170685973651622700515979315988600405563682920330486664845273165214922371767569956347920192959023447480720231820595590003596802409832935911909527048717061219934819426128006895966231433690709
    e = 97
    d = 0x7f4dbb449cc8aa9a0cb73c2fc7b1372da924d7b46c8a710c93e9281c010faaabfd8bec59ef47f5702648925cccc284099d138b33ad65a8a54db425a3c1f5b0b4f5cac22273b13cc617aed340d98ec1af4ed5206be011097c459726e72b7459192f35e1a8768567ea46883d30e7aaabc1fa2d8baa62cfcde93915a4a809bc3e9547bb07e1ecca16e51078312e89f0561e31b55db8b0ea5bc87a6ca7464a3d7c28a68c60e2ba88fe6a7d2b300d723e549910a987da89fc0a1c0de197a3d62c501b1f0e819891b1c32a0d6c233f2a285df87bb9e5c6c72d983ff3e706696bba639f573f9c3646968f02f3a615a438e20bb7c38d53621079f2899547a95350f3abeb

    beta = 0.5
    epsilon = beta^2/7

    nbits = n.nbits()
    #kbits = floor(nbits*(beta^2+epsilon))
    kbits = 300
    d0 = d & (2^kbits-1)
    d0 = 48553333005218622988737502487331247543207235050962932759743329631099614121360173210513133
    print "lower %d bits (of %d bits) is given" % (kbits, nbits)

    p = find_p(d0, kbits, e, n)
    print "found p: %d" % p
    q = n//p
    #print d
    print inverse_mod(e, (p-1)*(q-1))
