#Version: 1.2
#Date: 02/Aug/2012

import cx_Oracle, sys, string

sessionID = sys.argv[1]
fileName = sys.argv[2]

conn = cx_Oracle.Connection("prod/prod@PCMS35")
cursor = conn.cursor()
#-------------------------------------------------------------------------------------------------------------
def retText(text, maxSpacesBetweenLetters = 25, maxSpacesBetweenDigits = 10):
    """This fucntion will return a list of strings where each component is part of the text
inputed surrounded by spaces. Some examples:
    
>>> retText('2 0        0495/AV.IBIRAPUERA-USP                          0             0986/VICOSA-MG                                              1\r\n')
['0495/AV.IBIRAPUERA-USP', '0986/VICOSA-MG']
>>> retText('                SAO PAULO     ,SP                                                                  VICOSA        ,MG                                           1\r\n')
['SAO PAULO     ,SP', 'VICOSA        ,MG']
>>> retText('                 SAO PAULO                      ,SP                                          VICOSA                         ,MG                                3\r\n')
['SAO PAULO                      ,SP', 'VICOSA                         ,MG']
>>> retText('                         *010050202*                                                                   *365700009*                                             4\r\n')
['*010050202*', '*365700009*']
    
The input variables are: text, maxSpacesBetweenLetter and maxSpacesBetweenDigits. The variable text
is the input text that the users which to split, maxSpacesBetweenLetters is the maximun number of
spaces between two letters to considere that a new sentence start. The last input is maxSpacesBetweenDigits
which is similar to the previous variable, with the diference that in this case what is considere
is the spaces between two numbers or a letter and a number, to considere that a new sentence start.
Something to considere, is that a sentence can't start with just one number surrounded by spaces, in
that case the number is not considere."""
    
    currentText = ''
    digitsCounter = 0
    spacesCounter = 0
    tempText = ''
    returnTextList = []
    for currentChar in text:
        if currentChar in string.letters:
            tempText += currentChar
            spacesCounter = 0
            if not currentText:
                tempText = tempText.lstrip()
            currentText += tempText
            tempText = ''
        elif currentChar in string.digits:
            digitsCounter += 1
            tempText += currentChar
            
            if digitsCounter == 1 and not currentText:
                tempText = tempText.lstrip() 
                
            if spacesCounter <= maxSpacesBetweenDigits:
                spacesCounter = 0
                if digitsCounter > 1 or currentText:
                    currentText += tempText
                    tempText = ''
            elif digitsCounter > 1:
                spacesCounter = 0
                currentText += tempText
                tempText = ''                
                
        elif currentChar == ' ':
            spacesCounter += 1
            digitsCounter = 0
            tempText += currentChar
            if not currentText:
                tempText = ''
            if spacesCounter > maxSpacesBetweenLetters:
                tempText = ''
                spacesCounter = 0
                if currentText:
                    returnTextList.append(currentText)
                    currentText = ''
        elif currentChar != '\r' and currentChar != '\n':
            tempText += currentChar
            if currentText or digitsCounter > 1:
                currentText += tempText
                tempText = ''
    
    if len(currentText) >= 2:
        if tempText and not tempText.strip().isdigit():
            currentText += tempText
        elif tempText.strip().isdigit() and len(tempText.strip()) > 1:
            currentText += tempText
        returnTextList.append(currentText)
        
    return returnTextList
#-------------------------------------------------------------------------------------------------------------
f_read = open(fileName, 'rb')
c = 0

address_age_left = ''
emissao_left = ''
consec_left = 0
bc_postNet_left = ''
address_client_left = ''
bc_code128_left = ''

address_age_right = ''
emissao_right = ''
consec_right = 0
bc_postNet_right = ''
address_client_right = ''
bc_code128_right = ''

header = f_read.readline()

