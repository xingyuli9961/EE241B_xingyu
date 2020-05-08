# this file contains the .out file reader and instructions decoder

def dump_instructions(filename):
    fi = read_file(filename)[:-1]
    a = 0
    while (int(fi[a][4:12], 16) == 0):
        a += 1
    insn = ['00000013']
    pc = int(fi[a][4:12], 16)
    prev = fi[a][21:29]
    for i in range(a, len(fi)):
        curr_pc = int(fi[i][4:12], 16)
        curr_ins = fi[i][21:29]
        if (curr_pc != pc):
            pc = curr_pc
            prev = curr_ins
            insn.append(curr_ins)
        else:
            if (prev == '00000013'):
                insn.append(curr_ins)
                prev = curr_ins
    return insn


# NOP = 0;
# Rtype = 1;
# Itype-ALU = 2;
# Itype-Load = 3;
# Itype-Jalr = 4;
# Stype = 5;
# SBtype = 6;
# Utype = 7;
# UJtype = 8;
# Other(fence) = 9;


def decode_simple(array):
    insn_decoded = []
    for i in range(len(array)):
        tmp = array[i][6:8]
        if (array[i] == '00000013'):
            insn_decoded.append(0)
        elif (tmp=="33" or tmp=="b3"):
            insn_decoded.append(1)
        elif (tmp=="13" or tmp=="93"):
            insn_decoded.append(2)
        elif (tmp=="03" or tmp=="83"):
            insn_decoded.append(3)
        elif (tmp=="67" or tmp=="e7"):
            insn_decoded.append(4)
        elif (tmp=="23" or tmp=="a3"):
            insn_decoded.append(5)
        elif (tmp=="63" or tmp=="e3"):
            insn_decoded.append(6)
        elif (tmp=="37" or tmp=="b7" or tmp=="17" or tmp=="97"):
            insn_decoded.append(7)
        elif (tmp=="6f" or tmp=="ef"):
            insn_decoded.append(8)
        else:
            insn_decoded.append(9)
    return insn_decoded




def decode_detailed(array):
    insn_decoded = []
    for i in range(len(array)):
        element  = array[i]
        tmp = element[6:8]
        f3 = element[4]
        f7 = element[:2]
        
         # NOP
        if (array[i] == '00000013'):
            # NOP = 0;
            insn_decoded.append(0)
        
        # Rtype  
        elif (tmp=="33" or tmp=="b3"):
            if (f3 == "0" or f3 =="8"):
                if (f7 == "00" or f7 == "01"):
                    # ADD = 10
                    insn_decoded.append(10)
                else:
                    # SUB = 11
                    insn_decoded.append(11)
            elif (f3 == "1" or f3 =="9"):
                # SLL = 12
                insn_decoded.append(12)
            elif (f3 == "2" or f3 =="a"):
                # SLT = 13
                insn_decoded.append(13)
            elif (f3 == "3" or f3 =="b"):
                # SLTU = 14
                insn_decoded.append(14)
            elif (f3 == "4" or f3 =="c"):
                # XOR = 15
                insn_decoded.append(15)
            elif (f3 == "5" or f3 =="d"):
                if (f7 == "00" or f7 == "01"):
                    # SRL = 16
                    insn_decoded.append(16)  
                else:
                    # SRA = 17
                    insn_decoded.append(17)
            elif (f3 == "6" or f3 =="e"):
                # OR = 18
                insn_decoded.append(18)
            elif (f3 == "7" or f3 =="f"):
                # AND = 19
                insn_decoded.append(19)
            else:
                insn_decoded.append(0)
        
        # Itype-ALU
        elif (tmp=="13" or tmp=="93"):
            if (f3 == "0" or f3 =="8"):
                # ADDI = 20
                insn_decoded.append(20)
            elif (f3 == "1" or f3 =="9"):
                # SLLI = 21
                insn_decoded.append(21)
            elif (f3 == "2" or f3 =="a"):
                # SLTI = 22
                insn_decoded.append(22)
            elif (f3 == "3" or f3 =="b"):
                # SLTIU = 23
                insn_decoded.append(23)
            elif (f3 == "4" or f3 =="c"):
                # XORI = 24
                insn_decoded.append(24) 
            elif (f3 == "5" or f3 =="d"):
                if (f7 == "00" or f7 == "01"):
                    # SRLI = 25
                    insn_decoded.append(25)  
                else:
                    # SRAI = 26
                    insn_decoded.append(26)
            elif (f3 == "6" or f3 =="e"):
                # ORI = 27
                insn_decoded.append(27)
            elif (f3 == "7" or f3 =="f"):
                # ANDI = 28
                insn_decoded.append(28)
            else:
                insn_decoded.append(29)
        
        # Itype-Load     
        elif (tmp=="03" or tmp=="83"):
            if (f3 == "0" or f3 =="8"):
                # LB = 30
                insn_decoded.append(30)
            elif (f3 == "1" or f3 =="9"):
                # LH = 31
                insn_decoded.append(31)
            elif (f3 == "2" or f3 =="a"):
                # LW = 32
                insn_decoded.append(32)
            elif (f3 == "4" or f3 =="c"):
                # LBU = 33
                insn_decoded.append(33)
            elif (f3 == "5" or f3 =="d"):
                # LHU = 34
                insn_decoded.append(34)
            else:
                insn_decoded.append(39)
            
        # Itype-Jalr
        elif (tmp=="67" or tmp=="e7"):
            insn_decoded.append(40)
            
        # Stype  
        elif (tmp=="23" or tmp=="a3"):
            if (f3 == "0" or f3 =="8"):
                # SB = 50
                insn_decoded.append(50)
            elif (f3 == "1" or f3 =="9"):
                # SH = 51
                insn_decoded.append(51)
            elif (f3 == "2" or f3 =="a"):
                # SW = 52
                insn_decoded.append(52)
            elif (f3 == "4" or f3 =="c"):
                # SBU = 53
                insn_decoded.append(53)
            elif (f3 == "5" or f3 =="d"):
                # SHU = 54
                insn_decoded.append(54)
            else:
                insn_decoded.append(59)
            
        # SBtype   
        elif (tmp=="63" or tmp=="e3"):
            if (f3 == "0" or f3 =="8"):
                # BEQ = 60
                insn_decoded.append(60)
            elif (f3 == "1" or f3 =="9"):
                # BNE = 61
                insn_decoded.append(61)
            elif (f3 == "4" or f3 =="c"):
                # BLT = 62
                insn_decoded.append(62)
            elif (f3 == "5" or f3 =="d"):
                # BGE = 63
                insn_decoded.append(63)
            elif (f3 == "6" or f3 =="e"):
                # BLTU = 64
                insn_decoded.append(64)
            elif (f3 == "7" or f3 =="f"):
                # BLTU = 65
                insn_decoded.append(65)
            else:
                insn_decoded.append(69)
        
        # Utype = 7;
        elif (tmp=="37" or tmp=="b7" or tmp=="17" or tmp=="97"):
            if (tmp=="37" or tmp=="b7"):
                # LUI = 70
                insn_decoded.append(70)
            else:
                # AUIPC = 71
                insn_decoded.append(71)
        
        # UJtype
        elif (tmp=="6f" or tmp=="ef"):
            # UJtype = 80;
            insn_decoded.append(80)
            
        # Other(fence)
        else:
            # Other(fence) = 9;
            insn_decoded.append(90)
    return insn_decoded
