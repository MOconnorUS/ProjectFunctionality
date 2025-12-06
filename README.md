# CSE 620 Final Project
# Leveraging ASP on Real-Time Market Data to Observe the Most Profitable Day
## Authors: Matthew O'Connor

# Project Summary
My CSE 620 final project leverages the Charles Schwab Datastream via their API. Real-time market data is stored into three excel files which can be found in Days. Each excel file (Day1, Day2, Day3) contain information pertaining to 11 companies. That information being the Bid Price, Ask Price, Bid Size, Ask Size, High Price, Low Price, and Close Price. This information is read line by line via the functions in `file_reader.py`. The information on each line is interpreted and the data is prepared in Answer Set Prolog (ASP) format via the functions within `asp_file_functions.py`. Once the information is formatted an ASP encoding is created via `asp_file_writer.py`, the ASP file can be found in ASP Encoding. After, the ASP file is run and the answer set is both parsed and interpreted via the functions within `asp_output_parsing.py`. Depending on the output from the ASP program information may be appended to our encoding along with the new information from the excel however it is possible nothing new will be added. Once the end of the excel is reached a profitable days worth of interactions will be produced and the profit of the day will be calculated and produced as well.

---
# Below will showcase how to clone the project, download Python, download ASP, setup your own virtual environment, and run the project

# How to clone a repository
*Please note this is only for Windows devices*
1. Download and install [Git](https://git-scm.com/install/windows)
2. Open Command prompt type `cmd` into the search bar on your windows device
3. Navigate to your the folder you wish to clone the repository in this can be done by typing `cd file_path_to_directory`
4. Click on the green code button on the repository shown in the image below  
![Green Code Button](/assets/images/code_button.PNG "Green Code Button")
5. Copy the github link provided in the drop down by clicking the button circled in the image below  
![Copy Clone URL](/assets/images/copy_clone.PNG "Copy Clone URL")
6. Type: git clone github_link *github_link is the url provided by github which can be pasted by right clicking on the command prompt*

# Download Python and add it to your PATH
1. Download and install [Python](https://www.python.org/downloads/)
**While downloading ensure you either add Python to your PATH or save the file location you downloaded it to**

If you did NOT add Python to your PATH do the following
1. Copy the file path to your Python installation
2. Edit your system environment variables by searching "Environment variables" in your windows search
3. Click environment variables as seen in the screenshot below
![Environment Variables](/assets/images/environment_variables.PNG "Environment Variables")
4. Select the Path under System Variables and edit it as seen in the screenshot below
![Edit Path](/assets/images/edit_path.PNG "Edit Path")
5. Select New and then paste your file pathing into the text field
6. Press "Ok" on all three open windows to close them
7. If you had a cmd window open, restart it

# Download ASP and add it to your PATH
1. Download [ASP](https://github.com/potassco/clingo/releases?page=2)
*I used the winzip from version 5.4.0*
**Follow the Python steps above to add ASP to your PATH**

# Setup your own virtual environment
1. Open a command prompt window by typing `cmd` into your windows search
2. Navigate into the directory where you cloned the GitHub project via `cd path_to_directory`
3. Type the following: `python -m venv virtual_env`
*You can name 'virtual_env' whatever you would like*
4. Once it finishes loading you need to activate the environment by typing the following: `cd virtual_env/scripts` followed by `activate`
5. Now that your environment is active type `cd ../..` to return to the project directory
6. Finally for this project you will want to install all necessary libraries which can be done via typing `setup.bat`

# How to run
If you have completed everything above then you are ready to run your project! To do so simply type the following into the cmd window: `python main.py` and when prompted to enter which day you wish to run enter either `one, two, or three`. The project should take a moment to run through entirely and when it is done the final encoding will be in the ASP Encoding folder. The profit of the day will be printed to the console as well as being at the bottom of the ASP encoding.
