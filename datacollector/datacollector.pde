

const int LED_PIN = 13;
const int VCC_PIN = 0;
const int GND_PIN = A1;
const int ST_PIN = A5;
const int X_PIN = 2;
const int Y_PIN = 3;
const int Z_PIN = 4;
const int DELAY_TIME = 1000;

const int mvu = 4.89;

float x = 0;
float y = 0;
float z = 0;
float vcc_mv = 0;
float scale_factor = 0;
int vcc = 0;
int zero_g = 0;

void setup() {
 pinMode(GND_PIN, OUTPUT);
 digitalWrite(GND_PIN, LOW);
 pinMode(ST_PIN, OUTPUT);
 digitalWrite(ST_PIN, LOW);
 Serial.begin(9600);
}

void loop() {
  
  vcc = analogRead(VCC_PIN);
  vcc_mv = vcc * mvu;
  scale_factor = 1 / (vcc_mv/10);
  zero_g = vcc / 2;

  x = (analogRead(X_PIN) - zero_g) * mvu * scale_factor;
  y = (analogRead(Y_PIN) - zero_g) * mvu * scale_factor;
  z = (analogRead(Z_PIN) - zero_g) * mvu * scale_factor;
  
  Serial.print(x);
  Serial.print(',');
  Serial.print(y);
  Serial.print(',');
  Serial.print(z);
  Serial.println();
  
  //delay(DELAY_TIME);
  
}
