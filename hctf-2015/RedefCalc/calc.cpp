#include<stdio.h>
#include<string>

long long nums[1000],ans[1000][1000],prob[1000][1000],C[1000][1000];

int main() {
	long long mod=1000000007,tmp,t2;
	long n,i,j,k;
	int ops[1000];
	scanf("%ld",&n);
	for (i=0;i<n;i++)
		scanf("%lld",&nums[i]);
	for (i=0;i<n-1;i++)
		scanf("%d",&ops[i]);
	for (i=0;i<=n;i++) {
		C[i][0]=1;
		for (j=1;j<=i;j++)
			C[i][j]=(C[i-1][j-1]+C[i-1][j])%mod;
	}
	for (i=0;i<n;i++) {
		ans[i][0]=nums[i];
		prob[i][0]=1;
	}
	for (i=1;i<n;i++) {
		for (j=0;j<n-i;j++) {
			for (k=0;k<i;k++) {
				t2=(prob[j][k]*prob[j+k+1][i-k-1])%mod;
				t2=(C[i-1][k]*t2)%mod;
				prob[j][i]=(prob[j][i]+t2)%mod;
				if (ops[j+k]==0)
					tmp=ans[j][k]*prob[j+k+1][i-k-1]+ans[j+k+1][i-k-1]*prob[j][k];
				else if (ops[j+k]==1)
					tmp=ans[j][k]*prob[j+k+1][i-k-1]-ans[j+k+1][i-k-1]*prob[j][k];
				else if (ops[j+k]==2)
					tmp=ans[j][k]*ans[j+k+1][i-k-1];
				tmp=tmp%mod;
				tmp=(tmp*C[i-1][k])%mod;
				ans[j][i]=(ans[j][i]+tmp)%mod;
			}
		}
	}
	long long res=ans[0][n-1];
	if (res<0)
		res+=mod;
	printf("%lld\n",res);
	return 0;
}
