# logisim-discrete-CPU

![The CPU](https://i.imgur.com/aIL39s7.png)

This project aims to mimic [Ben Eater's 8-Bit CPU Project](https://eater.net/8bit), in the Digital Logic Simulator Logisim Evolution.

**Note:** *This project was developed in [Logisim Evolution v2.14.6](https://github.com/logisim-evolution/logisim-evolution/releases/tag/v2.14.6), and has only been tested on that version. Any other versions may break the project due to missing or differently sized circuit components.*

A full writeup/guide to replicate this project yourself from scratch may be found in the `CPU v1.XX.pdf` file in the root of this repository.

As Logisim doesn't support [VHDL](https://en.wikipedia.org/wiki/VHDL) modelling of components, each individual component and IC used by Ben has been built purely from discrete logic using Logisim's inbuilt logic gates, tri-state buffers, inputs and outputs.

The discrete implementations have been carefully designed to mirror the near exact operation of the corresponding ICs, to allow physical breadboarding and construction if desired. Most are based on the 7400 Series, as used by Ben. The `CPU.circ` file is intended to be loaded by [Logisim Evolution](https://github.com/reds-heig/logisim-evolution), as it uses push buttons and a couple of other features not found in the original Logisim program.

The pseudo-[28C16](http://cva.stanford.edu/classes/cs99s/datasheets/at28c16.pdf) (2K x 8-Bit ROM) used for the control logic (and output register display driver) is an exception to the discrete logic designs, due to its size. **Note** - The Control Logic ROM is pre-loaded with the correct microinstructions for the CPU, which mirrors the list of Ben Eater's (and uses the same microinstructions to achieve them). These are provided in `CPU Instructions.txt`. Logisim's ROM component is used instead, which is handy in allowing the loading of ROM image files. 

To that end, a Python 3 'helper' program was written to allow a CSV file of sequential binary instructions to be parsed and converted into a Logisim ROM image file, to be loaded into a ROM component for fast programming of the discrete RAM. This makes writing programs for the CPU much quicker. The utility is named genROM and is run from the command line with the following usage:

`> python genROM.py CSV ADDR WIDTH`

Where:

`CSV = Path to input CSV file (without any headers)`
`ADDR = Amount of ROM address lines (note - not total cells)`
`WIDTH = Bit width of each ROM cell`

The ADDR and WIDTH arguments are variable, in the case that the system is extended beyond the scope of this project and the available memory increased. The CSV content passed to the utility should simply look like this example:

`10010001, 11100001, 11011001, 00110111...`

Each representing a full instruction (opcode & operand) in binary. If too many values are supplied for the given ROM dimensions, or a value too large is supplied, the error will be caught and the user notified.

Once produced, the ROM image file can be loaded into the 'RAM Programmer' subcircuit by right clicking on the ROM component, and choosing `Load Image...`:

![Loading the ROM](https://i.imgur.com/AEo5FPI.png)

Then, inside the main CPU circuit (after pulsing the `RESET` input, which needs to be done every time the CPU simulation is reset to initialise the internal registers), the `PROG_RAM` input can be activated, and the `COMMIT` and `STEP`  push buttons can be toggled sequentially to `COMMIT` each instruction to the RAM's memory, and `STEP` to the next address in the ROM Programmer's (and RAM's) memory ready to repeat:

![Loading the RAM](https://i.imgur.com/vtcvBFd.png)

This can be repeated until all desired RAM locations are filled with instructions. When done, simply the `PROG_RAM` input can be returned to 0, `RESET` may be used again to reset the Program Counter to 0 (if not already there), and the Clock either manually stepped, or automatic Clock ticks enabled from the 'Simulate' Menu:

![Activating automatic Clock ticks](https://i.imgur.com/7l080oo.png)

'Tick Frequency' can also be altered, results may vary depending on your machine. Included in this project is a demo ROM image file, `Fib.ROM`, which computes the Fibonacci sequence from 0 to 233, then loops. `7Seg.ROM` and `BinaryToBCD.ROM` files are also included, which are pre-loaded into the ROMs used as the output display drivers. `controlROM.py` will generate the required control ROM file based on the microinstructions given within.

## Aims

The idea of this project is to present a full guide to build up to this project yourself, starting with only basic digital logic circuit knowledge. Please log any issues, and let me know if you'd like to use this project and/or build manual for anything cool! Forks are welcomed to build on and expand this system to bigger and better things, but it's encouraged to use as much discrete logic as possible! 

# Todo

 - Fix `HLT` microinstruction, as Logisim currently doesn't play nice with it
 - Implement an optional Clock cycle saving subcircuit to skip to the Instruction if the current control word == 0
 - Split the subcircuits into a Logisim library to be loaded inside other Logisim circuits
