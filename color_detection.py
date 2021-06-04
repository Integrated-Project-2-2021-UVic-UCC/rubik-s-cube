import numpy as np
import cv2
import matplotlib.pyplot as plt

#Creation of dictionary of how the faces are related with de center
dic_caras={}
dic_caras['B']=[['Y','d'],['R','l'],['W','u'],['O','r']]
dic_caras['R']=[['Y','r'],['G','l'],['W','r'],['B','r']]
dic_caras['O']=[['Y','l'],['B','l'],['W','l'],['G','r']]
dic_caras['G']=[['Y','u'],['R','r'],['W','d'],['O','l']]
dic_caras['Y']=[['G','u'],['R','u'],['B','u'],['O','u']]
dic_caras['W']=[['B','d'],['R','d'],['G','d'],['O','d']]

#Creation of dictionary with all 3 centers scanned
dic_centres={}
dic_centres['B']=[['O','W'],['W','R'],['R','Y'],['Y','O']]
dic_centres['R']=[['W','G'],['G','Y'],['Y','B'],['B','W']]
dic_centres['O']=[['B','Y'],['Y','O'],['G','W'],['W','B']]
dic_centres['G']=[['Y','R'],['R','W'],['W','O'],['O','Y']]
dic_centres['Y']=[['R','G'],['G','O'],['O','B'],['B','R']]
dic_centres['W']=[['O','G'],['G','R'],['R','B'],['B','O']]

#Function to change the number of the contour for the letter of the colour
def s_llista(llista,c,value):
    for f in range(0,3):
        if c+1 in llista[f]:
            i=llista[f].index(c+1)
            llista[f][i]=value
            break
#Function to correct the centers in case one of three is not detected
def center_correction(c1,c2,c3):
    #Look for all three and see which one is not a str
    r1=isinstance(c1,str)
    r2=isinstance(c2,str)
    r3=isinstance(c3,str)
    #Deppendig of the center that is not detected
    #According to the dict created before, say which letter correspond
    if r3==False:
        c1=c1.upper()
        c2=c2.upper()
        for key in dic_centres:
            for c in dic_centres[key]:
                if c[0]==c1 and c[1]==c2:
                    c3=key
                    break
    else:
        if r2==False:
            key=c3.upper()
            c1=c1.upper()
            for pos in dic_centres[key]:
                if pos[0]==c1:
                    c2=pos[1]
                    break
        else:
            key=c3.upper()
            c2=c2.upper()
            for pos in dic_centres[key]:
                if pos[1]==c2:
                    c1=pos[0]
                    break    
    c1=c1.upper()
    c2=c2.upper()
    c3=c3.upper()
    return c1,c2,c3
        
        

def obtenir_imatge():
    cap = cv2.VideoCapture(0) #Open camera

    #Create shape reference
    U1 = np.array([[304,6],[528,92],[311,225],[83,112]], np.int32)
    U2 = np.array([[83,112],[311,225],[318,472],[146,320]], np.int32)
    U3 = np.array([[311,225],[528,92],[490,310],[318,472]], np.int32)


    #Show the image of the cube and the shape ref.
    while(True):
        ret, frame = cap.read()#Capture frame
        #Add the cube to the image
        cv2.polylines(frame,[U1],True,(0,255,255))
        cv2.polylines(frame,[U2],True,(0,255,255))
        cv2.polylines(frame,[U3],True,(0,255,255))
        cv2.imshow('frame',frame) #Show the image
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #waitKey(1) update image every milisecond
            #When q is pressed, image is captured
            break

        
    cap.release()
    cv2.destroyAllWindows()
    return frame

def mascares(img):
    #Protocol to create masks for each colour
    #Convert image to hsv
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #HSV Rangs for each colour
    lower_blue = np.array([100,80,0])
    upper_blue = np.array([130,255,255])

    lower_yellow = np.array([23,20,50])
    upper_yellow = np.array([40,255,255])

    lower_orange = np.array([7,90,0])
    upper_orange = np.array([20,255,255])

    lower_red = np.array([0,0,0])
    upper_red = np.array([6,255,255])

    lower_green = np.array([40,40,40])
    upper_green = np.array([80,255,255])

    lower_white = np.array([0,0,0])
    upper_white = np.array([179,80,255])

    #Create a mask for each of them
    m_b = cv2.inRange(hsv_img, lower_blue, upper_blue)
    m_y = cv2.inRange(hsv_img, lower_yellow, upper_yellow)
    m_o = cv2.inRange(hsv_img, lower_orange, upper_orange)
    m_r = cv2.inRange(hsv_img, lower_red, upper_red)
    m_g = cv2.inRange(hsv_img, lower_green, upper_green)
    m_w = cv2.inRange(hsv_img, lower_white, upper_white)

    #Add masks to a list
    ll_masc=[m_w,m_b,m_y,m_o,m_r,m_g]

    #Create a Kernel (filter)
    kernel = np.ones((5,5),np.uint8)

    #for each mask, apply the filters with kernels
    #Improve image quality
    for i in range(0,len(ll_masc)):
        ll_masc[i]=cv2.morphologyEx(ll_masc[i], cv2.MORPH_CLOSE, kernel)
        ll_masc[i]=cv2.morphologyEx(ll_masc[i], cv2.MORPH_OPEN, kernel)

    return ll_masc

