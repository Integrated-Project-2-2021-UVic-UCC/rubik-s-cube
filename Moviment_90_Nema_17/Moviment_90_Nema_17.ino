int pin_dir[6]={22,26,30,34,38,42};
int pin_mot[6]={24,28,46,36,40,44};
int pin_enable[6]={23,27,31,35,48,52};
int s=0;
int c=0;
int motor;
int dir;
int sentido;
int m[1000];
int d[1000];

void setup() {                
  pinMode(23, OUTPUT);
  digitalWrite(23,HIGH);
  pinMode(27, OUTPUT);
  digitalWrite(27,HIGH);
  pinMode(31, OUTPUT);
  digitalWrite(31,HIGH);
  pinMode(35, OUTPUT);
  digitalWrite(35,HIGH);
  pinMode(48, OUTPUT);
  digitalWrite(48,HIGH);
  pinMode(52, OUTPUT);
  digitalWrite(52,HIGH);
  pinMode(22, OUTPUT); 
  pinMode(24, OUTPUT); 
  pinMode(26, OUTPUT); 
  pinMode(28, OUTPUT);
  pinMode(30, OUTPUT); 
  pinMode(46, OUTPUT); 
  pinMode(34, OUTPUT); 
  pinMode(36, OUTPUT);
  pinMode(38, OUTPUT); 
  pinMode(40, OUTPUT); 
  pinMode(42, OUTPUT); 
  pinMode(44, OUTPUT);
  pinMode(23, OUTPUT); 
  pinMode(27, OUTPUT);
  pinMode(31, OUTPUT);  
  pinMode(35, OUTPUT);  
  pinMode(39, OUTPUT);  
  pinMode(43, OUTPUT);

  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
    while (motor!=9 && dir!=9){
      while (!Serial.available());
      motor = Serial.readString().toInt();
      while (!Serial.available());
      dir = Serial.readString().toInt();
      m[c]=motor;
      d[c]=dir;
      c+=1;
    }
    while (!Serial.available());
    for (int i=0;i<=(c-2);i++){
      motor=m[i];
      dir=d[i];
      digitalWrite(pin_enable[motor],LOW);
      if (dir==0){
        sentido=LOW;
      }
      else{
        sentido=HIGH;
      }
      while (s!=50){
        digitalWrite(pin_dir[motor], sentido);    
        digitalWrite(pin_mot[motor], HIGH);         
        delay(1.25);              
        digitalWrite(pin_mot[motor], LOW);         
        delay(1.25); 
        s+=1;
      }
     s=0;
     delay(0);
     digitalWrite(pin_enable[motor],HIGH); 
    }
}
