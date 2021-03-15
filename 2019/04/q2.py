def checkRules(n):
    ns = [int(d) for d in str(n)]
    r1 = []
    r2 = []
    r3 = []
    for i, n in enumerate(ns[1:]):
        r1.append( n >= ns[i] )
        r2.append( n == ns[i] )
        if n == ns[i]:             
            r3.append( ns.count(n) == 2 )
        else:
            r3.append( False )
    ch1 = all(r1)
    ch2 = any(r2)
    ch3 = any(r3)
        
    return(all([ch1,ch2,ch3]))

def main():
    
    count = 0
    
    for n in range(168630,718098):
        if checkRules(n) :
            count += 1
    print(count)


if __name__ == '__main__':
    main()