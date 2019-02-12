##Version 1.7
##Date: 25/Jun/2012

import cx_Oracle, os, shutil, time, gnupg, glob
##---------------------------------------------------------------------------------------------------------------
myGpg = gnupg.GPG(gpgbinary = '\\\\10.101.94.10\\Workestra\\Bin\\GPG\\gpg.exe',
                  gnupghome = '\\\\10.101.94.10\\Workestra\\Bin\\GPG\\GPGHome')

def myDecrypt(input_file, output_file, passwd = ''):
    
    f1 = open(input_file, 'rb')
    cond = myGpg.decrypt_file(f1, passphrase = passwd,
                              output = output_file)
    f1.close()
    print cond.status
    return cond
##---------------------------------------------------------------------------------------------------------------
def id_name(temp):
    res = ''
    for i in temp:
        res += hex(i[0])[2:].upper() + '_'
    return res[:len(res)-1]

def str2(num):
    temp = str(num)
    return '0' * (2-len(temp)) + temp

def str6(num):
    temp = str(num)
    return '0' * (6-len(temp)) + temp
##---------------------------------------------------------------
conn = cx_Oracle.Connection("u_stationary/r1ncew1nd@PCMSBANK")
cursor = conn.cursor()

mainPath = '\\\\10.101.94.10\\cddata\\Transfer\\In\\ITAU\\Relatorios_PJ\\Split_Debito\\'
inPath = mainPath + 'Input\\'
if not os.path.lexists(inPath):
    os.makedirs(inPath)
if not os.path.lexists(mainPath + 'Erro\\'):
    os.makedirs(mainPath + 'Erro\\')

graph = '\\\\10.101.94.10\\Grafica\\Relat_Itau\\out\\'

procPath = inPath + 'Enviado\\'

dateStr = str(time.localtime().tm_year) + str2(time.localtime().tm_mon) + str2(time.localtime().tm_mday) +\
    '_' + str2(time.localtime().tm_hour) + str2(time.localtime().tm_min) + str2(time.localtime().tm_sec)

procPath += dateStr + '\\'

os.makedirs(procPath)
    
filesRaw = os.listdir(inPath)
files = []

for i in filesRaw:
    if os.path.isfile(inPath + i):
        status_dec = myDecrypt(inPath + i, inPath + i + '_dec', passwd = '!schnaps4')
        if os.path.lexists(inPath + i + '_dec'):
            os.remove(inPath + i)
            files.append(i + '_dec')
        else:
            shutil.move(inPath + i, mainPath + 'Erro\\' + i)

