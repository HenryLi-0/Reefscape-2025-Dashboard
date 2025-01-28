# Reefscape 2025 - 1155 Dashboard
An operator dashboard to control bits of FRC Team 1155's 2025 robot.

Big thanks to [wpilibsuite/StandaloneAppSamples](https://github.com/wpilibsuite/StandaloneAppSamples/tree/main) and [this CD post](https://www.chiefdelphi.com/t/problems-with-importing-wpilib-java/424464) for being starting points for the start of research for the Java version!

Also, thanks to [HenryLi-0/ivo](https://github.com/HenryLi-0/ivo/tree/main) for being the rendering system, which this dashboard uses a modified version of!

## Structure
The code is centered around [`subsystems/`](subsystems/). The NetworkTables system is in [`subsystems/comms.py`](</subsystems/comms.py>), while the interface is in [`interface.py`](</subsystems/interface.py>).

- `Main.java` loads the libraries, creates the Dashboard GUI, and runs the NetworkTable data.
- `Dashboard.java` consists of the Dashboard GUI.
- `Constants.java` consists of constants, which should be updated as necessary. `REAL` should be set

## Setup

See `requirements.txt` for modules to install.