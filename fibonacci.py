def fibSimple(n):
    if n <= 2 and n > 0:
        return 1
    elif n == 0:
        return 0
    else:
        return fibSimple(n-1) + fibSimple(n-2)

def fibAdvance(n):
    c = 2
    fibs = [0, 1, 1]
    return fibHelper(n, c, fibs)

def fibHelper(n, c, fibs):
    
    if n < 0:
        print 'No existe un numero de Fibonacci para numeros negativos'
        return 
    elif n <= 2:
        return fibs[n]
    else:
        if c + 1 == n:
            return fibs[c] + fibs[c-1]
        else:
            fibs.append(fibs[c] + fibs[c-1])
            return fibHelper(n, c+1, fibs)
