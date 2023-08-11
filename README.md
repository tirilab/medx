# MedX: Medication Regimen Complexity Calculation Python Package

### Overview

[MedX](https://github.com/tirilab/medx) is a Python package intended to transform longitudinal prescription data from the electronic health record (EHR) into patient-level medication regimen complexity metrics.

Understanding medication regimen complexity is important to understand what patients may benefit from pharmacist interventions.

MedX can take patient-level EHR data as input and then for each patient, calculate two medication complexity metrics: Medication Regimen Complexity Index (MRCI) score[1] and Medication Count.

The study team pilot-tested MedX with data collected in the ALIGN (Aligning Medications with What Matters Most) study.[2]

A sample of EHR pseudodata can be found [here](https://github.com/tirilab/medx/blob/release/1.0/tests/sample_data/sample_med.csv).

### Dependencies and Requiorements of Medx:
* Python >= 3.6
* Pandas

### Installation and Usage

Check [here](https://medx.readthedocs.io/en/latest/usage.html#installation) for installation and usage documentations.

### Issue
Submit bug reports and feature requests to [MedX bug tacker](https://github.com/tirilab/medx/issues).

### License and Citation
The MedX package was written by Louise Lu [ylu106@jhu.edu] and can be used as-is under the [MIT License](https://github.com/tirilab/medx/blob/main/LICENSE.txt) attached to the repository.

Please cite this article if using this package:
> Lu Y, Green AR, Quiles R, Taylor CO. An Automated Strategy to Calculate Medication Regimen Complexity. AMIA Annual Symposium 2023. (accepted)

1. George J, Phun Y-T, Bailey MJ, Kong DC, Stewart K. Development and validation of the medication regimen complexity index. Annals of Pharmacotherapy. 2004;38(9):1369–76. doi:10.1345/aph.1d479 

2. Green A. Align: Aligning Medications with What Matters Most, a pharmacist-led deprescribing intervention. 2022Jun21; Available from: https://beta.clinicaltrials.gov/study/NCT04938648 
