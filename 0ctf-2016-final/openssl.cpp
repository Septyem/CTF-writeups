#include <openssl/evp.h>
#include <openssl/ec.h>
#include <openssl/ecdh.h>
#include <openssl/sha.h>

#include <stdio.h>
#include <time.h>

struct cipher {
	int recvfd;
	int sendfd;
	unsigned char sendkey[16];
	unsigned char recvkey[16];
	unsigned char sendiv[4];
	unsigned char recviv[4];
	long long sendcnt;
	long long recvcnt;
	long pos1;
	long pos2;
	unsigned char dedata[100];
};


void aes_gcm_encrypt(unsigned char *key, unsigned char *iv, unsigned char *cnt, int cntlen, unsigned char *in, int inlen, unsigned char* out, int *outlen, unsigned char *tag, int taglen) {
	EVP_CIPHER_CTX *x;
	int ol1;
	x=EVP_CIPHER_CTX_new();
	EVP_EncryptInit_ex(x, EVP_aes_128_gcm(), NULL, key, iv);
	EVP_EncryptUpdate(x, 0, outlen,  cnt, cntlen);
	EVP_EncryptUpdate(x, out, &ol1,  in, inlen);
	*outlen=ol1;
	EVP_EncryptFinal_ex(x, out+(*outlen), &ol1);
	*outlen+=ol1;
	EVP_CIPHER_CTX_ctrl(x,EVP_CTRL_GCM_GET_TAG, taglen, tag);
	EVP_CIPHER_CTX_cleanup(x);
}

void aes_gcm_decrypt(unsigned char *key, unsigned char *iv, unsigned char *cnt, int cntlen, unsigned char *in, int inlen, unsigned char *tag, int taglen, unsigned char* out, int *outlen) {
	EVP_CIPHER_CTX *x;
	int ol1;
	x=EVP_CIPHER_CTX_new();
	EVP_DecryptInit_ex(x, EVP_aes_128_gcm(), NULL, key, iv);
	EVP_DecryptUpdate(x, 0, outlen,  cnt, cntlen);
	EVP_DecryptUpdate(x, out, &ol1,  in, inlen);
	*outlen=ol1;
	EVP_DecryptFinal_ex(x, out+(*outlen), &ol1);
	*outlen+=ol1;
}

void encrypt(struct cipher c, unsigned char *d, int dlen, unsigned char *oiv) {
	unsigned char out[1000], tag[16];
	int outlen,i;

	unsigned char newiv[12];
	unsigned char cnt[10];
	*(long long*)cnt = c.recvcnt;
	cnt[8]=dlen%256;
	cnt[9]=dlen/256;
	for (i=0;i<4;i++)
		newiv[i]=c.recviv[i];
	for (i=0;i<8;i++)
		newiv[i+4]=oiv[i];
	aes_gcm_encrypt(c.recvkey, newiv, cnt, 10, d, dlen, out, &outlen, tag ,16);
	printf("%d ", outlen);
	for (i=0; i<outlen; i++)
		printf("%c", out[i]);
	for (i=0; i<16; i++)
		printf("%c", tag[i]);
	for (i=0;i<8;i++)
		printf("%c", oiv[i]);
}

void decrypt(struct cipher c, unsigned char *d, int dlen, unsigned char *oiv, unsigned char *tag) {
	unsigned char out[1000];
	int outlen,i;
	unsigned char newiv[12];
	unsigned char cnt[10];
	*(long long*)cnt = c.sendcnt;
	cnt[8]=dlen%256;
	cnt[9]=dlen/256;
	for (i=0;i<4;i++)
		newiv[i]=c.sendiv[i];
	for (i=0;i<8;i++)
		newiv[i+4]=oiv[i];
	aes_gcm_decrypt(c.sendkey, newiv, cnt, 10, d, dlen, tag, 16, out, &outlen);
	printf("%d ", outlen);
	for (i=0; i<outlen; i++)
		printf("%c", out[i]);
}

int main() {
	srand((unsigned)time(NULL));
	int i;
	EC_KEY* key;
	//key = EC_KEY_new_by_curve_name(415);
	key = EC_KEY_new_by_curve_name(NID_X9_62_prime256v1);
	const EC_GROUP *group = EC_KEY_get0_group(key);
	if (EC_KEY_generate_key(key)==0) {
		printf("Error generate key\n");
		return -1;
	}
	unsigned char pk_b[33];
	const EC_POINT *pub = EC_KEY_get0_public_key(key);
	if (EC_POINT_point2oct(group, pub, POINT_CONVERSION_COMPRESSED, pk_b, 33, 0)!=33) {
		printf("Error 2\n");
		return -1;
	}
	unsigned char h1[16],h2[16];

	printf("\x02");
	for (i=0;i<16;i++) {
		h1[i]=rand()%256;
		printf("%c",h1[i]);
	}
	for (i=0;i<33;i++)
		printf("%c",pk_b[i]);
	fflush(stdout);
	//get h2
	for (i=0;i<16;i++) 
		h2[i]=rand()%256;
	for (i=0;i<16;i++)
		scanf("%c",&h2[i]);
		
	//get peerpk_b
	unsigned char peerpk_b[33]={2 , 30 , 25 , 50 , 17 , 242 , 232 , 55 , 157 , 18 , 106 , 115 , 214 , 193 , 192 , 39 , 207 , 226 , 184 , 216 , 244 , 147 , 111 , 188 , 125 , 230 , 38 , 125 , 231 , 50 , 56 , 152 , 148 };
	for (i=0;i<33;i++)
		scanf("%c",&peerpk_b[i]);
	
	EC_POINT *peerpk = EC_POINT_new(group);
	if (EC_POINT_oct2point(group, peerpk, peerpk_b, 33, 0)==0) {
		printf("Error 3\n");
		return -1;
	}
	unsigned char skey[33];
	if (ECDH_compute_key(skey, 32,  peerpk, key, NULL)==0) {
		printf("Error 4\n");
		return -1;
	}


	SHA512_CTX shactx;	
	unsigned char hash[SHA512_DIGEST_LENGTH];
	SHA512_Init(&shactx);
	SHA512_Update(&shactx, h2, 16);
	SHA512_Update(&shactx, skey, 32);
	SHA512_Update(&shactx, h1, 16);
	SHA512_Final(hash, &shactx);

	for (i=0;i<64;i++)
		printf("%02x",hash[i]);	
	fflush(stdout);

	struct cipher c;
	c.recvfd=0;
	c.sendfd=1;
	for (i=0;i<16;i++)
		c.sendkey[i]=hash[i];
	for (i=0;i<4;i++)
		c.sendiv[i]=hash[32+i];
	for (i=0;i<16;i++)
		c.recvkey[i]=hash[16+i];
	for (i=0;i<4;i++)
		c.recviv[i]=hash[36+i];
	c.sendcnt=0;
	c.recvcnt=0;

	unsigned char d[1000];
	unsigned char oiv[8];
	int op;
	char dlen;

	while (true) {
		scanf("%d",&op);
		scanf("%c",&dlen);
		scanf("%c",&dlen);
		for (i=0;i<dlen;i++)
			scanf("%c",&d[i]);
		if (op==1) {
			for (i=0;i<8;i++)
				oiv[i]=rand()%256;
			encrypt(c,d,dlen,oiv);
			c.recvcnt+=1;
		} else if (op==2) {
			for (i=0;i<8;i++)
				scanf("%c",&oiv[i]);
			decrypt(c,d,dlen,oiv, NULL);
			c.sendcnt+=1;
		}
		fflush(stdout);
	}
	
	return 0;
}

