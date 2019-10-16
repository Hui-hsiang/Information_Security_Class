import numpy as np
import sys

key = str(bin(int(sys.argv[1][2:],16)))[2:].zfill(64)
key = np.asarray(list(map(int,key)))
#print (key,key.shape)
ciphertext = str(bin(int(sys.argv[2][2:],16)))[2:].zfill(64)
ciphertext = np.asarray(list(map(int,ciphertext)))
#print(ciphertext,ciphertext.shape)

IP = np.array([58, 50, 42, 34, 26, 18, 10, 2,
               60, 52, 44, 36, 28, 20, 12, 4,
               62, 54, 46, 38, 30, 22, 14, 6,
               64, 56, 48, 40, 32, 24, 16, 8,
               57, 49, 41, 33, 25, 17, 9,  1,
               59, 51, 43, 35, 27, 19, 11, 3,
               61, 53, 45, 37, 29, 21, 13, 5,
               63, 55, 47, 39, 31, 23, 15, 7])

F_P = np.array([40,	8,	48,	16,	56,	24,	64,	32,
               39,	7,	47,	15,	55,	23,	63,	31,
               38,	6,	46,	14,	54,	22,	62,	30,
               37,	5,	45,	13,	53,	21,	61,	29,
               36,	4,	44,	12,	52,	20,	60,	28,
               35,	3,	43,	11,	51,	19,	59,	27,
               34,	2,	42,	10,	50,	18,	58,	26,
               33,	1,	41,	9,	49,	17,	57,	25])
#print (IP,IP.dtype)
#print (FP,FP.dtype)

pm_input = list()

for i in IP:
    pm_input.append(ciphertext[i - 1])

pm_input = np.asarray(pm_input)
#print (pm_input,pm_input.shape,pm_input.dtype)

li = pm_input[:32]
ri = pm_input[32:]

#print (li.shape,ri.shape)

PCone_l = np.array([57, 49, 41, 33, 25, 17, 9,
                  1,  58, 50, 42, 34, 26, 18,
                  10, 2,  59, 51, 43, 35, 27,
                  19, 11, 3,  60, 52, 44, 36])

PCone_r = np.array([63, 55, 47, 39, 31, 23, 15,
                  7,  62, 54, 46, 38, 30, 22,
                  14, 6,  61, 53, 45, 37, 29,
                  21, 13, 5,  28, 20, 12, 4])

Ci = list()
Di = list()

for i in range(28):
    Ci.append(key[PCone_l[i]])
    Di.append(key[PCone_r[i]])

Ci = np.asarray(Ci)
Di = np.asarray(Di)
#print(Ci.shape,Di.shape)

PCtwo = np.array([14, 17, 11, 24, 1,  5,
                  3,  28, 15, 6,  21, 10,
                  23, 19, 12, 4,  26, 8,
                  16, 7,  27, 20, 13, 2,
                  41, 52, 31, 37, 47, 55,
                  30, 40, 51, 45, 33, 48,
                  44, 49, 39, 56, 34, 53,
                  46, 42, 50, 36, 29, 32])

key_s = np.array(np.zeros((16,48),dtype=int))

for i in range(0,16):
    if i in [0,1,8,15]:
        tmpc = Ci[0]
        tmpd = Di[0]
        Ci = np.append(Ci[1:],tmpc)
        Di = np.append(Di[1:],tmpd)
    else:
        tmpc = Ci[:2]
        tmpd = Di[:2]
        Ci = np.append(Ci[2:],tmpc)
        Di = np.append(Di[2:],tmpd)
    ki = np.append(Ci,Di)
    tmpk = list()
    for j in PCtwo:
        tmpk.append(ki[j-1])
    ki = np.asarray(tmpk)
    key_s[i] = ki
#print (key_s)


E = np.array([32, 1,  2,  3,  4,  5,
              4,  5,  6,  7,  8,  9,
              8,  9,  10, 11, 12, 13,
              12, 13, 14, 15, 16, 17,
              16, 17, 18, 19, 20, 21,
              20, 21, 22, 23, 24, 25,
              24, 25, 26, 27, 28, 29,
              28, 29, 30, 31, 32, 1])

sbox = [
    # S1
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    # S2
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3,  13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0,  14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    # S3
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1 , 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    # S4
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3,  15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    # S5
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14,11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    # S6
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9 , 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4 , 3,  2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    # S7
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4,  11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    # S8
    [13, 2,  8,  4,  6,  15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4,  1,  9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1,  14, 7,  4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
  ]




tmp = list()
for i in range(15,0,-1):
    for j in E:
        tmp.append(ri[j-1])

    rn = np.asarray(tmp)
    rn = np.bitwise_xor(key_s[i],rn)
    #print (rn)
    b = [
        rn[0:6],rn[6:12],rn[12:18],rn[18:24],rn[24:30],rn[30:36],rn[36:42],rn[42:48]
    ]

    col = b[0][0]*2+b[0][5]
    row = b[0][1]*2*2*2 + b[0][2]*2*2 + b[0][3]*2 + b[0][4] 
    value = sbox[0][col*16 + row]
    value = str(bin(value))[2:].zfill(4)
    B = np.asarray(list(map(int,value)))
    for j in range(1,8):
        col = b[j][0]*2+b[j][5]
        row = b[j][1]*2*2*2 + b[j][2]*2*2 + b[j][3]*2 + b[j][4] 
        value = sbox[0][col*16 + row]
        value = str(bin(value))[2:].zfill(4)
        B = np.append(B,np.asarray(list(map(int,value))))

    FP = [
        16, 7,  20, 21, 29, 12, 28, 17,
        1,  15, 23, 26, 5,  18, 31, 10,
        2,  8,  24, 14, 32, 27, 3,  9,
        19, 13, 30, 6,  22, 11, 4,  25
    ]
    #print(B)
    rn = np.array(np.zeros(shape = (32),dtype=int))
    for x,j in enumerate(FP):
        rn[x] = B[j-1]


    rn = np.bitwise_xor(li,rn)
    li = ri
    ri = rn
    tmp = []
    #print (np.append(li,ri))


pre_final_output = np.append(li,ri)
final_output = list()
for i in F_P:
    final_output.append(pre_final_output[i-1])

final_output = "".join(np.asarray(final_output).astype(str))
final_output = hex(int(final_output,2))

print (final_output)