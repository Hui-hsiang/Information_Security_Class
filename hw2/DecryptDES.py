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

FP = np.array([40,	8,	48,	16,	56,	24,	64,	32,
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

key_s = np.array(np.empty((16,48)))

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
    



        





