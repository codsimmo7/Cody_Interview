# Welcome to StackEdit!

This is the README.md file for Codys interview. Included are install instructions, project layout, and some design decisions and further explanations. Thanks for taking the time to go over this project.

## Files
- install_program.py: This file creates and activates a virtual environment and installs the required packages from requirements.txt
- requirements.txt: This file holds the package names required to be installed in the virtual environment
- Interview_dataset.json: The input file provided for running the program against
- main.py: The program that does the json validation against the Interview_dataset.json file

## Generated Files
- A folder will get generated after running "install_program.py" with the name of the virtual environment which is hard-coded in the codebase.
- output.json: This file contains the records which passed the validation rules. This file only gets created if there were no errors in the entire json dataset.
- 

## Install instructions
Prerequisites: 
- Access to GitHub
- Means to clone the Git project either manually via www.github.com or the git CLI.
- Python3 installed on your machine. This project was developed using Python 3.11.7 for reference.
- A command-line interpreter for executing the code.
- Python.exe is added to your system path so that the command "python" evaluates correctly.

This code is intended to be cloned from a git repository. Once cloned, follow the steps below:
1) Ensure that you are running all commands when your current directory is the same as the project folder.
2) Simply run "python install_program.py"

## Design decisions
Overall, this was a tough project, but a fun challenge. I had actually never worked with Pydantic before so this was a pretty big learning curve. I found their documentation on their website is not the most concise given its examples, as they have almost no commentary around what their examples do, and there appears to be a lot. There also isn't a lot of google help regarding Pydantic v2 (which is what I used) so trying to use some reference examples from the old v1 syntax proved difficult.

**About the install_program.py:**
I began by of course, analyzing the requirements document which were pretty straight forward and easy to understand. I knew I would first need to import the Pydantic package, which meant I also knew I would need to consider a requirements.txt file. This of course meant I needed to also consider having some sort of installation or setup script involved, hence the install_program.py file.
I have actually never used a requirements.txt file personally, so I may have gone a little overboard with a custom python script for the setup. I see there is a setup.py file which using some configurations in the file, and after running "python install -e ." that it will do what my script did essentially. However, I didn't want to rely on the user to have to run the command, I figured I would go a little extra and show the skills I have creating virtual environments, and determining things like if the OS is Windows or not.

**About the main.py:**
I went back and forth on if I wanted to keep the code separate from the execution, and normally I would do so, but because this is a small example project, I decided to forgo that and keep the two combined. Normally I would take whatever is in the "def main()" section and extrapolate that to a second "run_program.py" script which would import the code as a package from a sub-folder within the project. But to keep things as simple as possible for the user, I kept these two together in one executable script.

The first thing I wanted to do was establish a printing format to make the standard out consistent in the type of logging that is occurring. I simply establish a format of "current_timestamp\tCodys interview -" with the intent of being followed up by a "SUCCESS, INFO, or ERROR" message during the important parts of the program. In most cases I like to setup a logger using the logging library initialized in a class, but that requires yet another file to produced which I thought would be overkill for this effort, and decided that printing to the standard out was sufficient.

With any Pydantic setup, you must first establish some class using Pydantic.BaseModel, and define what the structure is supposed to look like. I simply defined each column, the column type, and set the description, date_opened, and date_closed as Optional values, since the input file showed that in some cases they are blank ("", or null). Next, I set out to tackle defining custom validators, and using Pydantics documentation, I saw that this is done by the "@" decorator. I considered the validation setup on a rule by rule basis (one function for each rule type). This allows the business rules to be contained within a modifiable method that can simply be changed by changing the method alone. As far as which decorator to use (@field_validator, @model_validator etc) depended on if the requirement needed to analyze more than one condition on a column at one time.

