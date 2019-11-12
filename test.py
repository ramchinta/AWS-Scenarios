from datetime import datetime

print("Pranaty")

print("I work for Axelaar")
print("Linux Push")
print(datetime.now())


a = ['Lakshman','Chinta','Texas','California','Virginia']
b = ['Lakshman','Chinta1','Axelaar','Kissaan']
c=[]

fullmatch = [B for B in a if B.lower() in (x.lower() for x in b)]
for i in a:
    for j in b:
        if(i.lower() == j.lower()):
            c.append(i)
a = list(set(a)-set(c))
#a =list(a)

print(fullmatch)
print(a)

