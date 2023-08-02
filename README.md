# MedX: Medication Regimen Complexity Calculation Python Package
Developed by TIRI Lab @ JHU

#### Features

| Feature   Name                               | Description                                                                      | Input(s)                                                                                                                                                                                                                             | Output(s)                                                |
|----------------------------------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| Load File                                    | Read in data file with modifiable column name                                    | A file name for the input medication records list, a column name for patient identifier (optionally), a column name for medication name (optionally), a   column name for SIG (optionally), a column name for NDC code (optionally)  | An indicator showing whether the file loads successfully |
| Write file                                   | Write MRCI output to an output file with modifiable column name                  | A file name for the output file, a column name for patient identifier (optionally)                                                                                                                                                   | An indicator showing whether the file writes successfull |
| Customize Decision Keywords                  | Make modification of decision keyword list                                       | A file name for the  data file containing   the updated keywords, identifier of list need to be modified (A/B/C)                                                                                                                     | None                                                     |
| Calculate MRCI and MC (Single time point)    | Calculate MRCI score and MC from the data read in                                | Input data of medication list                                                                                                                                                                                                        | MRCI scores and MC at one time point                     |
| Calculate MRCI and MC (Multiple time points) | Calculate MRCI score and MC from the data read in when there are time identifier | Input data of medication list, column name for the time identifier                                                                                                                                                                   | MRCI scores and MC at multiple time points               |

#### Usage Guide

1. Download this repo using "Download ZIP" or command line

   `git clone https://github.com/tirilab/medx.git`
   
2. Unzip the download file if needed. 
3. Go to the project's root directory, run the terminal command below to install the package in the current working directory (.) in editable mode (-e)​
   
   `pip install -e .​`

4. Install dependencies if necessary
5. The package is ready to go. Test with the sample data “tests/sample_data/sample_med.csv” in your own codes or using the sample test "tests/test1.py" we provided.

### Alternative Usage

1. Install package using
   `pip install -i https://test.pypi.org/simple/ medx==1.0`

### Relevant Document
- Student Paper "An Automated Strategy to Calculate Medication Regimen Complexity" accepted to American Medical Informatics Association (AMIA) 2023 Symposium.
