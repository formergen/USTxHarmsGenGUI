
# OpenUtau USTx Auto Harmony Generator

## Description

This Python script is designed to automatically generate harmony parts for USTx files, a MIDI-like format used by OpenUtau and similar vocal synthesis software. It analyzes the notes in your USTx file, detects the key (major or minor), and creates new tracks with harmony notes (lower, upper, or both) based on a user-defined semitone interval.

This tool is helpful for:

*   Quickly creating backing vocals or harmonies for your songs in OpenUtau.
*   Experimenting with different harmony intervals and types.
*   Saving time by automating the process of manual harmony creation.

**Note:** The key detection and harmony generation algorithms are simplified and provide a starting point. For more sophisticated and musically advanced harmonies, further refinements (as outlined in the "Future Enhancements" section) would be beneficial.

## Features

*   **USTx File Format Support:** Reads and writes `.ustx` project files.
*   **Track Selection:** Allows you to choose specific tracks from your USTx project to generate harmonies for.
*   **Harmony Type Options:** Generates lower harmonies, upper harmonies, or both simultaneously.
*   **Key Detection (Major/Minor):**  Attempts to automatically detect the key (major or minor) of your music based on note frequencies.
*   **Manual Key Override:** Option to manually select the key (major or minor) if you prefer to override auto-detection.
*   **Scale-Aware Harmony Generation:**  Basic key correction ensures harmony notes generally stay within the detected major or minor scale.
*   **Customizable Interval:** User-defined semitone interval for harmony generation (e.g., 3 for a major third).
*   **User-Friendly Console Interface:**  Interactive command-line interface with colored text using `colorama` for better readability (especially on Windows).
*   **Automatic File Extension Handling:**  Automatically appends `.ustx` if you forget to include it in the input or output file paths.

## Installation

To use the OpenUtau USTx Auto Harmony Generator, you need to install Python and the required libraries. Follow these steps:

1.  **Install Python:**
    *   Ensure you have Python 3.x installed on your system. You can download the latest version from the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
    *   During the Python installation, **make sure to check the box "Add Python to PATH"** during the installation process. This is crucial for running Python and pip commands from your terminal or command prompt.

2.  **Install Required Libraries:**
    You can install the necessary Python libraries using either of the following methods:

    **Method 1: Using `pip install` command (Manual Installation)**

    *   Open your terminal or command prompt.
    *   Navigate to the directory where you saved the `main.py` script (and `requirements.txt` if provided). You can use the `cd` command to change directories.
    *   Run the following command to install the required libraries:

        ```bash
        pip install pyyaml colorama PyQt6
        ```

        This command will use `pip`, Python's package installer, to download and install `PyYAML`, `colorama`, and `PyQt6` libraries from the Python Package Index (PyPI).

    **Method 2: Using `requirements.txt` and `install.bat` (Automated Installation - Recommended for Windows)**

    *   **Ensure you have the `requirements.txt` and `install.bat` files** in the same directory as your `main.py` script. These files should be provided with the Harmony Generator.
    *   **Double-click the `install.bat` file.** This will open a command prompt window and automatically execute the installation process.
    *   The `install.bat` script will:
        *   **Check for Python and pip:** Verify if Python and `pip` are correctly installed and accessible in your system's PATH.
        *   **Update pip (optional but recommended):** Ensure you have the latest version of `pip`.
        *   **Install dependencies:** Use `pip` to install all the libraries listed in the `requirements.txt` file.
    *   **Wait for the script to finish.** It will display messages indicating the progress and success or failure of the installation. If successful, it will say "All dependencies were installed successfully!".

    **Explanation of `requirements.txt` and `install.bat`:**

    *   **`requirements.txt`:** This file is a list of Python libraries that the Harmony Generator needs to run. It simply contains the names of the packages: `PyYAML`, `colorama`, and `PyQt6`.
    *   **`install.bat`:** This is a batch script (for Windows) that automates the process of installing the libraries listed in `requirements.txt`. It's a convenient way to install all dependencies at once, especially for users who are not comfortable with manually using command-line `pip` commands.

3.  **Verify Installation (Optional):**

    *   After installation (using either method), you can verify if the libraries are installed correctly. Open a Python interpreter or run `python` in your terminal/command prompt and try to import the libraries:

        ```python
        import yaml
        import colorama
        from PyQt6.QtWidgets import QApplication
        print("Libraries installed successfully!")
        ```

        If you don't see any error messages when running this Python code, it means the libraries have been installed correctly.

Once you have completed these installation steps, you are ready to use the OpenUtau USTx Auto Harmony Generator! Proceed to the "Usage" section to learn how to run the script and generate harmonies.

## Usage

1.  **Open File** Run `run.bat` or `main.py`

2.  **Follow the prompts:** The script will guide you through the harmony generation process:

    *   **Enter the path to your USTx file:** Provide the path to the `.ustx` file you want to process.
    *   **Enter the path to output USTx file:** Provide the path to the output `.ustx` file.
    *   **Select track numbers:**  Choose the tracks for which you want to create harmonies.
    *   **Select harmony type:** Choose `Lower`, `Upper` or `Both` Harmonies mode.
    *   **Enter semitone interval:**  Input the semitone interval for the harmony (e.g., `3` for major third, `4` for major third, `7` for perfect fifth).
    *   **Run generator:** Click on `Generate Harmonies` button.
    *   
3.  **Import into OpenUtau:** Open the newly created `.ustx` file in OpenUtau. You will find new tracks added with the generated harmony parts.

## Limitations

*   **Simplified Key Detection:** The automatic key detection is based on statistical profiles and might not be perfect for all musical pieces, especially those with complex harmonies or key changes. Manual key selection is recommended for critical projects.
*   **Basic Harmony Generation:** The script generates parallel harmonies based on a fixed semitone interval. It does not yet implement more advanced harmony techniques like chord-based harmony, voice leading, or counterpoint.
*   **Key Correction is Basic:** The key correction attempts to keep harmony notes within the diatonic scale, but it's a simplified approach and might not always produce musically ideal results in all cases.
*   **Natural Minor Scale Only:** Minor key detection and harmony generation are currently based on the natural minor scale. Harmonic and melodic minor scales are not yet supported.

## Author

formergen(https://github.com/formergen)]

