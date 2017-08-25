//----------------------------------------------------------------------------
//-- Ejemplo de uso del receptor serie
//-- Se hace eco de todos los caracteres recibidos. Ademas los 4 bits menos
//-- significativos se sacan por los leds de la IceStick
//----------------------------------------------------------------------------
//-- (C) BQ. October 2015. Written by Juan Gonzalez (Obijuan)
//-- GPL license
//----------------------------------------------------------------------------
//-- Comprobado su funcionamiento a todas las velocidades estandares:
//-- 300, 600, 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200
//----------------------------------------------------------------------------

`default_nettype none

`include "baudgen.vh"

//-- Top design
module echo(input wire clk,         //-- Reloj del sistema
            input wire rx,          //-- Linea de recepcion serie
            output wire tx,          //-- Linea de transmision serie
            output reg [3:0] leds,  //-- 4 leds rojos
            output wire act       //-- Led de actividad (verde)
            );

//-- Parametro: Velocidad de transmision
localparam BAUD = `B115200;

//-- Señal de dato recibido
wire rcv;

//-- Datos recibidos
wire [7:0] rxdata;
wire [7:0] txdata;

//-- Señal de reset
reg rstn = 0;

reg [15:0] count;

//-- Señal de transmisor listo
wire ready;
wire logic_ce;
//-- Inicializador
always @(posedge clk)
  rstn <= 1;

//-- Instanciar la unidad de recepcion
uart_rx RX0 (.clk(clk),      //-- Reloj del sistema
       .rstn(rstn),    //-- Señal de reset
       .rx(rx),        //-- Linea de recepción de datos serie
       .rcv(rcv),      //-- Señal de dato recibido
       .data(rxdata)     //-- Datos recibidos
      );

//-- Instanciar la unidad de transmision
uart_tx TX0 ( .clk(clk),        //-- Reloj del sistema
         .rstn(rstn),     //-- Reset global (activo nivel bajo)
         .start(tx_strb),     //-- Comienzo de transmision
         .data(txdata),     //-- Dato a transmitir
         .tx(tx),         //-- Salida de datos serie (hacia el PC)
         .ready(ready)    //-- Transmisor listo / ocupado
       );

wire tx_strb;

always @(posedge clk)
    logic_ce <= (rcv)&&(rxdata == 8'h00);

always @(posedge clk)
    if (logic_ce)
    begin
        count <= count + 1;
        leds <= leds + 1;
    end

always @(posedge clk)
    if (rcv)
    begin
        tx_strb <= 1'b1;
        case(rxdata)
            8'h00: txdata <= 8'h00;
            8'h01: txdata <= leds;
            8'h02: txdata <= count;
            default: txdata <= 8'h00;
        endcase
    end else
        tx_strb <= 1'b0;

endmodule
