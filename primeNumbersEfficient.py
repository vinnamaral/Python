import math

def sumStrNum(strNum):

    try:

        numInt = int(strNum)

    except:

        try:

            numInt = int(float(strNum))

        except:

            return 0

    strNum2 = str(numInt)

    result = 0

    for i in strNum2:

        result += int(i)

    return result   
        
def isPrime(num):

    strNum = str(num)

    if num < 2:
        
        return False

    elif (num - int(num)) != 0:

        print "The number can't be decimal"

        return False

    elif int(num) in [2, 3, 5, 7]:

        return True

    elif strNum[-1] in ['0', '2', '4', '5', '6', '8']:

        return False

    elif num%3 == 0:

        return False

    elif num%7 == 0:

        return False

    elif sumStrNum(strNum)%3 == 0:

        return False

    else:

        tempNum1 = math.sqrt(num)

        tempNum2 = int(tempNum1)

        if (tempNum1 - tempNum2) == 0:

            return False

        else:

            limit = (int(tempNum1)+1)

            c = 8

            while c <= limit:

                if num%c == 0:

                    return False

                else:

                    c += 1

            return True


##c = 0
##l = []
###Whith the following while a have all the primes from 0 to 200
##while c <= 200:
##    if isPrime(c):
##        l.append(c)
##    c += 1
##
##c = 0
###Here I check to find where exists a interval of at least 13 composite numbers
##while c < len(l)-1:
##    if (l[c+1] - l[c]) >= 13:
##        print 'c: ', c
##	print 'l[c]: ', l[c]
##	print 'l[c+1]: ', l[c+1]
##	print 'dif: ', (l[c+1] - l[c])
##	print 'menor num de intervalo: ', l[c] + 1
##	print '----------------------------------------------'
##	break
##    
##    c += 1
