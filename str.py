
s = 'hasasedfdfds'
print(s)
p = s.find('s')
s = s[p+1:]
while p != -1 and s!='':
    print(p)
    print(s)
    x = input()
    if p+1<len(s):
        p = s.find('s')
        s = s[p+1:]