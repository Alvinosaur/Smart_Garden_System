//Normally use delay(ms), but this is inaccurate
//delays also prevent other functions from running
//instead call interrupt with built-in 16-bit timer

//these selects apply to two different multiplexers
int select0 = 2;
int select1 = 3;
int select2 = 4;

int sensorPin0 = A0;
int sensorPin1 = A1;
int sensorPin2 = A2;
  
void setup(){
  Serial.begin(9600);
  sensorSet0[8] = {0};
  sensorSet1[8] = {0};
  sensorSet2[8] = {0};
  //Activate normal mode by setting control registers A,B to 0
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 3036;
  TCCR1B |= (1<<CS12); //set prescaler to 256, change CS10 for diff prescaler
  //prescaler increments every 256 counts, so around 1047ms
  //as TCR increments from 0 to 65536, calls overflow flag at 65535
  TIMSK1 |= (1<<T0IE1);//use that flag as interrupt to trigger event
  //can adjust the prescaler to have each step incremented for logner time
}

ISR(TIMER1_OVF_vect){ //interrupt for overflow
  int startInc = 0;
  int endInc = 8;
  readSensor();
  sendValues(startInc,endInc);
  TCNT1 = 3036;
}

void readSensor(){
  for (int i = 0; i < 8; i++){
    digitalWrite(select0, HIGH && (i & B00000001));
    digitalWrite(select1, HIGH && (i & B00000010));
    digitalWrite(select2, HIGH && (i & B00000100));
    sensorSet0[i] = analogRead(sensorPin0);
    sensorSet1[i] = analogRead(sensorPin1);
    sensorSet2[i] = analogRead(sensorPin2);
  }
}
int sendValues(startInc,endInc){
  //send time and date at the start
  //for location, need to talk to jeff
  for (int i = startInc; i < endInc; i++){
    count = int(i/8)
    chooseValue(count,i,endInc);
    if (i==endInc-1)&&(i!=23){
     sendValues(startInc+8,endInc+8); 
  }
}
void chooseValue(count,i,endInc){
  switch(count){
   case 0:
    if (i == endInc-1){
    Serial.print(sensorSet0[i]);
    Serial.print(";");
    } else{
    Serial.print(sensorSet0[i]);
    Serial.print(",");
    }
    break;
   case 1:
    if (i == endInc-1){
    Serial.print(sensorSet1[i]);
    Serial.print(";");
    } else{
    Serial.print(sensorSet1[i]);
    Serial.print(",");
    }
    break;
   case 2:
    if (i == endInc-1){
    Serial.print(sensorSet2[i]);
    Serial.print(";");
    } else{
    Serial.print(sensorSet2[i]);
    Serial.print(",");
    }
    break;
    
  }
}
    
    
 

