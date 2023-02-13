import math
def Draper_Out_of_place(n,TD_Toffoli):
    Toffoli_D=4+math.floor(math.log2(n))+math.floor(math.log2(n/3))
    TD=Toffoli_D*TD_Toffoli
    #print("Draper_Out_of_place Toffoli-depth=", Toffoli_D)
    #print("Draper_Out_of_place T-depth=",TD)
    print(TD)

def Draper_Inplace(n,TD_Toffoli):
    Toffoli_D =math.floor(math.log2(n))+math.floor(math.log2(n-1))+math.floor(math.log2(n/3))+math.floor(math.log2((n-1)/3))+8
    TD = Toffoli_D * TD_Toffoli
    #print("Draper_Inplace Toffoli-depth=", Toffoli_D)
    #print("Draper_Inplace T-depth=", TD)
    print(TD)
def Takahashi_Inplace(n,TD_Toffoli):
    #Toffoli_D=30*((n-1).bit_length())#-O(loglogn)
    Toffoli_D = 30 *math.floor(math.log2(n))
    TD = Toffoli_D * TD_Toffoli
    #print("Takahashi_Inplace Toffoli-depth=", Toffoli_D)
    #print("Takahashi_Inplace T-depth=", TD)
    print(TD)
def Takahashi_Ripple_Carry(n,TD_Toffoli):
    Toffoli_D =2*n-1
    TD = Toffoli_D * TD_Toffoli
    #print("Takahashi_Ripple_Carry Toffoli-depth=", Toffoli_D)
    #print("Takahashi_Ripple_Carry T-depth=", TD)
    print(TD)

def Takahashi_CLA(n,TD_Toffoli):
    #Toffoli_D =9*((n-1).bit_length())
    Toffoli_D =9*math.floor(math.log2(n))
    TD = Toffoli_D * TD_Toffoli
    #print("Takahashi_CLA Toffoli-depth=", Toffoli_D)
    #print("Takahashi_CLA T-depth=", TD)
    print(TD)

def Thapliyal(n,TD_Toffoli):
    Toffoli_D =2+math.floor(math.log2(n))+math.floor(math.log2(n/3))
    TD = Toffoli_D * TD_Toffoli
    #print("Thapliyal Toffoli-depth=", Toffoli_D)
    #print("Thapliyal T-depth=", TD)
    print(TD)
'''Toffoli=Logic AND structure'''
def Out_QCL_1(n):
    term1=math.floor(math.log2(n))+math.floor(math.log2(n/3))
    TD =2*term1+14
    #print("Out_QCL_1 T-depth=", TD)
    print(TD)
def Out_QCL_2(n):
    term1 = math.floor(math.log2(n)) + math.floor(math.log2(n / 3))
    TD =3*term1+21
    #print("Out_QCL_2 T-depth=", TD)
    print(TD)
def In_QCL_1(n):
    term1 = math.floor(math.log2(n)) + math.floor(math.log2(n-1))
    term2=math.floor(math.log2(n/3))+math.floor(math.log2((n-1)/3))
    TD =2*(term1+term2)+28
    #print("In_QCL_1 T-depth=", TD)
    print(TD)
def In_QCL_2(n):
    term1 = math.floor(math.log2(n)) + math.floor(math.log2(n-1))
    term2=math.floor(math.log2(n/3))+math.floor(math.log2((n-1)/3))
    TD =3*(term1+term2)+42
    #print("In_QCL_2 T-depth=", TD)
    print(TD)

