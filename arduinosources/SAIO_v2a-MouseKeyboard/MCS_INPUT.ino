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



void DpadArrowkeys(){

  if(btns[B_UP]) {
    Keyboard.press(KEY_UP_ARROW);
  } else {
    Keyboard.release(KEY_UP_ARROW);
  }
  if (btns[B_DOWN]) {
    Keyboard.press(KEY_DOWN_ARROW);
  } else {
    Keyboard.release(KEY_DOWN_ARROW);
  }
  if (btns[B_LEFT]) {
    Keyboard.press(KEY_LEFT_ARROW);
  } else {
    Keyboard.release(KEY_LEFT_ARROW);
  }
  if (btns[B_RIGHT]) {
    Keyboard.press(KEY_RIGHT_ARROW);
  } else {
    Keyboard.release(KEY_RIGHT_ARROW);
  }

}




void KeyboardWithButtons(){

  DpadArrowkeys() ;

  if (btns[B_A]) {
    Keyboard.press(KEY_RETURN);
  } else {
    Keyboard.release(KEY_RETURN);
  }
  if (btns[B_B]) {
    Keyboard.press(KEY_ESC);
  } else {
    Keyboard.release(KEY_ESC);
  }
  if (btns[B_X]) {
    Keyboard.press(KEY_PERIOD);
  } else {
    Keyboard.release(KEY_PERIOD);
  }
  if (btns[B_Y]) {
    Keyboard.press(KEY_SPACE);
  } else {
    Keyboard.release(KEY_SPACE);
  }

  if (btns[B_START]) {
    Keyboard.press(KEY_LEFT_CTRL);
  } else {
    Keyboard.release(KEY_LEFT_CTRL);
  }
  if (btns[B_SELECT]) {
    Keyboard.press(KEY_LEFT_SHIFT);
  } else {
    Keyboard.release(KEY_LEFT_SHIFT);
  }

}




void MousewithDpad() {

  if(btns[B_UP]) {
    intervallcheckDPadmouse(0) ;
    Mouse.move(0, -MouseSpeed[0]);
  } else {
    MouseSpeed[0] = 0 ;
  }
  if(btns[B_DOWN]) {
    intervallcheckDPadmouse(1) ;
    Mouse.move(0, MouseSpeed[1]);
  } else {
    MouseSpeed[1] = 0 ;
  }
  if(btns[B_LEFT]) {
    intervallcheckDPadmouse(2) ;
    Mouse.move(-MouseSpeed[2], 0);
  } else {
    MouseSpeed[2] = 0 ;
  }
  if(btns[B_RIGHT]) {
    intervallcheckDPadmouse(3) ;
    Mouse.move(MouseSpeed[3], 0);
  } else {
    MouseSpeed[3] = 0 ;
  }    

  if (btns[B_A]) {
    Mouse.press(MOUSE_RIGHT);
  } else {
    Mouse.release(MOUSE_RIGHT);
  }
  if (btns[B_B]) {
    Mouse.press(MOUSE_LEFT);
  } else {
    Mouse.release(MOUSE_LEFT);
  }
  if (btns[B_X]) {
    Keyboard.press(KEY_PERIOD);
  } else {
    Keyboard.release(KEY_PERIOD);
  }
  if (btns[B_Y]) {
    Keyboard.press(KEY_ESC);
  } else {
    Keyboard.release(KEY_ESC);
  }

  if (btns[B_START]) {
    Keyboard.press(KEY_SPACE);
  } else {
    Keyboard.release(KEY_SPACE);
  }
  if (btns[B_SELECT]) {
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_F5);
  } else {
    Keyboard.release(KEY_F5);
    Keyboard.release(KEY_LEFT_CTRL);
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







void JoystickMouse(){

  JoystickMouseFunction() ;
  DpadArrowkeys();


  if (btns[B_L1]) {
    Mouse.press(MOUSE_LEFT);
  } else {
    Mouse.release(MOUSE_LEFT);
  }
  if (btns[B_R1]) {
    Mouse.press(MOUSE_RIGHT);
  } else {
    Mouse.release(MOUSE_RIGHT);
  }

  if (btns[B_A]) {
    Keyboard.press(KEY_RETURN);
  } else {
    Keyboard.release(KEY_RETURN);
  }
  if (btns[B_B]) {
    Keyboard.press(KEY_ESC);
  } else {
    Keyboard.release(KEY_ESC);
  }
  if (btns[B_X]) {
    Keyboard.press(KEY_PERIOD);
  } else {
    Keyboard.release(KEY_PERIOD);
  }
  if (btns[B_Y]) {
    Keyboard.press(KEY_M);
  } else {
    Keyboard.release(KEY_M);
  }

  if (btns[B_START]) {
    Keyboard.press(KEY_SPACE);
  } else{
    Keyboard.release(KEY_SPACE);
  }
  if (btns[B_SELECT]) {
    Keyboard.press(KEY_LEFT_CTRL);
    Keyboard.press(KEY_F5);
  } else {
    Keyboard.release(KEY_F5);
    Keyboard.release(KEY_LEFT_CTRL);
  }
  
}










void SetMousespeed(){
  uint8_t IvT = 0;
  uint8_t AmD = 0;
  if (cfg.Mousespeed == 0){
    IvT = 125 ;
    AmD = 5 ;
  } else if (cfg.Mousespeed == 1){
    IvT = 100 ;
    AmD = 8 ;
  } else if (cfg.Mousespeed == 2){
    IvT = 75 ;
    AmD = 10 ;
  } else if (cfg.Mousespeed == 3){
    IvT = 50 ;
    AmD = 12 ;
  } else if (cfg.Mousespeed == 4){
    IvT = 25 ;
    AmD = 15 ;
  }

  for(int i=0; i<4; i++){
    MouseIntervalls[i][1] = IvT ;
    MouseIntervalls[i][2] = AmD ;
  }
}





void KeyboardJoystickMouse(){
  
  

  SetMousespeed();

  if(cfg.mousemode == 0){
   if((btns[B_R1])){
      KeyboardWithButtons();
    } else {
      MousewithDpad();  
    }

  } else if(cfg.mousemode == 1){

    JoystickMouse();

  }


}





