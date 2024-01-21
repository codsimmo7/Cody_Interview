from pydantic import BaseModel, ValidationError, model_validator, validator, root_validator, field_validator
import json
from typing import Optional
from datetime import datetime
import os

# THIS CODE IS INTENDED TO BE RUN FROM THE SAME PROJECT DIRECTORY IN WHICH IS WAS CLONED FROM GIT
# This is because it uses os.getcwd(). Usage: "python .\main.py"

#-------------------------------#
# print formatting method       #
#-------------------------------#
def log_fmt():
    msg = f"{datetime.now()}\tCodys interview -"
    return msg

#-------------------------------#
#                               #
# Script Classes                #
#                               #
#-------------------------------#
class JsonModel(BaseModel):
    #--- This class defiend the Pydantic structure in which to validate against. It also sets validation rules
    # and constraints which to test against.
    id: int
    code: str
    description: Optional[str] = None
    status: str
    date_opened: Optional[str] = None
    date_closed: Optional[str] = None

    #--- Checks all str columns are set to "None" or effectively, null.
    @field_validator("code","description", "status","date_opened","date_closed")
    def convert_null_str(cls, value):
        return None if value == "" else value

    #### Mention how you added this extra check 
    #--- Checks that the "status" column only has values "OPEN","CLOSED", or "BOTH"
    @field_validator("status")
    def validate_status(cls, value):
        allowed_statuses = {'OPEN', 'CLOSED', 'BOTH'}
        if value not in allowed_statuses:
            raise ValueError(f"{log_fmt()} ERROR: Invalid status {value}. Allowed values are {allowed_statuses}")
        return value

    #--- model_validator is used to check one property against another of the class. This allows us to check values
    # between the "status" column, and "data_opened" or "date_closed" in a case like statement.
    @model_validator(mode='before')
    def validate_status_dates(cls, values):
        status = values.get("status")
        date_opened = values.get("date_opened")
        date_closed = values.get("date_closed")
        if status == "OPEN" and date_opened is None:
            raise ValueError(f"{log_fmt()} ERROR: date_opened must be populated when status is 'OPENED'")
        elif status == "CLOSED" and date_closed is None:
            raise ValueError(f"{log_fmt()} ERROR: date_closed must be populated when status is 'CLOSED'")
        elif status == "BOTH" and (date_opened is None or date_closed is None):
            raise ValueError(f"{log_fmt()} ERROR: Both date_opened and date_closed must be populated when status is 'BOTH'")
        return values

#-------------------------------#
#                               #
# Script Methods                #
#                               #
#-------------------------------#
def process_input(input_file: str, output_file: str):
    #--- This method does the following:
    # Validation occurs on a element level: All validators are run against one array item at a time before going to the next array item...
    # 1) Opens the input json file and creates an object out of it
    # 2) Pass the json object into the JsonModel class which runs the various custom defined pydantic validations against each element in the list of objects.
    #   2a) If there were errors from the pydantic rules, print the record that failed and why.
    #   2b) If no errors occurred, check if the current record has already been processed based on the id value.
    # 3) Write the valid records to a new-line delimited output file, ONLY if no errors occurred.

    validated_data = []

    with open(input_file, 'r') as f:
        json_data = json.load(f)

    # Perform a unique "id" value check after running the pydantic validations. If no failures, write the output to a new line delimited file.
    unique_id_list = []
    for json_object in json_data:
        try:
            instance = JsonModel(**json_object)
            model = instance.model_dump()
            # 
        except ValidationError as e:
            raise ValueError(f"{log_fmt()} ERROR: Validation error for record {json_object}: {e}")
        else:
            id = model["id"]
            if id in unique_id_list:
                raise ValueError(f"{log_fmt()} ERROR: Validation error for record {json_object}: \n The id value '{id} is not unique in the dataset!")
            else:
                unique_id_list.append(id)
                validated_data.append(model)
                
    with open(output_file, 'w') as f:
        for item in validated_data:
            f.write(json.dumps(item) + '\n')
#-------------------------------#
#                               #
# Main Execution                #
#                               #
#-------------------------------#
def main():
    project_path = os.path.join(os.getcwd())
    input_file = os.path.join(project_path,r"Interview_dataset.json")
    output_file = os.path.join(project_path, r"output.json")
    if os.path.exists(input_file):
        print(f"{log_fmt()} INFO: Running custom validation checks against {input_file}")
        try:
            process_input(input_file, output_file)
            print(f"{log_fmt()} SUCCESS! No validation errors occured.")
            print(f"{log_fmt()} INFO: The validated records can be found in the file: {output_file}")
        except ValueError as ve:
            print(f"{log_fmt()} ERROR: There was a problem validating the JSON file. Error message: {ve}")
    else:
        print(f"{log_fmt()} ERROR: No input file exists! Please make sure the input_file variable is declared.")

if __name__ == "__main__":
    main()