#可以选择是否有decomputation
def Higher_radix(n,TD_Toffoli,radix,decomputation=True,Logic_AND=False):
    radix=1.0*radix
    if Logic_AND==True:
        TD_BK=2
    else:
        TD_BK = TD_Toffoli

    if radix>=n:
        TD=n
        print("RCA=", TD)
    else:
        #STEP1: calculate p,g
        step1=TD_Toffoli
        if radix<=2:
            term1=0
        else:
            term1=1+math.floor(math.log2(radix-2)+1)


        # STEP2: Higher radix layer
        if radix==1:
            step2=0
        elif radix>=2:
            step2=(radix-1)*TD_Toffoli+TD_Toffoli+term1
        if n%radix==0:
            pairs = n / radix -1
        else:
            pairs = math.floor(n / radix)
        #print("pairs",pairs)
        term2=math.floor(math.log2(pairs)) + math.floor(math.log2(pairs/3))+2


        # STEP3 BK tree
        step3=TD_BK*(term2)


        # STEP4 Decomputation
        if term2<1:
            step4=0
        else:
            step4=TD_Toffoli*(term2-1)
        #如果不decomputation
        if decomputation==False:
            step4 = 0
        if TD_BK==2:
            step4=0

        # STEP5 Craig Gidney
        step5=radix

        #TD
        TD=step1+step2+step3+step4+step5
        print("step:",step1,step2,step3,step4,step5)
        print("Higher_radix T-depth=", TD)
        return TD



def T_depth(n,TD_Toffoli):
    #print("add_bit=",n)
    print(n)
    Takahashi_Ripple_Carry(n, TD_Toffoli)
    #print("")
    Draper_Out_of_place(n,TD_Toffoli)
    Draper_Inplace(n,TD_Toffoli)
    '''
    Takahashi_Inplace
    Takahashi_CLA
    '''
    Takahashi_Inplace(n,TD_Toffoli)
    Takahashi_CLA(n, TD_Toffoli)
    Thapliyal(n,TD_Toffoli)
    Out_QCL_1(n)
    Out_QCL_2(n)
    In_QCL_1(n)
    In_QCL_2(n)
    print("")

if __name__ == "__main__":
    n=int(10)
    '''
    TD_Toffoli=1
    T_depth(3, TD_Toffoli)
    T_depth(4, TD_Toffoli)
    T_depth(6, TD_Toffoli)
    T_depth(8, TD_Toffoli)
    T_depth(9, TD_Toffoli)
    T_depth(10,TD_Toffoli)
    T_depth(100, TD_Toffoli)
    T_depth(1000, TD_Toffoli)
    T_depth(10000, TD_Toffoli)


    TD_Toffoli=3
    print("TD_Toffoli=",TD_Toffoli)
    T_depth(3, TD_Toffoli)
    T_depth(4, TD_Toffoli)
    T_depth(6, TD_Toffoli)
    T_depth(8, TD_Toffoli)
    T_depth(9, TD_Toffoli)
    T_depth(10,TD_Toffoli)
    T_depth(100, TD_Toffoli)
    T_depth(1000, TD_Toffoli)
    T_depth(10000, TD_Toffoli)   
    '''
    TD_Toffoli = 3
    for i in range(1, 10):
        print("i=", i)
        Higher_radix(3, TD_Toffoli,radix=i)
        Higher_radix(4, TD_Toffoli,radix=i)
        Higher_radix(6, TD_Toffoli,radix=i)
        Higher_radix(8, TD_Toffoli,radix=i)
        Higher_radix(9, TD_Toffoli,radix=i)
        Higher_radix(10,TD_Toffoli,radix=i)
        Higher_radix(100, TD_Toffoli,radix=i)
        Higher_radix(1000, TD_Toffoli,radix=i)
        Higher_radix(10000, TD_Toffoli,radix=i)
    '''
    TD_9=[]
    TD_10=[]
    TD_100=[]
    TD_1000=[]
    TD_10000=[]
    TD_Toffoli=3
    for i in range(1, 9):
        print("i=", i)
        Higher_radix(9, TD_Toffoli,radix=i)
        TD_9.append(Higher_radix(9, TD_Toffoli,radix=i))
        Higher_radix(10,TD_Toffoli,radix=i)
        TD_10.append(Higher_radix(10, TD_Toffoli, radix=i))
    for i in range(1, 999):
        print("i=", i)
        Higher_radix(1000, TD_Toffoli,radix=i)
        TD_1000.append(Higher_radix(1000, TD_Toffoli, radix=i))
        Higher_radix(10000, TD_Toffoli,radix=i)
        TD_10000.append(Higher_radix(10000, TD_Toffoli, radix=i))

    print(min(TD_9),min(TD_1000),min(TD_10000))
    '''