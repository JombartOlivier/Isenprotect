/* 
 * Author: jmc
 *
 * Created on 12 july 2016
 */

// ****************************************
// ****  MEASURED CIRCUIT CONSUMPTION: ****
// ****  7 mA under 3.3 V              ****
// ****************************************

#define USE_AND_MASKS

// PIC18F23K20 Configuration Bit Settings

// 'C' source line config statements

#include <xc.h>

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

// CONFIG1H
#pragma config FOSC = INTIO7    // Oscillator Selection bits (Internal oscillator block, CLKOUT function on RA6, port function on RA7)
#pragma config FCMEN = OFF      // Fail-Safe Clock Monitor Enable bit (Fail-Safe Clock Monitor disabled)
#pragma config IESO = OFF       // Internal/External Oscillator Switchover bit (Oscillator Switchover mode disabled)

// CONFIG2L
#pragma config PWRT = OFF       // Power-up Timer Enable bit (PWRT disabled)
#pragma config BOREN = SBORDIS  // Brown-out Reset Enable bits (Brown-out Reset enabled in hardware only (SBOREN is disabled))
#pragma config BORV = 18        // Brown Out Reset Voltage bits (VBOR set to 1.8 V nominal)

// CONFIG2H
#pragma config WDTEN = OFF      // Watchdog Timer Enable bit (WDT is controlled by SWDTEN bit of the WDTCON register)
#pragma config WDTPS = 32768    // Watchdog Timer Postscale Select bits (1:32768)

// CONFIG3H
#pragma config CCP2MX = PORTC   // CCP2 MUX bit (CCP2 input/output is multiplexed with RC1)
#pragma config PBADEN = ON      // PORTB A/D Enable bit (PORTB<4:0> pins are configured as analog input channels on Reset)
#pragma config LPT1OSC = OFF    // Low-Power Timer1 Oscillator Enable bit (Timer1 configured for higher power operation)
#pragma config HFOFST = ON      // HFINTOSC Fast Start-up (HFINTOSC starts clocking the CPU without waiting for the oscillator to stablize.)
#pragma config MCLRE = ON       // MCLR Pin Enable bit (MCLR pin enabled; RE3 input pin disabled)

// CONFIG4L
#pragma config STVREN = ON      // Stack Full/Underflow Reset Enable bit (Stack full/underflow will cause Reset)
#pragma config LVP = OFF        // Single-Supply ICSP Enable bit (Single-Supply ICSP disabled)
#pragma config XINST = OFF      // Extended Instruction Set Enable bit (Instruction set extension and Indexed Addressing mode disabled (Legacy mode))

// CONFIG5L
#pragma config CP0 = OFF        // Code Protection Block 0 (Block 0 (000200-000FFFh) not code-protected)
#pragma config CP1 = OFF        // Code Protection Block 1 (Block 1 (001000-001FFFh) not code-protected)

// CONFIG5H
#pragma config CPB = OFF        // Boot Block Code Protection bit (Boot block (000000-0001FFh) not code-protected)
#pragma config CPD = OFF        // Data EEPROM Code Protection bit (Data EEPROM not code-protected)

// CONFIG6L
#pragma config WRT0 = OFF       // Write Protection Block 0 (Block 0 (000200-000FFFh) not write-protected)
#pragma config WRT1 = OFF       // Write Protection Block 1 (Block 1 (001000-001FFFh) not write-protected)

// CONFIG6H
#pragma config WRTC = OFF       // Configuration Register Write Protection bit (Configuration registers (300000-3000FFh) not write-protected)
#pragma config WRTB = OFF       // Boot Block Write Protection bit (Boot Block (000000-0001FFh) not write-protected)
#pragma config WRTD = OFF       // Data EEPROM Write Protection bit (Data EEPROM not write-protected)

// CONFIG7L
#pragma config EBTR0 = OFF      // Table Read Protection Block 0 (Block 0 (000200-000FFFh) not protected from table reads executed in other blocks)
#pragma config EBTR1 = OFF      // Table Read Protection Block 1 (Block 1 (001000-001FFFh) not protected from table reads executed in other blocks)

// CONFIG7H
#pragma config EBTRB = OFF      // Boot Block Table Read Protection bit (Boot Block (000000-0001FFh) not protected from table reads executed in other blocks)



