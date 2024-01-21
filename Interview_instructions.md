# Takehome

Given the attached json file, please create a script that does the following:
* Reads the json file
* Puts the json object into a Pydantic Model representation of the data structure
* Writes the output to a new-line delimited json file

## Validations
In addition to the following above, please note that your script should also validate that the following business logic conditions are met:
* If the object's status is `OPENED`, the `date_opened` field must be populated
* If the object's status is `CLOSED`, the `date_closed` field must be populated
* If the object's status is `BOTH`, both `date_opened` and `date_closed` must be populated
* The `id` field must be unique across the dataset
* String fields should have empty strings converted into a null value

If any of the above are violated, an exception should be raised indicating which record caused the issue alongside the content of the record

## Take Home Requirements
While the problem space is limited, please write this code as if it were code you'd contribute in this role. In addition to building a working version of the problem described above, please also provide the following:
* An explanation of design decisions you made and why
* How, if at all, your design decisions would change knowing the input dataset got much larger
* How, if at all, your design decisions would change knowing the input source were to change from a flat file to:
  * A 3rd party API
  * Multiple files (e.g. part-1, part-2, ...)
  * Database table

* Add tests

## Submission
Please create a public repository in your choice of hosted git providers (github, gitlab, bitbucket) and upload your solution there. Please send the link of the repository to `alex.cano@iscmga.com` as well as a document containing the design decision explanations.

Code sent directly or via zip files will be rejected.

## Questions
If any part of this assignment is unclear, please do not hesitate to reach out to me at `alex.cano@iscmga.com` with clarifying questions.