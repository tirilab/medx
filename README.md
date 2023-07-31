# MedX: Medication Regimen Complexity Calculation Python Package
## developed by TIRI Lab @ JHU

slides to the tutorial: https://livejohnshopkins-my.sharepoint.com/:p:/g/personal/ylu106_jh_edu/EUIkpgsQpMlJlmaEnXg8sKgBql_4nIVezXoZ74VmKnPkSw?e=VIylef

#### Features
| Feature   Name                               | Description                                                                        | Input(s)                                                                                                                                                                                                                                 | Output(s)                                                   |   |
|----------------------------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|---|
| Load File                                    | Read in data file with modifiable column name                                    | A   file name for the input medication records list, a column name for patient identifier (optionally), a column name for medication name (optionally), a   column name for SIG (optionally), a column name for NDC code (optionally)  | An   indicator showing whether the file loads successfully  |   |
| Write file                                   | Write   MRCI output to an output file with modifiable column name                  | A file name for the output file, a column name for patient identifier   (optionally)                                                                                                                                                   | An   indicator showing whether the file writes successfully |   |
| Customize Decision Keywords                  | Make   modification of decision keyword list                                       | A file name for the  data file containing the updated keywords, identifier of list need to be modified (A/B/C)                                                                                                                         | None                                                        |   |
| Calculate MRCI and MC (Single time point)    | Calculate MRCI score and MC from the data read in                                | Input data of medication list                                                                                                                                                                                                          | MRCI scores and MC at one time point                      |   |
| Calculate MRCI and MC (Multiple time points) | Calculate MRCI score and MC from the data read in when there are time identifiers | Input data of medication list, column name for the time identifier                                                                                                                                                                     | MRCI scores and MC at multiple time points                |   |


#### Usage Guide
1. Download this repo using "Download ZIP" or command line

   `git clone https://github.com/tirilab/medx`
   
2. Unzip the download file if needed. Go to the project's root directory, run the terminal command below to install the package in the current working directory (.) in editable mode (-e)​
   
   `pip install -e .​`

3. Install dependencies if necessary
4. The package is ready to go. Test with the sample data “sample_med.csv” ​using function `medx.mrciCalc()` and `medx.mrciCompa()` in your codespace.