// define time between two transmissions on SIGFOX network
// the timer cycle is 65536 * 256 * (4 / 8MHz) = 8.388608 seconds
// (16-bit, prescaler = 256, fosc = 8 MHz)
// long period (jumper removed) => 1 hour between 2 transmissions = 429 cycles
// short period (jumper inserted) => 15 mn between 2 transmissions = 107 cycles
#define long_period    429
#define short_period   107
//#define long_period    4    // for debugging
//#define short_period   1    // for debugging

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <xc.h>
#include "general.h"
#include "uart.h"
#include "i2c.h"


    UINT8_T header1;    // header = header1 header0 = frame number
    UINT8_T header0;    // from 0x0000 to 0x9999  (BCD coded))
    
    UINT8_T bat_voltage1;   // battery voltage = bat_voltage1 bat_voltage0 (BCD coded)
    UINT8_T bat_voltage0;   // from 0x0000 to 0x9999  (BCD coded))
                            // bat_voltage1 holds volt units, bat_voltage0 holds tenths and hundreds
                            // i.e. 0x06 0x51 for 6.51 V

    UINT8_T panel_voltage1;     // solar panel voltage = panel_voltage1 panel_voltage0 (BCD coded)
    UINT8_T panel_voltage0;     // from 0x0000 to 0x9999  (BCD coded))
                                // panel_voltage1 holds  volt units, voltage 0 holds tenths and hundreds
                                // i.e. 0x17 0x60 for 17.60 V

    float volts;                     // voltage in Volts
    UINT16_T volts_cV;               // voltage in centiVolts
    unsigned int ADC_result;

    UINT8_T temp_H;             // 1st byte (high byte) read from temperature sensor
    UINT8_T temp_L;             // 2nd byte (low byte) read from temperature sensor
    INT16_T temperature;        // temperature (concatenation of temp_H and temp_L)
    UINT8_T temp_BCD;           // temp (only the integer part) BCD coded
    
    BOOL send_data;
    UINT16_T timer_tick;             

    
    void update_header(void);
    void measure_battery(void);
    void measure_panel(void);
    void measure_temp(void);
    void inc_data(UINT8_T *data_pointer);
    void transmit_by_SIGFOX(void);
//    void send_to_module(UINT8_T *to_send_pointer);

void interrupt TMR0Interrupt() {

  if (INTCONbits.TMR0IF == 1)     // check if interrupt is triggered by TMR0
  {
      ++timer_tick;

      // jumper removed => RA2 = 0 => long period between 2 transmissions
      // jumper inserted => RA2 = 1 => short period between 2 transmissions
      if (((PORTAbits.RA2 == 0)&&(timer_tick >= long_period)) || ((PORTAbits.RA2 == 1)&&(timer_tick >= short_period)))
      {
        send_data = 1;
        timer_tick = 0;
      } 

      INTCONbits.TMR0IF = 0;     // clear interrupt flag
  }
}


int main(int argc, char** argv) {
    
    OSCCON = 0b01101100;    // internal oscillator = 8 MHz (=> for UART, SPBRG1 will be set to 16 = 0x10 (thus baudrate = 117647 bps and error = +2 %)
    header1 = 0;
    header0 = 0;
    bat_voltage1 = 0;
    bat_voltage0 = 0;
    panel_voltage1 = 0;
    panel_voltage0 = 0;
    send_data = 0;

    // ***** IOs configuration *****
    TRISA = 0b00000111;     // RA0 & RA1: analog inputs  --  RA2: digital input  --  others are outputs
    TRISB = 0x00;           // RBi: output
    // TRISB = 0b11000000;  // for debugging: PGC and PGD should be configured as inputs
    TRISC = 0b10011000;     // RC7(RX)  --  RC6(TX)  --  RC4(SDA) & RC3(SCL): must be configured as inputs

//    TRISAbits.TRISA0 = 1;               // analog input on RA0 (battery)
//    TRISAbits.TRISA1 = 1;               // analog input on RA1
//    TRISAbits.TRISA2 = 1;               // digital input on RA2 (to select data sending period)

    // ***** ADC configuration *****
    ADCON2 = 0b10111110;                // right justified (ADFM=1), A/D acq time = 20 TAD (ACTQ<2:0>=111), A/D clock = fOSC/64 (ADCS<2:0>=110)
    ADCON1 = 0b00000000;                // voltage ref = Vdd,Vss, 
    ADCON0 = 0b00000001;                // channel 0, stop conversion (GODONE=0), enable ADC (ADON=1)

    ANSELH = 0b00000000;
    ANSEL = 0b00000011;                 // analog input on RA0 and RA1 (disable digital input buffer)
    
    // ***** Timer0 configuration *****
    T0CON = 0b10000111;                 // Timer on, 16-bit, internal clock, prescaler = 256
    
    // ***** Interrupts configuration *****   
    INTCON = 0b00100000;                // enable TMR0 overflow interrupt

    // ***** UART configuration *****   
    UARTInit(115200);     // init UART @ 115200 bps

    // ***** I2C configuration *****   
    i2c_init();

    ei();                         // enable interrupt

    

    forever
    {
        if (send_data == 1)
        {
            update_header();
            measure_battery();
            measure_panel();
            measure_temp();
            transmit_by_SIGFOX();
            send_data = 0;
        }
    };

    return (EXIT_SUCCESS);
}

