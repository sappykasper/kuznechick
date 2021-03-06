# Алгоритм "КУЗНЕЧИК" – поэтапная реализация двух раундов =)

from contextlib import redirect_stdout

alf = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя '
num = '0123456789'

S_block = [[252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77],[233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193],[249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79],[5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31],[235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204],[181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135],[21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177],[50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87],[223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3],[224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74],[167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65],[173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59],[7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137],[225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97],[32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82],[89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]]
k = (148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1)

dict_ = {}

def bin_(msg):
    result = ''
    i = 0
    while i<=len(msg)-1:
        if msg[i] == ' ':
            result += '00010000'
            i+=1
        elif msg[i] in num:
            binary = bin(int(msg[i]+msg[i+1]))
            binary = (('0'*(8-len(binary[2:])))+binary[2:])
            result += binary
            i+=2
        else:
            binary = bin(int(192 + alf.index(msg[i])))
            result += binary[2:]
            i+=1
    return result

def text_for_block(text):
    result = []
    i = 0
    while i <= 127:
        result += [text[i:i+8]]
        i += 8
    return result

def hex_(binary):
    i = 0
    result = []
    while i <= len(binary)-1:
        result += [hex(int(binary[i][:4], 2))[2:]+hex(int(binary[i][4:], 2))[2:]]
        i += 1
    return result

def three_in_one(text, binary, hexing):
    i = 0
    n = 0
    m = 0
    len_ = len(text)-1
    if text[i] in num:
        len_ = len(text[8:])-1
        while n <= 6:
            print(text[n]+text[n+1], '---', binary[m], '---', hexing[m])
            n+=2
            m+=1
        text = text[8:]
        binary = binary[4:]
        hexing = hexing[4:]
        
    while i <= len_:
        print(text[i], '---', binary[i], '---', hexing[i])
        i+=1


#---------------------------------------------------------

def X_transformation(mes,key):
    result = []
    i = 0
    while i<=len(mes)-1:
        result += ['0'*(2-len(str(hex(int('0x'+mes[i],0)^int('0x'+key[i],0)))[2:]))+str(hex(int('0x'+mes[i],0)^int('0x'+key[i],0)))[2:]]
        i += 1
    return result

def S_transformation(mes,alfavit):
    result = []
    res = []
    i = 0
    n = 0
    while i<=len(mes)-1:
        res += [alfavit[int('0x'+mes[i][0],0)][int('0x'+mes[i][1],0)]]
        i+=1

    print('Преобразование s: ',res)
    print('==='*20)
    
    while n<=len(mes)-1:
        result += [hex(int(res[n]))[2:]]
        n += 1
    return result

