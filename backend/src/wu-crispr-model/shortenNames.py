f = open('names','r')
names = f.readlines()
names = [n.strip() for n in names]
names = [n.replace("count","cnt") for n in names]
names = [n.replace("folding","fld") for n in names]
names = [n.replace("binding","bind") for n in names]
names = [n.replace("pyrimidine","pyr") for n in names]
print(names)
f.close()

ff = open('newnames','w')
for n in names:
    ff.write(n+'\n')
ff.close()
