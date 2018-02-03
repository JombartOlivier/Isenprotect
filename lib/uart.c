#include <stdio.h>
#include <unistd.h>			//Used for UART
#include <fcntl.h>			//Used for UART
#include <termios.h>		//Used for UART
#include <ncurses.h>

int sendData(int uartFile, unsigned char *tx_buffer, int tx_length);
int UARTInit(int mode);
void UARTClean(int uartFileRef);
unsigned char* receiveData(int uartFileRef);

#define COMWITHGPS 0
#define COMWITHSIGFOX 1


/**********************************************************************************************
*
*                                      UARTInit
*                    This function is use to initialize the UART Bus
*
***********************************************************************************************/ 
int UARTInit(int mode){
    int uartFileRef = -1;

    //OPEN THE UART
	    //The flags (defined in fcntl.h):
	    //	Access modes (use 1 of these):
        //		O_RDONLY - Open for reading only.
        //		O_RDWR - Open for reading and writing.
        //		O_WRONLY - Open for writing only.
        //
        //	O_NDELAY / O_NONBLOCK (same function) - Enables nonblocking mode. When set read requests on the file can return immediately with a failure status
        //											if there is no input immediately available (instead of blocking). Likewise, write requests can also return
        //											immediately with a failure status if the output can't be written immediately.
        //
        //	O_NOCTTY - When set and path identifies a terminal device, open() shall not cause the terminal device to become the controlling terminal for the process.

	uartFileRef = open("/dev/ttyAMA0", O_RDWR | O_NOCTTY | O_NDELAY);		//Open in non blocking read/write mode

	if (uartFileRef == -1){
		printf("Error - Unable to open UART.  Ensure it is not in use by another application\n");
	}
	
	//CONFIGURE THE UART
	//The flags (defined in /usr/include/termios.h - see http://pubs.opengroup.org/onlinepubs/007908799/xsh/termios.h.html):
	//	Baud rate:- B1200, B2400, B4800, B9600, B19200, B38400, B57600, B115200, B230400, B460800, B500000, B576000, B921600, B1000000, B1152000, B1500000, B2000000, B2500000, B3000000, B3500000, B4000000
	//	CSIZE:- CS5, CS6, CS7, CS8
	//	CLOCAL - Ignore modem status lines
	//	CREAD - Enable receiver
	//	IGNPAR = Ignore characters with parity errors
	//	ICRNL - Map CR to NL on input (Use for ASCII comms where you want to auto correct end of line characters - don't use for bianry comms!)
	//	PARENB - Parity enable
	//	PARODD - Odd parity (else even)

	struct termios options;
	tcgetattr(uartFileRef, &options);
	options.c_iflag = IGNPAR;
	options.c_oflag = 0;
	options.c_lflag = 0;
    if(mode == COMWITHGPS){
        options.c_cflag = B9600 | CS8 | CLOCAL | CREAD;		//<Set baud rate
    }
    else if(mode == COMWITHSIGFOX){
        options.c_cflag = B115200 | CS8 | CLOCAL | CREAD;		//<Set baud rate
    }
    else{
        printf("Error, unreconised option");
        uartFileRef = -1;
    }

	tcflush(uartFileRef, TCIFLUSH);
	tcsetattr(uartFileRef, TCSANOW, &options);
    return uartFileRef;
}

/**********************************************************************************************
*
*                                      UARTClean
*                       This function is use to free the UART Bus
*
***********************************************************************************************/ 
void UARTClean(int uartFileRef){
    close(uartFileRef);
    printf("file reference closed\n");
}

/**********************************************************************************************
*
*                                      receiveData
*                   This function is use to read data on the UART bus
*
***********************************************************************************************/ 
unsigned char* receiveData(int uartFileRef){
	//printf("UART file ? : %i\n",uartFileRef);

   //----- CHECK FOR ANY RX BYTES -----
	if (uartFileRef != -1){
		// Read up to 255 characters from the port if they are there
		unsigned char rx_buffer[256];
		int rx_length = 0;
        printf("waiting data\n");
		while(rx_length == 0){
			rx_length = read(uartFileRef, (void*)rx_buffer, 255);
		}

		//printf("Rx_length : %i\n",rx_length);
		if (rx_length < 0){
            printf("Error, failed to recevie data%s\n");
		    return "-1";  //An error occured (will occur if there are no bytes)
		}

		else{
			//Bytes received
			rx_buffer[rx_length] = '\0';
			printf("%i bytes read : %s\n", rx_length, rx_buffer);
            return *rx_buffer;
		}
	}
}

/**********************************************************************************************
*
*                                      sendData
*                   This function is use to send data on the UART bus
*
***********************************************************************************************/ 
int sendData(int uartFile, unsigned char *tx_buffer, int tx_length){

	
	if (uartFile != -1){

		int count = write(uartFile, &tx_buffer[0], tx_length);		//Filestream, bytes to write, number of bytes to write
		//printf("Data : %s\n",&tx_buffer);
		//printf("Data send ? : %i\n",count);
		if (count < 0){

			printf("UART TX error\n");
            return -1;
		}
        else{
            printf("Data sent\n");
            return 0;
        }
	}
    else{
        printf("UART TX error\n");
        return -1;
    }
}

int main(){
unsigned char p_tx_buffer[5];
	 p_tx_buffer[0] = 'H';
	 p_tx_buffer[1] = 'e';
	 p_tx_buffer[2] = 'l';
	 p_tx_buffer[3] = 'l';
	 p_tx_buffer[4] = 'o';
    int uartFileRef = UARTInit(COMWITHGPS);
    sendData(uartFileRef, p_tx_buffer, 5);
    unsigned char* data = receiveData(uartFileRef);
    int i = 0;
    while(&data != "\0"){
        printf("data received : %s\n", &data);
	i++;
    }
    UARTClean(uartFileRef);
}