def R_transformation(mes,alfavit):
    mod = '0b111000011'

    result = []
    res = ''
    block_mod = []
    
    i = 0
    s_bin = []
    k_bin = []
    while i<=len(mes)-1:
        s_bin += [bin(int('0x'+mes[i],0))[2:]]
        k_bin += [bin(alfavit[i])[2:]]
        i += 1
        
    print('s_bin',s_bin)
    print('k_bin',k_bin)
    print('///'*20)
    
    n = 0
    while n<=len(mes)-1:
        m = 0
        r = 0
        l = 0
        block = ''
        block_l = ''
        block_multi = []
        block_xor = []

        print(s_bin[n],'*',k_bin[n])
        while m<=len(s_bin[n])-1:
            if s_bin[n]=='0':
                print(bin(int('0b'+k_bin[n],0)),'*',bin(int('0b1'+'0'*(len(s_bin[n])-m-1),0)),'=',bin(int('0b'+k_bin[n],0)*int('0b1'+'0'*(len(s_bin[n])-m-1),0)))
                block_multi += [bin(int('0x00',0))]
                m+=1
            elif s_bin[n][m]=='1':
                print(bin(int('0b'+k_bin[n],0)),'*',bin(int('0b1'+'0'*(len(s_bin[n])-m-1),0)),'=',bin(int('0b'+k_bin[n],0)*int('0b1'+'0'*(len(s_bin[n])-m-1),0)))
                block_multi += [bin(int('0b'+k_bin[n],0)*int('0b1'+'0'*(len(s_bin[n])-m-1),0))]
                m+=1
            else:
                m+=1
                
        print('---'*20)        
        print('block_multi',block_multi)
        print('---'*20)
        
        while r<=len(block_multi)-1:
            if len(block_multi) == 1:
                block_xor += [block_multi[r]]
                print('xor = ', block_multi[r])
                break
            elif r==0:
                print('xor: ',bin(int(block_multi[r],0)),'^',bin(int(block_multi[r+1],0)),'=',bin(int(block_multi[r],0)^int(block_multi[r+1],0)))
                block = bin(int(block_multi[r],0)^int(block_multi[r+1],0))
                r+=1
            elif r==len(block_multi)-1:
                print('xor = ',block)
                block_xor += [block]
                break
            else:
                print('xor: ',bin(int(block,0)),'^',bin(int(block_multi[r+1],0)),'=',bin(int(block,0)^int(block_multi[r+1],0)))
                block = bin(int(block,0)^int(block_multi[r+1],0))
                r+=1
                
        print('---'*20)        
        print('block_xor',block_xor)
        print('---'*20)
        
        block_l = block_xor[0]
        while l<=len(block_xor[0][2:])-1:
            #block_l = block_xor[0]
            #print('block_l',block_l)
            if len(block_l)<=10:
                print('modification = ',block_l[2:])
                block_mod += [block_l[2:]]
                break
            else:
                print('mod: ',bin(int(block_l,0)),'^',bin(int(mod+'0'*(len(block_l)-len(mod)),0)),'=',bin(int(block_l,0)^int(mod+'0'*(len(block_l)-len(mod)),0)))
                block_l = bin(int(block_l,0)^int(mod+'0'*(len(block_l)-len(mod)),0))
                l+=1
        #print(block_mod)
        n+=1
        
    print('---'*20)    
    print('block_mod',block_mod)

    print('==='*20)
    print('СЛОЖЕНИЕ (XOR) ВСЕХ ПОЛУЧЕННЫХ РЕЗУЛЬТАТОВ')
    print('==='*20)
    z = 0       
    while z<len(block_mod)-1:
        if z==0:
            print('res: ',bin(int('0b'+block_mod[z],0)),'^',bin(int('0b'+block_mod[z+1],0)),'=',bin(int('0b'+block_mod[z],0)^int('0b'+block_mod[z+1],0)))
            res = bin(int('0b'+block_mod[z],0)^int('0b'+block_mod[z+1],0))
            z+=1
        else:
            print('res: ',bin(int(res,0)),'^',bin(int('0b'+block_mod[z+1],0)),'=',bin(int(res,0)^int('0b'+block_mod[z+1],0)))
            res = bin(int(res,0)^int('0b'+block_mod[z+1],0))
            z+=1
    
    print('==='*20)

    result += [str('0'*(2-len(hex(int(res,0))[2:])))+str(hex(int(res,0))[2:])]
    result += mes[:-1]
    return result
     
#---------------------------------------------------------

def LSX(key):
    dict_['key']=key
    active_X=X_transformation(dict_['X'],dict_['key'])
    dict_['S']=active_X
    print('Преобразование X: ',active_X)
    print('==='*20)

    active_S=S_transformation(dict_['S'],S_block)
    dict_['R']=active_S
    print('Преобразование S: ',active_S)
    print('==='*20)

    i = 0
    while i<=15:
        active_R=R_transformation(dict_['R'],k)
        dict_['R']=active_R
        print('Преобразование R -',i,':',active_R)
        print('==='*20)
        i+=1
        
    dict_['X']=active_R


