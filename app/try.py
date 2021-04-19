from trycheck import *

f=open('MyCity.txt','r')
t=f.read()
no=Check_spelling(t)
print(no)
