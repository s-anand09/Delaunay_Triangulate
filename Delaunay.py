from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
import math
import csv

T_C=[[0,0,0],[250,0,0],[0,0,250]]
A=[(T_C[1][0]-T_C[0][0]),(T_C[1][1]-T_C[0][1]),(T_C[1][2]-T_C[0][2])]
B=[(T_C[2][0]-T_C[1][0]),(T_C[2][1]-T_C[1][1]),(T_C[2][2]-T_C[1][2])]
CrossAB=[((A[1]*B[2])-(A[2]*B[1])),((A[2]*B[0])-(A[0]*B[2])),((A[0]*B[1])-(A[1]*B[0]))]
D=((T_C[0][0]*CrossAB[0])+(T_C[0][1]*CrossAB[1])+(T_C[0][2]*CrossAB[2]))
X=((T_C[1][0]*CrossAB[0])+(T_C[1][1]*CrossAB[1])+(T_C[1][2]*CrossAB[2]))
#Putting Coordinates:
#A1B1=[((T_C[0][1]*T_C[1][2])-(T_C[1][1]*T_C[0][2])),((T_C[0][2]*T_C[1][0])-(T_C[0][0]*T_C[1][2])),((T_C[0][0]*T_C[1][1])-(T_C[0][1]*T_C[1][0]))]
#A1C1=[((T_C[0][1]*T_C[2][2])-(T_C[2][1]*T_C[0][2])),((T_C[0][2]*T_C[2][0])-(T_C[0][0]*T_C[2][2])),((T_C[0][0]*T_C[2][1])-(T_C[0][1]*T_C[2][0]))]
#def 
#def CP(Tcd,Pp):

def crossProdSign(P1,P2,P3):
    V1=[0]*3
    V2=[0]*3
    i=0
    for each in P2:
        V1[i]=P2[i]-P1[i]
        V2[i]=P3[i]-P1[i]
        i+=1
    Sig1=(V1[1]*V2[2])-(V2[1]*V1[2])
    if Sig1!=0:
        Sig1=Sig1/abs(Sig1)
    Sig2=(V1[2]*V2[0])-(V2[2]*V1[0])
    if Sig2!=0:
        Sig2=Sig2/abs(Sig2)
    Sig3=(V1[0]*V2[1])-(V2[0]*V1[1])
    if Sig3!=0:
        Sig3=Sig3/abs(Sig3)
    Sig=[Sig1,Sig2,Sig3]
    return Sig

def checkInternal(A,B,C,P):
    C1=crossProdSign(A,B,P)
    C2=crossProdSign(B,C,P)
    C3=crossProdSign(C,A,P)
    if C1==C2 and C2==C3:
        Res=True
    else:
        Res=False
    return Res    
    
def Area3D (X1,Y1,Z1,X2,Y2,Z2,X3,Y3,Z3):
    VEC1=[(X2-X1),(Y2-Y1),(Z2-Z1)]
    VEC2=[(X3-X1),(Y3-Y1),(Z3-Z1)]
    DotP=(VEC1[0]*VEC2[0])+(VEC1[1]*VEC2[1])+(VEC1[2]*VEC2[2])
    Mag1=((VEC1[0]**2)+(VEC1[1]**2)+(VEC1[2]**2))**0.5
    Mag2=((VEC2[0]**2)+(VEC2[1]**2)+(VEC2[2]**2))**0.5
    ANG=math.acos(DotP/(Mag1*Mag2))
    AR=0.5*Mag1*Mag2*math.sin(ANG)
    return AR

Area=Area3D(T_C[0][0],T_C[0][1],T_C[0][2],T_C[1][0],T_C[1][1],T_C[1][2],T_C[2][0],T_C[2][1],T_C[2][2])
print(A,B,CrossAB,D,Area)
print(X==D)
L_P=[]
n=input("Enter number of points : ")
mind=input("Enter the minimum mesh length : ")
i=0
while i<int(n):
    while True:
        #X1=random.randrange(5,92,0.05)
        #Z1=random.randrange(-3,104,0.05)
        switch=0
#        X1=random.uniform(5,250)
#        Z1=random.uniform(-3,103)
#        Y1=(D-(CrossAB[0]*X1)-(CrossAB[2]*Z1))/CrossAB[1]
        X1=random.uniform(0,250)
        Z1=random.uniform(0,250)
        Y1=0
        Point=[X1,Y1,Z1]
        try:
            if L_P != []:
                for each in L_P:
                    d=(((each[0]-X1)**2)+((each[1]-Y1)**2)+((each[2]-Z1)**2))**0.5
                    if d<float(mind):
                        switch=1
            if checkInternal(T_C[0],T_C[1],T_C[2],Point)==True and switch==0:
                L_P.append([X1,Y1,Z1])
                break           
        except:
            v=1
    i+=1

XC=[]; YC=[]; ZC=[]
for each in L_P:
    XC.append(each[0])
    YC.append(each[1])
    ZC.append(each[2])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(XC, YC, ZC, c='r', marker='o')
ax.plot([T_C[0][0],T_C[1][0]], [T_C[0][1],T_C[1][1]], [T_C[0][2],T_C[1][2]], '-b')
ax.plot([T_C[1][0],T_C[2][0]], [T_C[1][1],T_C[2][1]], [T_C[1][2],T_C[2][2]], '-b')
ax.plot([T_C[2][0],T_C[0][0]], [T_C[2][1],T_C[0][1]], [T_C[2][2],T_C[0][2]], '-b')
T_S=[T_C]

for every in L_P:
    i=0
    for r1 in T_S:
        if checkInternal(r1[0],r1[1],r1[2],every)==True:
            T_S[i]=[r1[0],r1[1],every]
            T_S.append([r1[1],r1[2],every])
            T_S.append([r1[2],r1[0],every])
        i+=1

print(T_S)

for each in T_S:
    ax.plot([each[0][0],each[1][0]], [each[0][1],each[1][1]], [each[0][2],each[1][2]], '-b')
    ax.plot([each[1][0],each[2][0]], [each[1][1],each[2][1]], [each[1][2],each[2][2]], '-b')
    ax.plot([each[2][0],each[0][0]], [each[2][1],each[0][1]], [each[2][2],each[0][2]], '-b')
                
plt.show()

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(L_P)

x=input(" CDE ")
    