def two_rounds(key_list):
    i = 0
    while i<=len(key_list)-1:
        print('!!!'*20,i,'-й РАУНД','!!!'*20)
        key = key_list[i]
        LSX(key)
        i+=1
#---------------------------------------------------------
a = 'Информационная безопасность'
b = 'Костиков Виктор Александрович Костиков'

text = a[:16]
db_text = b[:32]

print('==='*20)

print('Сообщение: ', text)
print('Ключ: ', db_text)
print('==='*20)

print(text, len(text))
print(db_text, len(db_text))

text_bin=bin_(text)
db_1_text_bin=bin_(db_text[:16])
db_2_text_bin=bin_(db_text[16:])

print(text_bin)
print()
print(db_1_text_bin)
print(db_2_text_bin)

text_bin_block=text_for_block(text_bin)
db_1_text_bin_block=text_for_block(db_1_text_bin) # Ключ №1
db_2_text_bin_block=text_for_block(db_2_text_bin) # Ключ №2

print('Битовое сообщение: ', text_bin_block)
print('Битовой ключ №1: ', db_1_text_bin_block)
print('Битовой ключ №2: ', db_2_text_bin_block)
print('==='*20)

text_hex_block=hex_(text_bin_block)
db_1_text_hex_block=hex_(db_1_text_bin_block)
db_2_text_hex_block=hex_(db_2_text_bin_block)

print('16-ое сообщение: ', text_hex_block)
print('16-ый ключ №1: ', db_1_text_hex_block)
print('16-ый ключ №2: ', db_2_text_hex_block)

three_in_one(text, text_bin_block, text_hex_block)
print('==='*20)
three_in_one(db_text[:16], db_1_text_bin_block, db_1_text_hex_block)
print('==='*20)
three_in_one(db_text[16:], db_2_text_bin_block, db_2_text_hex_block)
print('==='*20)


dict_['X']=text_hex_block
key_list = [db_1_text_hex_block,db_2_text_hex_block]

two_rounds(key_list)

with open('file_name.txt', 'w') as f: 
    with redirect_stdout(f):
        a = 'Информационная безопасность'
        b = 'Костиков Виктор Александрович Костиков'
        text = a[:16]
        db_text = b[:32]
        print('==='*20)
        print('Сообщение: ', text)
        print('Ключ: ', db_text)
        print('==='*20)
        print(text, len(text))
        print(db_text, len(db_text))
        text_bin=bin_(text)
        db_1_text_bin=bin_(db_text[:16])
        db_2_text_bin=bin_(db_text[16:])
        print(text_bin)
        print()
        print(db_1_text_bin)
        print(db_2_text_bin)
        text_bin_block=text_for_block(text_bin)
        db_1_text_bin_block=text_for_block(db_1_text_bin) # Ключ №1
        db_2_text_bin_block=text_for_block(db_2_text_bin) # Ключ №2
        print('Битовое сообщение: ', text_bin_block)
        print('Битовой ключ №1: ', db_1_text_bin_block)
        print('Битовой ключ №2: ', db_2_text_bin_block)
        print('==='*20)
        text_hex_block=hex_(text_bin_block)
        db_1_text_hex_block=hex_(db_1_text_bin_block)
        db_2_text_hex_block=hex_(db_2_text_bin_block)
        print('16-ое сообщение: ', text_hex_block)
        print('16-ый ключ №1: ', db_1_text_hex_block)
        print('16-ый ключ №2: ', db_2_text_hex_block)
        three_in_one(text, text_bin_block, text_hex_block)
        print('==='*20)
        three_in_one(db_text[:16], db_1_text_bin_block, db_1_text_hex_block)
        print('==='*20)
        three_in_one(db_text[16:], db_2_text_bin_block, db_2_text_hex_block)
        print('==='*20)
        dict_['X']=text_hex_block
        key_list = [db_1_text_hex_block,db_2_text_hex_block]
        
        two_rounds(key_list)
