#include <dht11.h> // dht11 kütüphanesini ekliyoruz.
#define DHT11PIN 10 // DHT11PIN olarak Dijital 10'u belirliyoruz.
char message;//Python tarafından gelecek olan 1 bitlik message verisini tanımladık.
dht11 DHT11;
float temp ;
float humiditydata;
int sicaklikmavi = 3;
int sicaklikyesil = 4 ;
int sicakliksari = 5;
int sicaklikkirmizi =6;
int nemkirmizi = 9 ;
int nemyesil = 8 ; 
int nemmavi = 7 ; 

int buzzer = 2;
void setup()
{
  Serial.begin(9600); // Seri iletişimi başlatıyoruz.
  pinMode(sicaklikmavi,OUTPUT);
  pinMode(sicaklikyesil,OUTPUT);
  pinMode(sicakliksari,OUTPUT);
  pinMode(sicaklikkirmizi,OUTPUT);
  pinMode(nemkirmizi,OUTPUT);
  pinMode(nemyesil,OUTPUT);
  pinMode(nemmavi,OUTPUT);
  pinMode(buzzer,OUTPUT);
}

void loop()
{
  
  
  int chk = DHT11.read(DHT11PIN);
  float temp = DHT11.temperature;
  float humiditydata = DHT11.humidity;
  
  int dataToSend = float (temp);
  int dataToSendHumidity = float (humiditydata);
  
  message=Serial.read();
  
  if (message == '1'){
    Serial.println(dataToSend);
    delay(1000); 
  }

  if (message == '3'){
    Serial.println(dataToSendHumidity);
    delay(1000); 
  }
  if (message == '4'){
      digitalWrite(nemmavi,HIGH);
      digitalWrite(sicaklikmavi,HIGH);
      delay(1000);
      digitalWrite(nemyesil,HIGH);
      digitalWrite(sicaklikyesil,HIGH);
      digitalWrite(sicakliksari,HIGH);
      delay(1000);
      digitalWrite(nemkirmizi,HIGH);
      digitalWrite(sicaklikkirmizi,HIGH);
      delay(1000);
      digitalWrite(nemkirmizi,LOW);
      digitalWrite(sicaklikkirmizi,LOW);
      delay(1000);
      
      digitalWrite(nemyesil,LOW);
      digitalWrite(sicaklikyesil,LOW);
      digitalWrite(sicakliksari,LOW);
      delay(1000);
      digitalWrite(nemmavi,LOW);
      digitalWrite(sicaklikmavi,LOW);
      delay(1000);
      
      for(int my_measure_led = 0 ; my_measure_led < 4; my_measure_led++){
        digitalWrite(nemmavi,HIGH);
        digitalWrite(nemyesil,HIGH);
        digitalWrite(nemkirmizi,HIGH);
        digitalWrite(sicaklikmavi,HIGH);
        digitalWrite(sicaklikyesil,HIGH);
        digitalWrite(sicakliksari,HIGH);
        digitalWrite(sicaklikkirmizi,HIGH);
        delay(100);
        digitalWrite(nemmavi,LOW);
        digitalWrite(nemyesil,LOW);
        digitalWrite(nemkirmizi,LOW);
        digitalWrite(sicaklikmavi,LOW);
        digitalWrite(sicaklikyesil,LOW);
        digitalWrite(sicakliksari,LOW);
        digitalWrite(sicaklikkirmizi,LOW);
        delay(100);
        tone(buzzer,5000);
        delay(100);
        noTone(buzzer);
        delay(10); 
      }
    
  }
  
  
  if(humiditydata <33 ){
    digitalWrite(nemmavi,HIGH);
    digitalWrite(nemyesil,LOW);
    digitalWrite(nemkirmizi,LOW);
    
    
    }
  else if((humiditydata >33 )&&(humiditydata<66)){
    digitalWrite(nemmavi,HIGH);
    digitalWrite(nemyesil,HIGH);
    digitalWrite(nemkirmizi,LOW);
    
    
    }
  else if((humiditydata >66 )){
    digitalWrite(nemmavi,HIGH);
    digitalWrite(nemyesil,HIGH);
    digitalWrite(nemkirmizi,HIGH);    
    }
  if(temp < 15)
    {
    digitalWrite(sicaklikmavi,HIGH);
    digitalWrite(sicaklikyesil,LOW);
    digitalWrite(sicakliksari,LOW);
    digitalWrite(sicaklikkirmizi,LOW);
    
    
    
  }
  else if ((temp > 15)&&(temp < 30))
    {
    digitalWrite(sicaklikmavi,HIGH);
    digitalWrite(sicaklikyesil,HIGH);
    digitalWrite(sicakliksari,LOW);
    digitalWrite(sicaklikkirmizi,LOW);
   
  }
  else if ((temp > 31)&&(temp < 50))
    {
    digitalWrite(sicaklikmavi,HIGH);
    digitalWrite(sicaklikyesil,HIGH);   
    digitalWrite(sicakliksari,HIGH);   
    digitalWrite(sicaklikkirmizi,LOW);
   
  }
  else if ((temp > 51))
    {
    digitalWrite(sicaklikmavi,HIGH);   
    digitalWrite(sicaklikyesil,HIGH);    
    digitalWrite(sicakliksari,HIGH);   
    digitalWrite(sicaklikkirmizi,HIGH);
    tone(buzzer,5000);
    delay(100);
    noTone(buzzer);
    delay(10);
  }
  delay(1);

}