For example, the method "validate_status_dates" uses the @model_validator while the rest of the rules use @field_validator because the rules has to check both the value of status AND date_closed/date_open at the same time. But the method "convert_null_str" uses @field_validator because a single condition is needed to be checked. This includes even if the one condition is checked against multiple keys/columns. I also chose to include an extra validation that was not in the requirements in the "validate_status" method which simply checks for valid domain values within a list of "OPEN,CLOSED,BOTH" to show that other considerations were taken. I could have also done even more by making sure the date fields were in the proper format, but thought the example of checking the status domain values already demonstrated ways of thinking more in depth about the requirements.

The hardest part of this entire effort that took me the longest was on the requirement to check for unique ids across the entire dataset. Every time I attempted to setup some kind of decorator (even trying the built in @root_validator, I kept running into an issue where Pydantic wants to finish the validation for each element and move on. This meant that each time I wanted to back reference some kind of list, I needed to perhaps attempt to reference a class variable within the decorator, and I just could not get it to work after hours or trying. I would either get an error about an integer object not being iterable, or a ModuleAttribute cant be referenced. If you notice for example in each method there is a "cls,value" as inputs to the method. Python didn't like when I tried cls.__some_variable where __some_variable was defined within the JsonModel class.

It may have been the way I was handling the loop to read each element regarding my validators, but I chose to make it evaluate record by record (or json object by json object in the array from the input) because of the requirement specifically asking about comparing status and the date columns. I knew I would have to do a validation both on a record by record basis, and across the whole set with the unique_id. I therefor chose to perform the check after Pydantics validators, and created my own extrapolation list of each id as it was read into the program. I simply checked if if in unique_list, and if not append it and continue. Then when the next record is read in, after performing the custom validations, the next id would get checked against the list, and if existed, the code would fail. Lastly, I decided to not write records that had passed validation to the output.json file. This was because I didn't want the user to think his final file was "complete" as it would only contain some of the total number of records. Unless he were to check a log file for logged errors, or see the standard out of the program (unlikely), he might assume everything was fine and the post-process procedure could suffer not having all records. Therefore, I thought it best to fail the entire code when any record had an error. This may not be suitable if the dataset is large however.

This of course leads to the question about if the dataset was much larger. If dealing with larger datasets, loading all of the JSON file into memory can be an issue. Using streaming processing libraries such as jsonlines allows for reading of the file incrementally instead. I have never personally used jsonlines before, however, but am aware of it.
Other considerations around file size include:
- batch processing: processing the json in smaller batches if streaming isn't feasible
- parallel processing: I am not too familiar with python libraries for concurrent processing but I am sure there are some.
- Creating an index structure for the JSON for columns like "id"
- Using faster JSON encoding libraries that exist
- Compressing the JSON file (however decompressing the file for processing could result in worse numbers)

The bullet points aforementioned, can also be applied if the source was an API or multiple files.  The files and or API data still needed to first be loaded to memory to which I could consider again streaming, parallel processing or batch processing as an example. If its coming from a database, choosing to optimize the query to only return the results that are needed, using ETL processes such as trigger tables, adding larger warehouses if its an MPP database, or if not writing the results to multiple files and again doing concurrent processing or batch depending on the use case.

Regarding the unit tests, I apologize but I do not have the time to code a unit testing framework or script. My pseudo-code however, involves the following:
	
    requirment1_fail = [{dict1}.{dict2}] # dict1 and dict2 both have a duplicate "id" value.
    	requirement1_pass = [{dict1},{dict2}] #dict 1 and dict2 have different "id" values.
    	requirement2_fail = (the failed json data for requirement2)
    	requirement2_pass = (the passed json data for requirement2)
    	.....
    	
    	def test_failed(file,expected_result):
    		file  = pathlib.Path(file)
    		with  open(file) as  f:
		    	input_data  =  f.read()
			assert process_input(input_data) !=  expected_results
			
		def test_passed(file,expected_result):
			file = pathlib.Path(file)
			with open(file) as f:
				intput_data = f.read()
			assert process_input(input_data) == expected_results

		main():
		test1 = test_failed("path/to/file.txt",requirement1_fail)
		test2 = test_passed("path/to/file.txt",requirement1_pass)
		....
		if any_tests_failed:
			print("some error")