void update_header(void)
{
    inc_data(&header0);
    if (header0 == 0x00)
    {
        inc_data(&header1);
    }
}

void measure_battery(void)
{
//    float volts;                     // voltage in Volts
//    UINT16_T volts_cV;                  // voltage in cVolts
//    unsigned int ADC_result;         // 16-bit 2's complement - to store the result of ADC conversion
    
    ADCON0 = 0b00000001;             // select channel 0 (AN0)
    ConvertADC();                    // start conversion (GO = 1)
    while (BusyADC());               // wait until GO/DONE falls to 0
    ADC_result = ReadADC();          // read (ADRESH | ADRESL) and return int (16-bit unsigned)
    // convert ADC value into volts
    // 1 LSB is (3.3 / 1023) volt
    // take into account input resistive divider: 330k and 220k
    // (so 7V battery voltage is translated to 2.8V)
    // => voltage resolution is (3.3 / 1023) * (550 / 220) = 8 mV
    // => max voltage on input = 3.3 * (550 / 220) = 8.25 V
//    volts = (3.3 / 1023) * (550 / 220) * ADC_result;    // example: volts = 6.51
    // remarque: la ligne ci-dessus donne un résultat erroné (testé avec le debugger))
    // => il faut la simplifier par la ligne ci-dessous
//    volts = (8.25 / 1023) * ADC_result;
    volts = (8.32 / 1023) * ADC_result;         // adjusted relation based on practical test
                                                // (takes into account components deviation)
    volts_cV = (UINT16_T)(volts * 100);                         // example: volts_cV = 651
    bat_voltage1 = volts_cV / 100;                                  // example: bat_voltage1 = 0x06
    bat_voltage0 = ((volts_cV / 10) % 10 << 4) | (volts_cV % 10);   // example: bat_voltage0 = 0x51
    
}

void measure_panel(void)
{
//    float volts;                     // voltage in Volts
//    UINT16_T volts_cV;                  // voltage in cVolts
//    unsigned int ADC_result;         // 16-bit 2's complement - to store the result of ADC conversion
    
    ADCON0 = 0b00000101;             // select channel 1 (AN1)
    ConvertADC();                    // start conversion (GO = 1)
    while (BusyADC());               // wait until GO/DONE falls to 0
    ADC_result = ReadADC();          // read (ADRESH | ADRESL) and return int (16-bit unsigned)
    // convert ADC value into volts
    // 1 LSB is (3.3 / 1023) volt
    // take into account input resistive divider: (330k + 330k) and 68k
    // (so 25V panel voltage is translated to 2.33V)
    // => voltage resolution is (3.3 / 1023) * (728 / 68) = 34 mV
    // => max voltage on input = 3.3 * (768 / 68) = 37.3 V
//    volts = (3.3 / 1023) * (728 / 68) * ADC_result;    // example: volts = 17.60
//    volts = (35.8 / 1023) * ADC_result;       // theoretical equation
    volts = (35.9 / 1023) * ADC_result;         // adjusted relation based on practical test
                                                // (takes into account components deviation)
    volts_cV = (UINT16_T)(volts * 100);                    // example: volts_cV = 1760
    panel_voltage1 = ((volts_cV / 1000) << 4) | ((volts_cV / 100) % 10);    // example: panel_voltage1 = 0x17
    panel_voltage0 = ((volts_cV / 10) % 10 << 4) | (volts_cV % 10);         // example: panel_voltage0 = 0x60
    
}