for i in files:

    f1 = open(inPath + i, 'rb')
    header = ''
    infoCartoes = ''
    newId = ''
    f2 = open(procPath + 'temp.txt', 'ab')
    cHeader = 0
    cCartoes = 0
    condTotal = True

    for j in f1:

        j = j[2 : j.rfind(' ')]

        temp = j.split(' ')
        temp2 = []
        for k in temp:
            if k:
                temp2.append(k)

        if temp2:

            try:
                int(temp2[0])
                
                cCartoes += 1

                if (i[:4] == 'TCTG' and i[15:] == '.04'):
                    cartao = temp2[2]
                else:
                    c2 = 0
                    for l in temp2:
                        c2 += 1
                        if '/' in l:
                            try:
                                int(l[:2])
                                int(l[3:])
                                break
                            except:
                                pass
                    cartao = temp2[c2]
                
                cursor.execute("""select wo.workorderiddisplay, ca.indexnumber from prod.card ca
                                  inner join prod.workorder wo
                                  on wo.workorderid = ca.workorderid
                                  where ca.primarykeyvalue = :arg1
                                  and wo.workorderid = wo.workorderiddisplay""",
                               arg1 = cartao)
                idOrder = cursor.fetchall()

                oldId = newId
                
                if idOrder:
                    newId = id_name(idOrder)
                else:

                    cursor.execute("""select wo.workorderiddisplay, ca.indexnumber from prod.card ca
                                      inner join prod.workorder wo
                                      on wo.workorderid = ca.workorderid
                                      where ca.primarykeyvalue = :arg1
                                      and wo.workorderid = wo.workorderiddisplay""",
                                   arg1 = cartao + 'FFFFFFFFFF')
                    idOrder = cursor.fetchall()

                    if idOrder:
                        newId = id_name(idOrder)
                    else:
                        newId = 'no_id'
                        
                if newId != oldId:

                    if condTotal:
                        f2.write('\r\n                                             TOTAL DE CARTOES  =      ' + str(cCartoes) + '\r\n')

                    cCartoes = 1
                    condTotal = True
                    f2.close()
                    f2 = open(procPath + newId + '.txt', 'ab')
                    f2.write(header)

                    cHeader = 1

                if not cHeader:
                    f2.write(header)

                num = str6(idOrder[0][1])
                new_cartao = cartao[:4] + 'XXXXXXXX' + cartao[12:]
                j = j[:j.find(temp2[0])] + num + j[j.find(temp2[0])+6:j.find(cartao)] + new_cartao + j[j.find(cartao)+16:]

                cHeader += 1

                f2.write(j + '\r\n')
                
            except:

                if temp2[0].lower() == 'total':
                    f2.write('\r\n                                             TOTAL DE CARTOES  =      ' + str(cCartoes) + '\r\n')
                    cCartoes = 0
                    header = ''
                    cHeader = 0
                    condTotal = False
                else:
                    if header:
                        header += j + '\r\n'
                    else:
                        header += '\r\n\r\n' +j + '\r\n'

    f1.close()
    f2.close()
    try:
        os.remove(procPath + 'temp.txt')
    except:
        pass

file_names = glob.glob(procPath + '*')

for i in file_names:

    if os.path.isfile(i) and i[i.rfind('\\') + 1 : ] != 'no_id.txt':

        f_write = open(i + '_new', 'wb')
        idNumber = i[i.rfind('\\') + 1: i.rfind('.txt')]
        cursor.execute("""select max(ca.indexnumber) from card ca
                          inner join workorder wo
                          on wo.workorderid = ca.workorderid
                          where  wo.workorderid = to_number(:arg, 'XXXXXX')""", arg = idNumber[:5])
        maxSeq = cursor.fetchall()
        if maxSeq:
            maxSeq = maxSeq[0][0]
            print maxSeq
        else:
            maxSeq = 0
            print 'O id: ' + idNumber + ', nao esta no banco de dados.'
            
        counterSeq = 0

        while counterSeq < maxSeq:

            print counterSeq

            f_read = open(i, 'rb')
            header = ''
        
            for j in f_read:

                temp = j.split(' ')
                temp2 = []
                for k in temp:
                    if k and k != '\r\n':
                        temp2.append(k)

                if temp2:

                    try:
                        newSeq = int(temp2[0])
                        if newSeq == (counterSeq + 1):
                            if header:
                                f_write.write(header)
                                header = ''
                            f_write.write(j)
                            counterSeq += 1
                        else:
                            header = ''

                    except:

                        if temp2[0].lower() == 'total':
                            if (newSeq + 1) == counterSeq:
                                f_write.write('\r\n' + j)
                            
                        else:
                            if header:
                                header += j
                            else:
                                header += '\r\n\r\n' + j

            f_read.close()

        f_write.close()

        os.remove(i)
        os.rename(i + '_new', i)
    
cursor.close()
conn.close()

for i in files:

    try:
        os.remove(inPath + i)
    except:
        pass

try:
    os.stat(graph + dateStr)
    files2move = os.listdir(procPath)
    for i in files2move:

        if i != 'no_id.txt':
            try:
                os.stat(graph + dateStr + '\\' + i)
                os.remove(graph + dateStr + '\\' + i)
                shutil.copyfile(procPath + i, graph + dateStr + '\\' + i)
            except:
                shutil.copyfile(procPath + i, graph + dateStr + '\\' + i)
except:
    shutil.copytree(procPath, graph + dateStr)
    try:
        os.stat(graph + dateStr + '\\no_id.txt')
        os.remove(graph + dateStr + '\\no_id.txt')
    except:
        pass
