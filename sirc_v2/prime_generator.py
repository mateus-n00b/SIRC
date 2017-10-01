# Return the prime numbers between 2 and 'to'
#
# 
#
#
def prime_generator(prime, to):
    for i in xrange(2,to):
        count = 2
        for j in range(2,i):
            if (i%j) == 0 and i != 2:
                count+=1
                if count > 2:
                    prime.remove(i)
                    break
