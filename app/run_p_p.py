f=open('MyCity.txt','r')
t=f.read()
from para_phrase import *
x=para_phrasing(t,'Computer a boon or bale')
print(x)
