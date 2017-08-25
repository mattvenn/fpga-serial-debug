# Debugging FPGA designs via serial port 

After simulation, you may discover unexpected issues in your FPGA design when
it's running on the hardware. What if you could pause execution and examine
registers via the built in serial port?

This idea is from this [blog post by Dan
Gisselquist](http://zipcpu.com/blog/2017/05/26/simpledbg.html), who has many
more ideas on how to build even better debugging frameworks.

The serial port is from [Obijuan's open source verilog tutorial](https://github.com/Obijuan/open-fpga-verilog-tutorial/wiki/Cap%C3%ADtulo-25%3A-Unidad-de-recepci%C3%B3n-serie-as%C3%ADncrona)

Both resources are highly recommended!

The program is just 2 counters, a 4 bit counter is attached to the LEDs on the Icestick, and
the other is a 16 bit counter. Both advance one step every clock cycle.

The idea is to use the serial port as a way of sending control commands to the
FPGA. In this basic example we just have 3:

* take a step
* read the LED register
* read the count register (only bottom 8 bits are read)

Instead of putting the counter incrementers in an always block, they are wrapped
in clock enabled always block, so the counters only step when a 0x00 data block
is received:

    always @(posedge clk)
        logic_ce <= (rcv)&&(rxdata == 8'h00);

    always @(posedge clk)
        if (logic_ce)
        begin
            // put any logic you want to debug here
            count <= count + 1;
            leds <= leds + 1;
        end

We can also inspect the count and led registers:

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

A [python program](control.py) sends the messages and reads the results. As a bonus the
results are later [formatted into a VCD](convert_csv_to_vcd.py) file that can be
displayed with GTKWave.

# Instructions

## Requirements

* Icestick FPGA development board, but can easily work on any serial equipped
 dev board.
* The [IceStorm](http://www.clifford.at/icestorm/) open source synthesis suite from Clifford Wolf and others. 

## Build and program

    make sint2
    make prog

## Run the debugger

    make control

control.py sends the commands over serial to take 2000 steps, and reads the
results of the registers every step. The results are exported to dumpvar.csv

    make view

converts the dumpvar.csv file to a vcd then runs GTKWave to show the
results.

# Resources

* http://zipcpu.com/blog/2017/05/26/simpledbg.html
* https://github.com/Obijuan/open-fpga-verilog-tutorial/wiki/Cap%C3%ADtulo-25%3A-Unidad-de-recepci%C3%B3n-serie-as%C3%ADncrona

