#include <stdio.h>
#include <unistd.h>			//Used for UART
#include <fcntl.h>			//Used for UART
#include <termios.h>		//Used for UART
#include <ncurses.h>
#include <string.h>

int UARTInit();
void UARTClean(int uartFile);
int sendByte(int uartFile, unsigned char* buffer, int bufferLength);
unsigned char receiveByte(int uartFile);

int UARTInit(){
    int uartFile = -1;

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

	uartFile = open("/dev/ttyAMA0", O_RDWR | O_NOCTTY | O_NONBLOCK);		//Open in non blocking read/write mode
	if (uartFile == -1)
	{
		//ERROR - CAN'T OPEN SERIAL PORT
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
	tcgetattr(uartFile, &options);
	options.c_cflag = B115200 | CS8 | CLOCAL | CREAD;		//<Set baud rate
	options.c_iflag = IGNPAR;
	options.c_oflag = 0;
	options.c_lflag = 0;
	tcflush(uartFile, TCIFLUSH);
	tcsetattr(uartFile, TCSANOW, &options);
    return uartFile;
}

void UARTClean(int uartFile){
    close(uartFile);
}

int sendByte(int uartFile, unsigned char* buffer, int bufferLength){
	
	if (uartFile != -1){

		int count = write(uartFile, buffer, bufferLength);		//Filestream, bytes to write, number of bytes to write
		printf("Data : %s\n", buffer);
		printf("Data send ? : %i\n", count);
		if (count < 0){

			printf("UART TX error\n");
            return -1;
		}
        else{
            return 0;
        }
	}

    else{
        printf("UART TX error\n");
        return -1;
    }
}

unsigned char receiveByte(int uartFile){
	printf("UART file ? : %i\n",uartFile);
   //----- CHECK FOR ANY RX BYTES -----
	if (uartFile != -1)
	{
		// Read up to 255 characters from the port if they are there
		unsigned char rx_buffer[256];
		int rx_length = 0;
		while(rx_length == 0){
			rx_length = read(uartFile, (void*)rx_buffer, 255);
		}

		printf("Rx_length : %i\n",rx_length);
		if (rx_length < 0)
		{
			//An error occured (will occur if there are no bytes)
		}
		else
		{
			//Bytes received
			rx_buffer[rx_length] = '\0';
			printf("%i bytes read : %s\n", rx_length, rx_buffer);
			return rx_buffer;		}
	}
}

int main(){
    int uartFile = -1;
	//unsigned char tx_buffer[20];
	unsigned char p_tx_buffer[6];
	unsigned char rxBuffer;
	/*p_tx_buffer = &tx_buffer[0];
	*p_tx_buffer++ = 'H';
	*p_tx_buffer++ = 'e';
	*p_tx_buffer++ = 'l';
	*p_tx_buffer++ = 'l';
	*p_tx_buffer++ = 'o';*/
	p_tx_buffer[0] = '1';
	p_tx_buffer[1] = '2';
	p_tx_buffer[2] = '3';
	p_tx_buffer[3] = '4';
	p_tx_buffer[4] = '5';
	p_tx_buffer[5] = '6';
    uartFile = UARTInit();
    sendByte(uartFile, p_tx_buffer, 6);
    rxBuffer = receiveByte(uartFile);
	printf('data : %s\n', rxBuffer);
	/*while(&rxBuffer != '/0'){
		printf('data : %c\n', &rxBuffer);
		*rxBuffer++;
	}*/
    /*while(receiveByte(uartFile) != -1 | receiveByte(uartFile) != 2){
	  debug = receiveByte(uartFile);
	  printf("boucle while : %s\n",debug); 
    }*/
    UARTClean(uartFile);
    printf("program finish\n");
}
