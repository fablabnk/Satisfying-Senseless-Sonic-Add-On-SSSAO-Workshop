# Supercon 8 2024 Badge Hack

![Supercon 8 Badge](https://raw.githubusercontent.com/MakeItHackin/Supercon_8_2024_Badge_Hack/refs/heads/main/images/connectingWithFriends.png)

Welcome to the **Supercon 8 2024 Badge Hack** project! This repository contains the Micropython code developed for the Supercon 8 conference badge, demonstrated in Pasadena, CA from November 1-3, 2024. The badge, featuring the Raspberry Pi Pico Wireless, incorporates multiple Simple Add-Ons (SAOs) to enhance functionality and interactivity.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Hardware Components](#hardware-components)
- [Software Components](#software-components)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Credits](#credits)
- [License](#license)
- [References](#references)

## Project Overview

The **Supercon 8 2024 Badge** is a customizable and interactive badge designed for conference attendees. Powered by the Raspberry Pi Pico Wireless, the badge offers wireless capabilities and multiple ports for connecting various SAOs. These add-ons provide additional functionalities such as displays, sensors, lighting effects, and more, creating a dynamic and engaging experience for users.

### Key Highlights

- **Raspberry Pi Pico Wireless**: Acts as the central controller with wireless communication capabilities.
- **Six Ports**: Facilitate the connection of Simple Add-Ons (SAOs) for extended functionalities.
- **Dual I2C Buses**: Ports 1-3 operate on `I2C0`, and ports 4-6 on `I2C1`.
- **Integrated SAOs**: Six diverse SAOs enhance the badge with features like displays, touch controls, lighting, and event scheduling.

## Features

- **Interactive Display**: OLED display for information and animations.
- **Touch Controls**: Touchwheel SAO for intuitive user interactions.
- **Lighting Effects**: NeoPixels for customizable lighting and animations.
- **Event Scheduling**: Schedule SAO to display event timings and details.
- **Custom Drawings**: Etch SAO-Sketch for creative sketches and designs.
- **Classic Aesthetics**: MacSAO emulates the look and feel of classic Macintosh interfaces.
- **Notifications**: Skull of Fate SAO for themed alerts and messages.
- **Wireless Communication**: Seamless interaction between SAOs and the central controller.

## Hardware Components

- **Raspberry Pi Pico Wireless**: The main microcontroller unit powering the badge.
- **Six Ports**: Enable the connection of various SAOs.
  - **Ports 1-3**: Operate on `I2C0`.
  - **Ports 4-6**: Operate on `I2C1`.
- **Simple Add-Ons (SAOs)**: Enhance the badge with additional features.

### Connected SAOs

1. **Skull of Fate SAO**
   - **Creators**: p1x317h13f and MakeItHackin
   - **Description**: Themed alert system for displaying messages.
   - **Project Link**: [Skull of Fate](https://hackaday.io/project/198974-skull-of-fate-sao)

2. **Etch SAO-Sketch**
   - **Creator**: Andy Geppert
   - **Description**: Allows users to create sketches and drawings on the badge.
   - **Project Link**: [Etch SAO-Sketch](https://hackaday.io/project/197581-etch-sao-sketch)

3. **Touchwheel SAO**
   - **Creator**: Todbot
   - **Description**: Intuitive touch-based control interface.
   - **Project Link**: [Touchwheel SAO](https://github.com/todbot/TouchwheelSAO?tab=readme-ov-file)

4. **BlinkyLoop SAO**
   - **Creator**: Flummer
   - **Description**: Dynamic lighting effects using NeoPixels.
   - **Project Link**: [BlinkyLoop SAO](https://hackaday.io/project/198163-blinky-loop-sao)

5. **The Schedule SAO**
   - **Creator**: DaveDarko
   - **Description**: Displays event schedules and countdowns.
   - **Project Link**: [The Schedule SAO](https://hackaday.io/project/198229-the-schedule-sao)

6. **MacSAO**
   - **Creator**: SirCastor
   - **Description**: Emulates classic Macintosh interface aesthetics.
   - **Project Link**: [MacSAO](https://hackaday.io/project/196403-macintosh-sao)

## Software Components

- **Micropython**: The programming language used for developing the badge's firmware.
- **Libraries**:
  - `machine`: For hardware interactions.
  - `ssd1306`: For OLED display control.
  - `neopixel`: For NeoPixel LED control.
  - `etch`: For Etch SAO-Sketch functionalities.

## Installation

### Prerequisites

- **Hardware**:
  - Raspberry Pi Pico Wireless
  - Supercon 8 Badge
  - Compatible SAOs (as listed above)
- **Software**:
  - Micropython firmware installed on Raspberry Pi Pico Wireless
  - USB cable for programming
  - [Thonny IDE](https://thonny.org/) or any compatible Micropython IDE

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MakeItHackin/Supercon_8_2024_Badge_Hack.git
   cd Supercon_8_2024_Badge_Hack
   ```

2. **Connect Raspberry Pi Pico Wireless**

   - Connect the Pico to your computer via USB.
   - Ensure it's in bootloader mode for firmware updates if necessary.

3. **Upload the Firmware**

   - Open Thonny IDE.
   - Select the Raspberry Pi Pico as the interpreter.
   - Open `ConnectingWithFriends.py` from the cloned repository.
   - Save the script to the Pico.

4. **Install Required Libraries**

   - Ensure all necessary libraries (`ssd1306`, `neopixel`, `etch`, etc.) are available on the Pico.
   - You can upload them similarly via Thonny or include them in the repository.

5. **Connect SAOs**

   - Attach the desired SAOs to the badge ports.
   - Ensure each SAO is connected to the correct port (1-3 on `I2C0`, 4-6 on `I2C1`).

6. **Power On the Badge**

   - Once all connections are secure, power on the badge.
   - The boot LED should illuminate, indicating successful startup.

## Usage

Upon powering the badge:

- **Main Menu**: Navigate using the buttons to select different functionalities such as I2C device detection, event display, or the Pong animation.
- **I2C Detection**: Scan and display connected SAOs with detailed information.
- **Event Display**: View scheduled events with countdown timers.
- **Pong Animation**: Enjoy a dynamic screensaver featuring moving circles and rectangles.

### Controls

- **Button A**: Navigate through menu options.
- **Button B**: Select or confirm a menu option.
- **Button C**: Return to the main menu or previous menu.

### Touchwheel

- Interact with the touchwheel SAO for additional control inputs and RGB color settings.

### NeoPixels

- Experience customizable lighting effects and animations through the BlinkyLoop SAO.

## Contributing

Contributions are welcome! If you have suggestions, improvements, or wish to add new features, please follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

   - Provide a detailed description of your changes.

## Credits

This project was collaboratively developed by:

- **MakeItHackin**
- **CodeAllNight**
- **Danner**


## License

This project is licensed under the [MIT License](LICENSE).

