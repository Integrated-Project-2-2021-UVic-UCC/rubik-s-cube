int steps = 22;       
int direccion = 24;   
int s=0;
int x=5;
int sentido;

void setup() {                
  
  // inicializamos pin como salidas.
  Serial.begin(9600);
  Serial.setTimeout(1);
  pinMode(steps, OUTPUT); 
  pinMode(direccion, OUTPUT); 
}
 
void loop() {
    while (!Serial.available());
    x = Serial.readString().toInt();
    while (s!=50){
    if (x==0){
      sentido=LOW;
    }
    else{
      sentido=HIGH;
    }
    digitalWrite(direccion, sentido);    // cambiamos de dirección segun pulsador
    digitalWrite(steps, HIGH);         // Aqui generamos un flanco de bajada HIGH - LOW
    delay(1.5);              // Pequeño retardo para formar el pulso en STEP
    digitalWrite(steps, LOW);         // y el A4988 de avanzara un paso el motor
    delay(1.5); // generamos un retardo con el valor leido del potenciometro
    s+=1;
    }
    s=0;
    delay(1000);
    x=5;
  }
