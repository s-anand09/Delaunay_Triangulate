#delaunay triangulation

#Importing Libraries
############################################################################## 
import numpy as np
import matplotlib.pyplot as plt


#Function definitions:
##############################################################################   

def sign_CP(point_1,point_2,point_3): #Check sign of cross product
    V1=[point_2[0]-point_1[0],point_2[1]-point_1[1],point_2[2]-point_1[2]] #vector 1
    V2=[point_3[0]-point_1[0],point_3[1]-point_1[1],point_3[2]-point_1[2]] #vector 2
    Sign=[(V1[1]*V2[2])-(V2[1]*V1[2]),(V1[2]*V2[0])-(V2[2]*V1[0]),(V1[0]*V2[1])-(V2[0]*V1[1])] #sign of new vector
    for i in range(0,3):
        if Sign[i]!=0:Sign[i]=Sign[i]/abs(Sign[i])
    return Sign
    
def if_inside(triangle,point_coordinates): #Triangle, point_coordinates
    C1=sign_CP(triangle[0],triangle[1],point_coordinates) #Check for side 1 
    C2=sign_CP(triangle[1],triangle[2],point_coordinates) #Check for side 2
    C3=sign_CP(triangle[2],triangle[0],point_coordinates) #Check for side 3
    if C1==C2 and C2==C3: #Should be equal if point lies inside the triangle
        Res=True
    else:
        Res=False
    return Res 

def add_point(triangle_list,point_coordinates): #List of existing triangles, point to be added
    new_triangle_list=[]
    for each in triangle_list:
        if if_inside(each,point_coordinates)==False: #add unchanged triangles
            new_triangle_list=new_triangle_list+[each]
        else: #add new triangles
            new_triangle_list=new_triangle_list+[[each[0],each[1],point_coordinates]]
            new_triangle_list=new_triangle_list+[[each[1],each[2],point_coordinates]]
            new_triangle_list=new_triangle_list+[[each[2],each[0],point_coordinates]]
            #+[each[2],each[0],point_coordinates]
            # new_triangle_list.append()
            # new_triangle_list.append()
    return new_triangle_list
            
            
def common_edge(triangle_1,triangle_2): #check for common edge
    n_common=0
    for each in triangle_1:
        for every in triangle_2:
            if each==every:n_common+=1
    if n_common==2:
        Res=True
    else: Res=False
    return Res

def find_common_edge(triangle_1,triangle_2): #find common edge
    com_edge=[]
    for each in triangle_1:
        for every in triangle_2:
            if each==every:
                com_edge.append(each)
    return com_edge

def get_angle(point_1,point_2,point_3): #enclosed angle
    import math 
    V1=[point_2[0]-point_1[0],point_2[1]-point_1[1],point_2[2]-point_1[2]] #vector 1
    V2=[point_2[0]-point_3[0],point_2[1]-point_3[1],point_2[2]-point_3[2]] #vector 2
    dot_v1_v2=(V1[0]*V2[0])+(V1[1]*V2[1])+(V1[2]*V2[2]) #dot products
    mag_v1=math.sqrt((V1[0]**2)+(V1[1]**2)+(V1[2]**2)) #Magnitude v1
    mag_v2=math.sqrt((V2[0]**2)+(V2[1]**2)+(V2[2]**2)) #Magnitude v2
    Theta=180*((math.acos((dot_v1_v2)/(mag_v1*mag_v2)))/math.pi)
    if Theta>180:
        Theta=360-Theta
    return Theta

def find_norm(point_1,point_2,point_3): #Find normal to plane
    V1=[point_2[0]-point_1[0],point_2[1]-point_1[1],point_2[2]-point_1[2]] #vector 1
    V2=[point_3[0]-point_1[0],point_3[1]-point_1[1],point_3[2]-point_1[2]] #vector 2
    Norm=[(V1[1]*V2[2])-(V2[1]*V1[2]),(V1[2]*V2[0])-(V2[2]*V1[0]),(V1[0]*V2[1])-(V2[0]*V1[1])] 
    return Norm
    
def vec_angle(V1,V2): #enclosed angle b/w two vectors
    import math 
    dot_v1_v2=(V1[0]*V2[0])+(V1[1]*V2[1])+(V1[2]*V2[2]) #dot products
    mag_v1=math.sqrt((V1[0]**2)+(V1[1]**2)+(V1[2]**2)) #Magnitude v1
    mag_v2=math.sqrt((V2[0]**2)+(V2[1]**2)+(V2[2]**2)) #Magnitude v2
    Theta=180*((math.acos((dot_v1_v2)/(mag_v1*mag_v2)))/math.pi)
    if Theta>180:
        Theta=360-Theta
    return Theta
    
def swap_edges(triangle_1,triangle_2): #Swap edges for better aspect ratio
    comedge=find_common_edge(triangle_1,triangle_2) #finding common edges
    for each in triangle_1:
        if each not in comedge:
            t1_op=each
    for each in triangle_2:
        if each not in comedge:
            t2_op=each
    old_angle= get_angle(comedge[0],t1_op,comedge[1])+get_angle(comedge[0],t2_op,comedge[1]) #angle for current configuration
    if old_angle>180:
        triangle_set=[[t1_op,comedge[0],t2_op],[t1_op,comedge[1],t2_op]]
    else:
        triangle_set=[triangle_1,triangle_2]
    return triangle_set