def insertData(sID, agencia, emi, conse, postNet, client, code128):
    
    cursor.execute("""insert into chord.bra_rel_corr(session_id, address_age, emissao, 
                    consec, bc_postnet, address_client, bc_code128)
                    values(:session_id, :address_age, :emissao, 
                    :consec, :bc_postnet, :address_client, :bc_code128)""", session_id = sID,
                                                                          address_age = agencia,
                                                                          emissao = emi,
                                                                          consec = conse,
                                                                          bc_postnet = postNet,
                                                                          address_client = client,
                                                                          bc_code128 = code128)

for line in f_read:
    
    cleanData = retText(line.replace('\x00', ' ')) 
    
    if line[:2] == '2\x00' or line[:3] == '2 0' or line[:2] == '3\x00' or line[:3] == '3 0':    
        
        if emissao_left:
        
            insertData(sID = sessionID, agencia = address_age_left, emi = emissao_left, conse = consec_left, 
                       postNet = bc_postNet_left, client = address_client_left, code128 = bc_code128_left)
        
        if emissao_right:
            
            insertData(sID = sessionID, agencia = address_age_right, emi = emissao_right, conse = consec_right,
                       postNet = bc_postNet_right, client = address_client_right, code128 = bc_code128_right)            
        
        c = 0
        
        address_age_left = ''
        emissao_left = ''
        consec_left = 0
        bc_postNet_left = ''
        address_client_left = ''
        bc_code128_left = ''
        
        address_age_right = ''
        emissao_right = ''
        consec_right = 0
        bc_postNet_right = ''
        address_client_right = ''
        bc_code128_right = ''
        
        if cleanData:
            if len(cleanData) >= 1:
                address_age_left = cleanData[0].strip() + '\r\n'
            if len(cleanData) >= 2:
                address_age_right = cleanData[1].strip() + '\r\n'
        else:
            address_age_left = '\r\n'
            address_age_right = '\r\n'
    
    else:
        
        if cleanData:
            if c == 0:
                if len(cleanData) >= 1:
                    address_age_left += cleanData[0].strip() + '\r\n'
                if len(cleanData) >= 2:
                    address_age_right += cleanData[1].strip() + '\r\n'
            
            elif c == 1:
                if not emissao_left and len(cleanData) >= 1:
                    consec_left = int(cleanData[0][cleanData[0].find('ENVEL.')+6:].strip())
                if not emissao_right and len(cleanData) >= 2:
                    consec_right = int(cleanData[1][cleanData[1].find('ENVEL.')+6:].strip())
                
                if len(cleanData) >= 1:
                    emissao_left += cleanData[0].strip() + '\r\n'
                if len(cleanData) >= 2:
                    emissao_right += cleanData[1].strip() + '\r\n'
                
            elif c == 2:
                if len(cleanData) >= 1:
                    bc_postNet_left = cleanData[0].strip()[1:-1]
                if len(cleanData) >= 2:
                    bc_postNet_right = cleanData[1].strip()[1:-1]
            
            elif c == 3:
                if len(cleanData) >= 1:
                    address_client_left += cleanData[0].strip() + '\r\n'
                if len(cleanData) >= 2:
                    address_client_right += cleanData[1].strip() + '\r\n'
            
            elif c == 5:
                if len(cleanData) >= 1:
                    bc_code128_left = cleanData[0].strip()
                if len(cleanData) >= 2:
                    bc_code128_right = cleanData[1].strip()
        
        else:
            c += 1

if emissao_left:
        
    insertData(sID = sessionID, agencia = address_age_left, emi = emissao_left, conse = consec_left,
               postNet = bc_postNet_left, client = address_client_left, code128 = bc_code128_left)

if emissao_right:

    insertData(sID = sessionID, agencia = address_age_right, emi = emissao_right, conse = consec_right,
               postNet = bc_postNet_right, client = address_client_right, code128 = bc_code128_right)

conn.commit()

f_read.close()
cursor.close()
conn.close()