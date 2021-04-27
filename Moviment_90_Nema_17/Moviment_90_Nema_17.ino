int pin_mot[6]={22,26,30,34,38,42};
int pin_dir[6]={24,28,32,36,40,44};
int s=0;
int c=0;
int motor;
int dir;
int sentido;
int m[1000];
int d[1000];

void setup() {                
  
  // inicializamos pin como salidas.
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(22, OUTPUT); 
  pinMode(24, OUTPUT); 
  pinMode(26, OUTPUT); 
  pinMode(28, OUTPUT);
  pinMode(30, OUTPUT); 
  pinMode(32, OUTPUT); 
  pinMode(34, OUTPUT); 
  pinMode(36, OUTPUT);
  pinMode(38, OUTPUT); 
  pinMode(40, OUTPUT); 
  pinMode(42, OUTPUT); 
  pinMode(44, OUTPUT); 
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
    for (int i=0;i<=(c-2);i++){
      motor=m[i];
      dir=d[i];
      if (dir==0){
        sentido=LOW;
      }
      else{
        sentido=HIGH;
      }
      while (s!=50){
        digitalWrite(pin_dir[motor], sentido);    // cambiamos de dirección segun pulsador
        digitalWrite(pin_mot[motor], HIGH);         // Aqui generamos un flanco de bajada HIGH - LOW
        delay(1.5);              // Pequeño retardo para formar el pulso en STEP
        digitalWrite(pin_mot[motor], LOW);         // y el A4988 de avanzara un paso el motor
        delay(1.5); // generamos un retardo con el valor leido del potenciometro
        s+=1;
      }
     s=0;
     delay(1000);
    }
}