#----------------------------------------------------------------------#
#Create countors of each piece of the rubik's cube

def contorns():
    #Read image with 
    image = cv2.imread("cube_drawing.jpg")
    #Convert to grey scale to convert to binary
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    #Convert to binary
    _, binary = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
    #Find all the contours of the image
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #We detect more contours than 27
    c=0
    n_c=[] #List where contours are saved
    for cnt in contours:
        c+=1
        area=cv2.contourArea(cnt) #Compute the area of a contours
        if area<10000 and area>1000:
            #If it is inside the values that we have previously compute
            n_c.append(cnt) #Add them to the list
    return n_c


#--------------------------------------------------------------------#

#Function to show the image with the number of the contour
'''
for (i,c) in enumerate(n_c):
    M= cv2.moments(c)
    cx= int(M['m10']/M['m00'])
    cy= int(M['m01']/M['m00'])
    cv2.putText(image, text= str(i+1), org=(cx,cy),
            fontFace= cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0,0,0),
            thickness=2, lineType=cv2.LINE_AA)

    

plt.imshow(image)
plt.show()
'''


def deteccio_colors():
    image=obtenir_imatge()
    masc=mascares(image)
    cont=contorns()
    ll_col=['w','b','y','o','r','g']
    #List with the colour of each face
    #They are with the same order than the masks

    #Matrix of the contours sort by they number
    face1=[[27,26,24],[25,23,20],[22,19,16]]
    face2=[[18,15,12],[11,9,5],[7,3,1]]
    face3=[[13,17,21],[6,10,14],[2,4,8]]

    #For each contour, (each piece)
    for i in range(len(cont)):
        c=0
        ll_area=[]
        index=0
        maxim=0
        for mask in masc:
            #For each mask
            #Create an image of the same size all black (0)
            cimg = np.zeros_like(image)
            #Draw the contour
            cv2.drawContours(cimg, cont, i, (255,255,255), thickness=-1)
            #Convert it to grey scale
            cimg = cv2.cvtColor(cimg, cv2.COLOR_RGB2GRAY)
            #Create a binary mask
            _, cimg = cv2.threshold(cimg, 225, 255, cv2.THRESH_BINARY)
            #Add contour's mask to colour's mask
            n=cv2.copyTo(mask, cimg)
            #Count the white pixels(1) that are in the combination of two masks
            area=cv2.countNonZero(n)
            #Count whites of the contour only
            area1=cv2.contourArea(cont[i])
            if area/area1>0.6 and area/area1>maxim:
                ll_area.append(area/area1)
                maxim=area/area1
                index=c
            c+=1
        if maxim!=0:
            #If the area calculated is 60% of the contour area
            #The contour has X colour
            #Search which number and position corresponds to that colour
            s_llista(face1,i,ll_col[index])
            s_llista(face2,i,ll_col[index])
            s_llista(face3,i,ll_col[index])          
            
    return face1,face2,face3

#Change positions of a matrix
def editar_matriu(cara,d):
    A=[['','','',],['','','',],['','','',]]
    if d==1:
        c=2
        f=0
        for e in cara:
            for i in e:
                A[f][c]=i
                f+=1
            f=0
            c-=1
    else:
        c=0
        f=2
        for e in cara:
            for i in e:
                A[f][c]=i
                f-=1
            f=2
            c+=1               
    return A

#Depending on the colours of the 3 centers, change the matrix
#to have it as it is needed
def canvi_matriu(m1,m2,m3):
   #Try if all the centers are detected
    try:
        c1=m1[1][1].upper()
        c2=m2[1][1].upper()
        c3=m3[1][1].upper()
    except:
    #If not, go to function center correction
        c1,c2,c3=center_correction(m1[1][1],m2[1][1],m3[1][1])
        m1[1][1]=c1.lower()
        m2[1][1]=c2.lower()
        m3[1][1]=c3.lower()
    for item in dic_caras[c1]:
        if item[0]==c2:
            d=1
            mov=1
            posf=item[1]
            if posf!='u':
                if posf=='l':
                    d=-1
                elif posf=='d':
                    mov=2
                for i in range(0,mov):
                    m2=editar_matriu(m2,d)
        elif item[0]==c3:
            d=1
            mov=1
            posf=item[1]
            if posf!='u':
                if posf=='l':
                    d=-1
                elif posf=='d':
                    mov=2
                for i in range(0,mov):
                    m3=editar_matriu(m3,d)
    for item in dic_caras[c2]:
        if item[0]==c1:
            d=1
            mov=1 
            posf=item[1]
            if posf!='d':
                if posf=='r':
                    d=-1
                elif posf=='u':
                    mov=2
                for i in range(0,mov):
                    m1=editar_matriu(m1,d)
    return m1,m2,m3
            
