int steps = 22;       // pin step 9
int direccion = 24;   // pin direccion 3
int s=0;

 
void setup() {                
  
  // inicializamos pin como salidas.
  
  pinMode(steps, OUTPUT); 
  pinMode(direccion, OUTPUT); 
}
 
void loop() {

    while (s!=50){
    int sentido = HIGH;
    digitalWrite(direccion, sentido);    // cambiamos de dirección segun pulsador
    digitalWrite(steps, HIGH);         // Aqui generamos un flanco de bajada HIGH - LOW
    delay(1.5);              // Pequeño retardo para formar el pulso en STEP
    digitalWrite(steps, LOW);         // y el A4988 de avanzara un paso el motor
    delay(1.5); // generamos un retardo con el valor leido del potenciometro
    s+=1;
    }
    s=0;
    delay(1000);
  }
