def ruleDoubleDigits(n):
    return len(set(str(n))) < len(str(n))
    
def ruleIncreasing(n):
    ns = [int(d) for d in str(n)]
    ch = []
    for i, n in enumerate(ns[1:]):
        ch.append( n >= ns[i] )
    return(all(ch))

def main():
    count = 0
    for n in range(168630,718098):
        if all( [ruleDoubleDigits(n), ruleIncreasing(n)] ) :
            count += 1
    print(count)


if __name__ == '__main__':
    main()