void measure_temp(void)
{
        i2c_start();                                    // send start condition
        i2c_write((AT30TS75_ADDRESS << 1) | I2C_READ);  // send to slave 7-bit address (1001 000) + RD (1)
        temp_H = i2c_read();                            // receive 1st byte
        i2c_ACK();
        temp_L = i2c_read();                            // receive 2nd byte       
        i2c_NAK();                                      // send a NAK (last read)
        i2c_stop();                                     // send stop condition
        temperature = (temp_H << 8) | temp_L;
        // temp_H holds the integer part of temperature in degrees
        // temp_L holds the fractional part of temperature)
        temp_BCD = ((temp_H / 10) << 4) | (temp_H % 10);    // keep only the integer part, BCD coded
}


void inc_data(UINT8_T *data_pointer)           // increment byte in BCD format
{                                              // from 0x00 to 0x99 then roll-over
    if ((*data_pointer & 0x0F) < 9)      // test low nibble
    {
        ++*data_pointer;
    }
    else
    {
        *data_pointer = *data_pointer & 0xF0;       // reset low nibble
        if ((*data_pointer & 0xF0) < 0x90)     // and update high nibble (increment or reset)
        {
            *data_pointer = *data_pointer + 0x10;
        }
        else
        {
            *data_pointer = *data_pointer & 0x0F;
        }
    }
}

void transmit_by_SIGFOX (void)
{
    UARTWriteByte(0xFF);
    UARTWriteByte(0xFF);
    UARTWriteByte(0xFF);
    UARTWriteByte(0xFF);
    UARTWriteByte(0xFF);
    UARTWriteByte('A');     // ASCII code = 0x41
    UARTWriteByte('T');     // ASCII code = 0x54
    UARTWriteByte('$');     // ASCII code = 0x24
    UARTWriteByte('S');     // ASCII code = 0x53
    UARTWriteByte('F');     // ASCII code = 0x46
    UARTWriteByte('=');     // ASCII code = 0x3D

    // message begin

    // ------- 1st byte = header1 -------------------------
    UARTWriteByte((header1 >> 4) + '0');       // transmit high nibble in ASCII format
    UARTWriteByte((header1 & 0x0F) + '0');     // transmit low nibble in ASCII format    
    // ------- 2nd byte = header0 -------------------------
    UARTWriteByte((header0 >> 4) + '0');
    UARTWriteByte((header0 & 0x0F) + '0');
    // ------- 3rd byte 0x00 (delimiter) -------------------------
    UARTWriteByte('0');
    UARTWriteByte('0');                 //
    // ------- 4th byte = bat_voltage1 -------------------------
    UARTWriteByte((bat_voltage1 >> 4) + '0');
    UARTWriteByte((bat_voltage1 & 0x0F) + '0');
    // ------- 5th byte = bat_voltage0 -------------------------
    UARTWriteByte((bat_voltage0 >> 4) + '0');
    UARTWriteByte((bat_voltage0 & 0x0F) + '0');
    // ------- 6th byte = 0x00 (delimiter) -------------------------
    UARTWriteByte('0');
    UARTWriteByte('0');
    // ------- 7th byte = panel_voltage1 -------------------------
    UARTWriteByte((panel_voltage1 >> 4) + '0');
    UARTWriteByte((panel_voltage1 & 0x0F) + '0');   
    // ------- 8th byte = panel_voltage1 -------------------------
    UARTWriteByte((panel_voltage0 >> 4) + '0');
    UARTWriteByte((panel_voltage0 & 0x0F) + '0');
    // ------- 9th byte = 0x00 (delimiter) -------------------------
    UARTWriteByte('0');
    UARTWriteByte('0');
    // ------- 10th byte = temperature -------------------------
    UARTWriteByte((temp_BCD >> 4) + '0');
    UARTWriteByte((temp_BCD & 0x0F) + '0');
    
    // message end
    
    UARTWriteByte(',');     // ASCII code = 0x2C
    UARTWriteByte('0');     // ASCII code = 0x30
    UARTWriteByte(0x0D);    // Cariage Return: ASCII code = 0x0D
}

//void send_to_module(UINT8_T *to_send_pointer)           // increment byte in BCD format
//{
//    UARTWriteByte((*to_send_pointer >> 4) + '0');         // transmit high nibble in ASCII format
//    UARTWriteByte((*to_send_pointer & 0x0F) + '0');     // transmit low nibble in ASCII format
//}