def plane_eq(triangle): #Plane equation
    norm=find_norm(triangle[0],triangle[1],triangle[2])
    d=-(norm[0]*triangle[0][0])-(norm[1]*triangle[0][1])-(norm[2]*triangle[0][2])
    eqn=[norm[0],norm[1],norm[2],d]
    return eqn


def dist_points(point1,point2):
    import math
    d=math.sqrt(((point2[0]-point1[0])**2)+((point2[1]-point1[1])**2)+((point2[2]-point1[2])**2))
    return d

def seed_point(master_triangle, points_list,min_mesh):
    import random
    
    mt=master_triangle
    
    plane=plane_eq(mt)
    
    xmin=min(mt[0][0],mt[1][0],mt[2][0])
    xmax=max(mt[0][0],mt[1][0],mt[2][0])
    
    ymin=min(mt[0][1],mt[1][1],mt[2][1])
    ymax=max(mt[0][1],mt[1][1],mt[2][1]) 
    
    flag=True
    
    while flag==True:
        
        flag1=True
        flag2=True
        
        sp=[random.uniform(xmin,xmax),random.uniform(ymin,ymax)]
        z=((-plane[0]*sp[0])-(-plane[1]*sp[1])-plane[3])/plane[2]
        sp.append(z)
        for each in points_list:
            if dist_points(each,sp)<min_mesh:
                flag1=False
        
        if if_inside(mt,sp)==False:
            flag2=False
        
        if flag1==True and flag2==True:
            flag=False
            
    points_list.append(sp)
    return points_list

def Area3D (X1,Y1,Z1,X2,Y2,Z2,X3,Y3,Z3):
    import math
    VEC1=[(X2-X1),(Y2-Y1),(Z2-Z1)]
    VEC2=[(X3-X1),(Y3-Y1),(Z3-Z1)]
    DotP=(VEC1[0]*VEC2[0])+(VEC1[1]*VEC2[1])+(VEC1[2]*VEC2[2])
    Mag1=((VEC1[0]**2)+(VEC1[1]**2)+(VEC1[2]**2))**0.5
    Mag2=((VEC2[0]**2)+(VEC2[1]**2)+(VEC2[2]**2))**0.5
    ANG=math.acos(DotP/(Mag1*Mag2))
    AR=0.5*Mag1*Mag2*math.sin(ANG)
    return AR

def index_maxArea(triangle_list):
    Area=[]
    for each in triangle_list:
        A=Area3D(each[0][0],each[0][1],each[0][2],each[1][0],each[1][1],each[1][2],each[2][0],each[2][1],each[2][2])
        Area.append(A)
    index=Area.index(max(Area))
    return index
    
#Calculations
############################################################################## 
    
# print(swap_edges([[0, 30, 0], [-100, 0, 0], [0, -30, 0]], [[0, 30, 0], [100, 0, 0], [0, -30, 0]]))
    
# x=[[[0,0,0],[4,0,0],[2,3,0]],[[4,0,0],[5,3,0],[2,3,0]]]#,[2,1,0])
# x1=(find_norm([0,0,0],[42,50,200],[200,35,200]))
# print(vec_angle((x1),[1,0,0]))
# print(vec_angle((x1),[0,1,0]))
# print(vec_angle((x1),[0,0,1]))
# #print(x)

mt=[[0,0,0],[4,0,0],[2,3,0]]
triangle_list=[mt]
N=int(input("Enter the number of seed points: "))
Minmesh=float(input("Enter the minimum mesh length: "))
plist=[]

#for i in range(0,N):
#   plist=seed_point(mt,plist,Minmesh)


#for each in plist: 
    
for i in range(0,N):
    plist=seed_point(mt,plist,Minmesh)
    index=index_maxArea(triangle_list)
    if if_inside(triangle_list[index],plist[i])==True:
        triangle_list=add_point(triangle_list,plist[i])
        #Sweeping 
        for t1 in triangle_list:
            i1=triangle_list.index(t1)
            for t2 in triangle_list:
                i2=triangle_list.index(t2)
                if common_edge(t1,t2)==True:
                    out=swap_edges(t1,t2)
                    triangle_list[i1]=out[0]
                    triangle_list[i2]=out[1]



#Plotting the triangles
    
XC=[]; YC=[]; ZC=[]
for each in plist:
    XC.append(each[0])
    YC.append(each[1])
    ZC.append(each[2])
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
# ax.scatter(XC, YC, ZC, c='r', marker='o')

for each in triangle_list:
    ax.plot([each[0][0],each[1][0]], [each[0][1],each[1][1]], [each[0][2],each[1][2]], '-b')
    ax.plot([each[1][0],each[2][0]], [each[1][1],each[2][1]], [each[1][2],each[2][2]], '-b')
    ax.plot([each[2][0],each[0][0]], [each[2][1],each[0][1]], [each[2][2],each[0][2]], '-b')
    

    