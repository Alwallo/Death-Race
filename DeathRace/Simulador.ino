
//Define pines.
const int joystickX = A1;            // joystick eje X   
const int joystickY = A0;            // joystick eje Y 

int leerTeclas(int eje) {
  int lectura = analogRead(eje);                   // leer valor analogico.
  lectura = map(lectura, 0, 1023, 0, 10);
   delay(20);
   return lectura;
 }
 
void setup() {
  Serial.begin(9600);
  pinMode (2, INPUT);
  pinMode (3, OUTPUT);
}

void loop() {

  if (digitalRead(2) == HIGH){
    digitalWrite(3, HIGH);
    Serial.println("Disparo");
  }
  else{
    digitalWrite(3, LOW);
  }
  
  int leerY = leerTeclas(joystickX);
  int leerX = leerTeclas(joystickY);
  //Serial.println(String(leerX)+", "+String(leerY));
  if (leerX < 3){
    Serial.println("Derecha");
  }
  else{
    if(leerX > 8){
      Serial.println("Izquierda");
    }
    else{
      if(leerY < 3){
        Serial.println("Arriba");
      }
      else{
        if(leerY > 8){
          Serial.println("Abajo");
        }
        else{
          Serial.println("Centro");
        }
      }
    }
  }
}
 
