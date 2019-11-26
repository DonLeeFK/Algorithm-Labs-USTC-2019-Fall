def __hash(Str):
    hash_value=0
    for i in range(len(Str)):
        hash_value+=ord(Str[i])*(128**(len(Str)-i-1))
    return hash_value

def RabinKarp(T,Patten):
    hash_p=__hash(Patten)
    hash_t=__hash(T[:len(Patten)])
    for i in range(len(T)-len(Patten)):
        if hash_p==hash_t:
            return True,i,i+len(Patten)
        else:
            hash_t-=ord(T[i])*128**(len(Patten)-1)
            hash_t*=128
            hash_t+=ord(T[i+len(Patten)])
    if hash_p==hash_t: return True,len(T)-len(Patten), len(T)
    if hash_p!=hash_t: return False
    
s1=input('T: ')
s2=input('P: ')
print(RabinKarp(s1,s2))
