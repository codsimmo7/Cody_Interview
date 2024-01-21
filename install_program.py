import os
import sys
import subprocess
from datetime import datetime

# THIS CODE IS INTENDED TO BE RUN FROM THE SAME PROJECT DIRECTORY IN WHICH IS WAS CLONED FROM GIT
# This is because it uses os.getcwd(). Usage: "python .\install_program.py"

#-------------------------------#
#                               #
# Script Classes                #
#                               #
#-------------------------------#
class installProject():
    #--- This class sets initial class variables that can be referenced in the rest of the project including the venv name
    # as well as the venv's Scripts directory
    def __init__(self):
        self.venv_name = "interview-cody-env"
        self.env_scripts = os.path.join(os.getcwd(),self.venv_name,r"Scripts")

    def create_virtualenv(self):
        #--- This function invokes python to try and create a virtual environment based on the class variable name "venv_name"
        print(f"{datetime.now()} Codys interview - INFO: Checking for venv '{self.venv_name}' and creating if it doesnt exist.")
        try:
            # Check if virtual environment exists
            subprocess.run(["python", "-m", "venv", self.venv_name], check=True)
        except subprocess.CalledProcessError:
            print(f"{datetime.now()} Codys interview - Error: Failed to create virtual environment '{self.venv_name}'")
            sys.exit(1)
        else:
            print(f"{datetime.now()} Codys interview - SUCCESS: Successfully created {self.venv_name}")

    def activate_virtualenv(self):
        #--- This function activates the venv, using logic based on the OS the user is executing from as the "source" operation is different.
        activate_script = os.path.join(os.getcwd(), self.venv_name, r"Scripts\activate") if sys.platform == "win32" else os.path.join(os.getcwd(), self.venv_name, "bin/activate")
        activate_path = os.path.join(self.venv_name, activate_script)
        activate_cmd = f"source {activate_path}" if sys.platform != "win32" else f"{activate_path}"
        print(f"{datetime.now()} Codys interview - INFO: Activating venv '{self.venv_name}'")
        subprocess.run(activate_cmd, shell=True, check=True)
        print(f"{datetime.now()} Codys interview - SUCCESS: Successfully activated '{self.venv_name}'")

    def install_requirements(self):
        #--- This function uses pip to install the provided requirements.txt file within the project.
        print(f"{datetime.now()} Codys interview - INFO: Installing requirements from requirements.txt")
        requirements_file = os.path.join(os.getcwd(),r"requirements.txt")
        try:
            subprocess.run([os.path.join(self.env_scripts, r"pip"), "install", "-r", requirements_file], check=True)
        except subprocess.CalledProcessError:
            print(f"{datetime.now()} Codys interview - Error: Failed to install requirements")
            sys.exit(1)
        else:
            print(f"{datetime.now()} Codys interview - SUCCESS: Succesfully installed requirements")
        
    def main(self):
        # Check if virtual environment exists, and create if not
        self.create_virtualenv()

        # Activate virtual environment
        self.activate_virtualenv()

        # Install requirements
        self.install_requirements()

        print(f"{datetime.now()} Codys interview - SUCCESS Setup completed successfully!")

if __name__ == "__main__":
    proj = installProject()
    proj.main()