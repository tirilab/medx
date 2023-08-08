# MedX: Medication Regimen Complexity Calculation Python Package

### Overview

[MedX](https://github.com/tirilab/medx) is a python package developed by Translational Informatics @ Johns Hopkins University.

Understanding medication regimen complexity is important to understand what patients may benefit from pharmacist interventions.
Medication Regimen Complexity Index (MRCI), a 65-item tool to quantify the complexity by incorporating the number, dosage form, frequency, and special administration instructions of prescription medicines, provides a more nuanced way of assessing complexity. 

MedX package aims to automate the calculation of MRCI and Medication Count from raw EHR data. 
A sample of EHR pseudodata can be found [here](https://github.com/tirilab/medx/blob/release/1.0/tests/sample_data/sample_med.csv).

### Dependencies and Requiorements of Medx:
* Python >= 3.6
* Pandas

### Installation and Usage

Check [here](https://medx.readthedocs.io/en/latest/usage.html#installation) for installation and usage documentations.

### Issue
Submit bug reports and feature requests to [MedX bug tacker](https://github.com/tirilab/medx/issues).

### License
The MedX package was written by Louise Lu [ylu106@jhu.edu].

MedX is licensed under the [MIT License](https://github.com/tirilab/medx/blob/main/LICENSE.txt).

### Reference
* Student Paper "An Automated Strategy to Calculate Medication Regimen Complexity" accepted to American Medical Informatics Association (AMIA) 2023 Symposium.

* George J, Phun Y-T, Bailey MJ, Kong DC, Stewart K. Development and validation of the medication regimen complexity index. Annals of Pharmacotherapy. 2004;38(9):1369–76. doi:10.1345/aph.1d479 

* Green A. Align: Aligning Medications with What Matters Most, a pharmacist-led deprescribing intervention. 2022Jun21; Available from: https://beta.clinicaltrials.gov/study/NCT04938648 