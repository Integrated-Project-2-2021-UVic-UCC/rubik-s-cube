# Importing Libraries
import serial
import time

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)


m=''
ll=[]
while m!='*':
    m=input('m,d:')
    a=m.split(',')
    ll.append(a)
ll=ll[:-1]
print(ll)
    

def write(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

def write_read():
    data = arduino.readline()
    time.sleep(0.05)
    return data


for instruccio in ll:
    write(instruccio[0])
    write(instruccio[1])


write(str(9))
write(str(9))


'''
while True:
    num = input("Enter a number: ") # Taking input from user
    value = write(num)

    import serial
import time
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

while True:
    num = input("Enter a number: ") # Taking input from user
    value = write_read(num)
    print(value) # printing the value
'''
