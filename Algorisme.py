from color_detection import deteccio_colors
from color_detection import canvi_matriu
import kociemba
import serial
import time

a=0

def color_correction(ll):
    #Function that corrects those colours that are not detected
    #Only if all the errors are from same colour
    d_colors={'b':0,'y':0,'o':0,'r':0,'w':0,'g':0}
    errors=0
    for face in ll:
        for f in face:
            for c in f:
                if isinstance(c,str):
                    #If it is okey, add to the dict
                    d_colors[c]+=1
    #For each colour add number of errors, in case number is different from 9
    for key in d_colors:
        if d_colors[key]!=9:
            n=9-d_colors[key]
            errors+=n
    for key in d_colors:
        #If number of errors is the same as number left to 9 of that colour
        #Change the contour of the list to the number
        if d_colors[key]!=0 and errors==9-d_colors[key]:
            for face in range(0,len(ll)):
                for f in range(0,len(ll[face])):
                    for c in range(0,len(ll[face][f])):
                        if isinstance(ll[face][f][c],int):
                            ll[face][f][c]=key
                            
#Function to write to Arduino
def write(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

#Function to read from Arduino
def write_read():
    data = arduino.readline()
    time.sleep(0.05)
    return data

#Function to send movements
def enviar_moviments(ll):    
    for instruccio in ll:
        write(instruccio[0])
        if instruccio[0]=='1':
            if instruccio[1]=='0':
                write('1')
            else:
                write('0')
        else:
            write(instruccio[1])
    write(str(9))
    write(str(9))

#Connect with Arduino
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
x=0
#Dict with positions
cube_rubik={}

#Dict with faces related to the center
dic_caras={}
dic_caras['B']=[['Y','d'],['R','l'],['W','u'],['O','r']]
dic_caras['R']=[['Y','r'],['G','l'],['W','r'],['B','r']]
dic_caras['O']=[['Y','l'],['B','l'],['W','l'],['G','r']]
dic_caras['G']=[['Y','u'],['R','r'],['W','d'],['O','l']]
dic_caras['Y']=[['G','u'],['R','u'],['B','u'],['O','u']]
dic_caras['W']=[['B','d'],['R','d'],['G','d'],['O','d']]

while a==0:
    #Run the program until detection is OK
    c1,c2,c3=deteccio_colors()
    c4,c5,c6=deteccio_colors()

    ll_caras=[c1,c2,c3,c4,c5,c6]

    ll_caras[0],ll_caras[1],ll_caras[2]=canvi_matriu(c1,c2,c3)
    ll_caras[3],ll_caras[4],ll_caras[5]=canvi_matriu(c4,c5,c6)

    color_correction(ll_caras)

    for item in ll_caras:
        cube_rubik[item[1][1].upper()]=item

    '''
    UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
    '''
    #Change language format to the one the library need
    #Add the list to an string
    ll_config=['Y','R','B','W','O','G']
    rubik=''
    for face in ll_config:
        for f in cube_rubik[face]:
            for c in f:
                if c=='y':
                    rubik+='U'
                elif c=='r':
                    rubik+='R'
                elif c=='b':
                    rubik+='F'
                elif c=='w':
                    rubik+='D'
                elif c=='o':
                    rubik+='L'
                elif c=='g':
                    rubik+='B'
                   
    print(rubik)

    try:
        if rubik=='UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB':
            input(print("Rubik's cube is solved"))
        else:
            sol=kociemba.solve(rubik)
        break
    except:
        input(print("Scanning ERROR, change the position and press ENTER to Start"))

#Change format of solution to send it to Arduino
sol=sol.split()
env=[]
motors=['U','R','F','D','L','B']
for mov in sol:
    #Each movent need the motor and direction in a list [motor,direction]
    #mov are strings like F, F2 or F'
    ll=[]
    for i in range(0,len(motors)):
        if mov[0]==motors[i]:
            #First character is the motor
            ll.append(str(i))
    if len(mov)>1:
        #If second char is "'" direction change
        if mov[1]=="'":
            ll.append('0')
            #Add to the list that is goint to be send the movement
            env.append(ll)
        #If second char is "2" is a double movement
        elif mov[1]=='2':
            ll.append('1')
            #Add 2 same movements
            env.append(ll)
            env.append(ll)
    else:
        ll.append('1')
        env.append(ll)

#Send movements
enviar_moviments(env)
input('Press key enter to START')
write('0')

    


            
        
        
        
    
