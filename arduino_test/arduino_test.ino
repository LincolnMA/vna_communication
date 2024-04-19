void setup(){
    Serial.begin(9600);
}
void loop(){
    byte data;
    if(Serial.available() > 0){
        data = Serial.read();
        Serial.write(data);
    }
}