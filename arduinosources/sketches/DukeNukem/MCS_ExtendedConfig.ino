// code from moooarcuuuus as extension for Kites

#include "config.h"
#include "defs.h"

//--------------------------------------------------------------------------------------







void ExtendedConfig(){
  
  if(mode == 1){    // 1 = Pressed

    if(btns[B_L1]){
      if(L1Presstime == 0){
        L1Presstime = millis();
      }
      uint32_t L1Deltatime = millis() - L1Presstime ;
      if(L1Deltatime <5000 ){
        L1State = 1 ;
        analogWrite(PIN_BL, 75);
        //delay(500);
      } else if (L1Deltatime <10000) { 
        L1State = 2 ;
        analogWrite(PIN_BL, 150);
        //delay(500);
      } else if (L1Deltatime <15000) { 
        L1State = 3 ;
        analogWrite(PIN_BL, 200);
        //delay(500);
      } else if (L1Deltatime <20000) { 
        L1State = 4 ;
        analogWrite(PIN_BL, 225);
        //delay(500);
      }
    } else {
      SetconfigL1() ;
    }
    if(btns[B_R1]){
      if(R1Presstime == 0){
        R1Presstime = millis();
      }
      uint32_t R1Deltatime = millis() - R1Presstime ;
      if(R1Deltatime <5000 ){
        R1State = 1 ;
        analogWrite(PIN_BL, 75);
      } else if (R1Deltatime <10000) { 
        R1State = 2 ;
        analogWrite(PIN_BL, 150);
      } else if (R1Deltatime <15000) { 
        R1State = 3 ;
        analogWrite(PIN_BL, 200);
      } else if (R1Deltatime <20000) { 
        R1State = 4 ;
        analogWrite(PIN_BL, 225);
      }
    } else {
      SetconfigR1();
    }
  } else {
  	L1Presstime = 0 ;
  	L1State = 0 ;
  	R1Presstime = 0 ;
  	R1State = 0 ;
  }

} 



void SetconfigL1(){

  if(L1State != 0){

	  if(L1State == 1){
	    cfg.Mousespeed += 1 ;
	    if(cfg.Mousespeed == 5){
	      cfg.Mousespeed = 0 ;
	    }
	  }
	  if(L1State == 2){
	    cfg.XInvert = !cfg.XInvert ;
	  }
	  if(L1State == 3){
	    cfg.mousemode += 1 ;
	    if(cfg.mousemode == 2){
	      cfg.mousemode = 0 ;
	    }
	  }
	  if(L1State == 4){
	    // Nothing to do here
	  }

    eepromWrite();  
    analogWrite(PIN_BL, 255);
    delay(500);
    analogWrite(PIN_BL, cfg.bl_val);
  	L1Presstime = 0 ;
  	L1State = 0 ;
  }

}




void SetconfigR1(){

  if(R1State != 0){

	if(R1State == 1){
	  cfg.Joy1Mouseaxis = !cfg.Joy1Mouseaxis ;
	}
	if(R1State == 2){
	  cfg.YInvert = !cfg.YInvert ;
	}
	if(R1State == 3){
	  cfg.screensavermode = !cfg.screensavermode ;
	}
	if(R1State == 4){
	  // Nothing to do here
	}

    eepromWrite();  
    analogWrite(PIN_BL, 255);
    delay(500);
    analogWrite(PIN_BL, cfg.bl_val);
  	R1Presstime = 0 ;
  	R1State = 0 ;
  }
}







//--------------------------------------------------------------------------------------
// Screensaver
void screensaver(){

  if(mode == 0){

    if(cfg.screensavermode == 1){
      for(int i=0; i<sizeof(btns); i++){
        if(btns[i]){
          ButtonLastpressed = millis();
        }
      }
      //Serial.println('screensaver active')
      uint32_t deltatime = millis() - ButtonLastpressed ;
      uint32_t ssStarttime = ButtonLastpressed + screensavertime * 1000 ;
      if(deltatime > ssStarttime){
        uint32_t ssEndtime = ssStarttime + 15000 ;
        if(deltatime >= ssEndtime){
          deltatime = ssEndtime ;
        }
        uint8_t val = map(deltatime, ssStarttime, ssEndtime, cfg.bl_val, 255);
        analogWrite(PIN_BL, val) ;
      } else {
        analogWrite(PIN_BL, cfg.bl_val);
      }
    }

  }

}