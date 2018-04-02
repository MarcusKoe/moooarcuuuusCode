// code from moooarcuuuus as extension for Kites

#include "config.h"
#include "defs.h"

//--------------------------------------------------------------------------------------


bool intervallcheckDPadmouse(byte RowTimeArray) {
  uint32_t TimeLastcheck = MouseIntervalls[RowTimeArray][0] ;
  uint32_t TimeIntervall = MouseIntervalls[RowTimeArray][1] ; 
  if(millis() >= (TimeLastcheck + TimeIntervall)){
        MouseIntervalls[RowTimeArray][0] = millis() ;
        uint8_t speed = MouseSpeed[RowTimeArray] ;
        MouseSpeed[RowTimeArray] = speed + 1 ;
  } 
}










void JoystickMouseFunction(){
  
  if (cfg.iscalib1) {
    uint16_t x = analogRead(PIN_JOY1_X);
    uint16_t y = analogRead(PIN_JOY1_Y);
    
    int16_t xx = x-cfg.xmid1;
    int16_t yy = y-cfg.ymid1;

    if (xx > cfg.dz) {
      xx -= cfg.dz;
    } else if (xx<(cfg.dz-cfg.dz-cfg.dz)) {
      xx += cfg.dz;
    } else {
      xx = 0;
    }

    if (yy > cfg.dz) {
      yy -= cfg.dz;
    } else if (yy<(cfg.dz-cfg.dz-cfg.dz)) {
      yy += cfg.dz;
    } else {
      yy = 0;
    }

    uint8_t MS = MouseIntervalls[0][2] ;
    xx = map(xx, cfg.xmin1+50, cfg.xmax1-50, -MS, MS);
    yy = map(yy, cfg.ymin1+50, cfg.ymax1-50, MS, -MS);
    int8_t xMove ;
    int8_t yMove ;
    if(cfg.Joy1Mouseaxis == 0){
      xMove = xx;
      yMove = yy;
    } else {
      xMove = yy;
      yMove = xx;
    }

    if(cfg.XInvert == 1){
        xMove = -1 * xMove ;
    }

    if(cfg.YInvert == 1){
        yMove = -1 * yMove ;
    }

    Mouse.move(xMove, yMove);
  } else {
    Mouse.move(0, 0);
  }

}







void C64v1(){

  JoystickMouseFunction() ;


  if(btns[B_UP]) {
    Keyboard.press(KEYPAD_8);
  } else {
    Keyboard.release(KEYPAD_8);
  }
  if (btns[B_DOWN]) {
    Keyboard.press(KEYPAD_2);
  } else {
    Keyboard.release(KEYPAD_2);
  }
  if (btns[B_LEFT]) {
    Keyboard.press(KEYPAD_4);
  } else {
    Keyboard.release(KEYPAD_4);
  }
  if (btns[B_RIGHT]) {
    Keyboard.press(KEYPAD_6);
  } else {
    Keyboard.release(KEYPAD_6);
  }


  if (btns[B_R1]) {
    Keyboard.press(KEY_1);
  } else {
    Keyboard.release(KEY_1);
  }
  if (btns[B_L1]) {
    Keyboard.press(KEY_SPACE);
  } else {
    Keyboard.release(KEY_SPACE);
  }
  // if (btns[B_L2]) {
  //   Keyboard.press(KEY_E);
  // } else {
  //   Keyboard.release(KEY_E);
  // }
  // if (btns[B_R2]) {
  //   Keyboard.press(KEY_LEFT_SHIFT);
  // } else {
  //   Keyboard.release(KEY_LEFT_SHIFT);
  // }



  if (btns[B_A]) {
    Keyboard.press(KEYPAD_0);
  } else {
    Keyboard.release(KEYPAD_0);
  }
  if (btns[B_B]) {
    Keyboard.press(KEYPAD_8);
  } else {
    Keyboard.release(KEYPAD_8);
  }
  if (btns[B_Y]) {
    Keyboard.press(KEY_J);
  } else {
    Keyboard.release(KEY_J);
  }
  
  // if (btns[B_X]) {
  //   Keyboard.press(KEY_LEFT_ARROW);
  // } else {
  //   Keyboard.release(KEY_LEFT_ARROW);
  // }

  if (btns[B_START]) {
    Keyboard.press(KEY_F12);
  } else{
    Keyboard.release(KEY_F12);
  }
  if (btns[B_SELECT]) {
    Keyboard.press(KEY_RETURN);
  } else {
    Keyboard.release(KEY_RETURN);
  }
  
}










void SetMousespeed(){
  uint8_t IvT = 0;
  uint8_t AmD = 0;
  if (cfg.Mousespeed == 0){
    IvT = 125 ;
    AmD = 25 ;
  } else if (cfg.Mousespeed == 1){
    IvT = 100 ;
    AmD = 30 ;
  } else if (cfg.Mousespeed == 2){
    IvT = 75 ;
    AmD = 35 ;
  } else if (cfg.Mousespeed == 3){
    IvT = 50 ;
    AmD = 40 ;
  } else if (cfg.Mousespeed == 4){
    IvT = 25 ;
    AmD = 45 ;
  }

  for(int i=0; i<4; i++){
    MouseIntervalls[i][1] = IvT ;
    MouseIntervalls[i][2] = AmD ;
  }
}





void Inputfunctions(){
  
    //SetMousespeed();
    C64v1();

}





