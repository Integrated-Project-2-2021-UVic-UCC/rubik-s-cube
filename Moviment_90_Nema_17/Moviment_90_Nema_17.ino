int steps1 = 26;       
int direccion1 = 28; 
int steps2 = 22;       
int direccion2 = 24;    
int s=0;
int x=5;
int y;
int sentido;

void setup() {                
  
  // inicializamos pin como salidas.
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(steps1, OUTPUT); 
  pinMode(direccion1, OUTPUT); 
  pinMode(steps2, OUTPUT); 
  pinMode(direccion2, OUTPUT); 
}
 
void loop() {
    while (!Serial.available());
    x = Serial.readString().toInt();
    while (!Serial.available());
    y=Serial.readString().toInt();
    while (s!=50){
    if (x==0){
      sentido=LOW;
    }
    else{
      sentido=HIGH;
    }
    if (y==1){
      digitalWrite(direccion1, sentido);    // cambiamos de dirección segun pulsador
      digitalWrite(steps1, HIGH);         // Aqui generamos un flanco de bajada HIGH - LOW
      delay(1.5);              // Pequeño retardo para formar el pulso en STEP
      digitalWrite(steps1, LOW);         // y el A4988 de avanzara un paso el motor
      delay(1.5); // generamos un retardo con el valor leido del potenciometro
      s+=1;
      }
    if (y==0){
      digitalWrite(direccion2, sentido);    // cambiamos de dirección segun pulsador
      digitalWrite(steps2, HIGH);         // Aqui generamos un flanco de bajada HIGH - LOW
      delay(1.5);              // Pequeño retardo para formar el pulso en STEP
      digitalWrite(steps2, LOW);         // y el A4988 de avanzara un paso el motor
      delay(1.5); // generamos un retardo con el valor leido del potenciometro
      s+=1;
      }
    }
   s=0;
   delay(1000);
   x=5;
}
