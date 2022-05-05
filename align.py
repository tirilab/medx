import pandas as pd
import numpy as np
import re

# takes ~40s to read in these two data sheet
data = pd.read_excel('Med list.xlsx')
drug = pd.read_excel('ndc database.xlsx')
drug.fillna('', inplace = True)
data.fillna('', inplace = True)

# Get dosage form and route for Score A
def formSearch(data,i,drug):
    code = data['NDC Code'][i]
    if data['NDC Code'].isnull()[i]:
        return ["invalid","invalid"]  
    if re.search('[0-9][0-9][0-9][0-9]-[0-9]+', code):
        n_code = code[0:9]
    else:
        # format code
        n_code = code[0:4] + '-' + code[4:8]
    # search in database
    index = drug[drug['PRODUCTNDC'] == n_code]
    if len(index) > 1:
        rows = [False for i in range(len(index))]
        rows[0] = True
        index = index.iloc[rows]
    
    if index.empty:
        # search in raw name
        return [data['Medication Name'][i], 'Invalid']   
    else:
        dosage = index['DOSAGEFORMNAME'].astype('string').item()
        route = index['ROUTENAME'].astype('string').item()

        return [dosage,route]

# Score A dictionary {(route regex, type regex) : score}
scoreADict = {('SPRAY|AEROSOL|TABLET','(?i)SUBLINGUAL') : 2, ('TABLET|CAPSULE','(?i)ORAL|mouth') : 1, ('MOUTHWASH|LOZENGE|GUM|LIQUID|SOLUTION|POWDER|GRANULE','(?i)ORAL||mouth') : 2, \
    ('CREAM|GEL|OINTMENT|SOLUTION|PATCH','(?i)TOPICAL|CUTANEOUS|TRANSDERMAL') : 2, ('DRESSING|PASTE','(?i)TOPICAL|CUTANEOUS|TRANSDERMAL') : 2, ('SPRAY|AEROSOL','(?i)TOPICAL|CUTANEOUS|TRANSDERMAL') : 1,\
    ('.*','(?i)AURICULAR|OPHTHALMIC|INTRAOCULAR|NASAL|nostril|nare') : 3,\
    ('GAS','(?i)INHALATION|INTRABRONCHIAL|RESPIRATORY') : 5, ('SOLUTION','(?i)inhale|INHALATION|INTRABRONCHIAL|RESPIRATORY') : 4, ('.*','(?i)INHALATION|INTRABRONCHIAL|RESPIRATORY') : 3,\
    ('SUPPOSITORY','.*') : 2, ('VAGINAL','(?i)CREAM') : 2, ('.*','(?i)SUBCUTANEOUS|INTRAVENOUS|INTRAMUSULAR|PERINEURAL|INTRAVASCULAR|INTRA-ARTERIAL|inject') : 3, ('ENEMA|LIQUID','(?i)RECTAL') : 2}

# score B dictionary {freq regex: score}
scoreBDict = {'(?i)MWF|MONDAY|WEDNESDAY|FRIDAY|(once weekly)|((once|twice) [a-z1-9]+ week[s]*)|(every [.]+ month[s]*)|(every other day)|(on|after) dialysis days|': 2,\
    '(?i)(twice|((2|two)( \(two\))* times)) (daily|a day)': 2, '(?i)(?=.*(twice|((2|two)( \(two\))* times)) (daily|a day))(?=.*(as needed)|PRN)': 1,\
    '(?i)(3|three) times (daily|a day)': 3, '(?i)(?=.*(3|three) times (daily|a day))(?=.*(as needed)|PRN)': 1.5, '(?i)(4|four) times (daily|a day)': 4,\
    '(?i)(?=.*(4|four) times (daily|a day))(?=.*(as needed)|PRN)': 2, '(?i)(once daily)|nightly|daily|(every (day|night|evening|afternoon))': 1, \
    '(?i)(?=.*(once daily)|nightly|daily|(every (day|night|evening|afternoon)))(?=.*(as needed)|PRN)': 0.5, '(?i)(as needed)|PRN': 0.5,\
    '(?i)every (12|twelve)( \(twelve\))* times)) hours': 2.5, '(?i)（?=.*every (12|twelve)( \(twelve\))* times)) hours)(?=.*(as needed)|PRN)': 1.5,\
    '(?i)every (8|eight)( \(eight\))* times)) hours': 3.5, '(?i)(?=.*every (8|eight)( \(eight\))* times)) hours)(?=.*(as needed)|PRN)': 2,\
    '(?i)every (6|six)( \(six\))* times)) hours': 4.5, '(?i)(?=.*every (6|six)( \(six\))* times)) hours)(?=.*(as needed)|PRN)': 2.5,\
    '(?i)every (4|four)( \(four\))* times)) hours': 6.5, '(?i)(?=.*every (4|four)( \(four\))* times)) hours)(?=.*(as needed)|PRN)': 3.5,\
    '(?i)every (2|two)( \(two\))* times)) hours': 12.5, '(?i)(?=.*every (2|two)( \(two\))* times)) hours)(?=.*(as needed)|PRN)': 6.5,\
    '(?i)(?=.*oxygen)(?=.*(as needed)|PRN)': 1, '(?i)(?=.*oxygen)(?=.*continuous)': 3, '(?i)oxygen': 2}

# score C dictionary {other intruction regex: score}
scoreCDict = {'(?i)(G-tube|PEG (EC)* tab|tablet)|crush|0[.][25]+|1/[24]|half|quarter|cut|break': 1,'(?i)dissolve': 1,\
    '(?i)tabs|tables|capsules|caps|puffs|inhalations|drops|patches|((combine|together|along|give) with)': 1,\
    '(?i)AM|PM|morning|afternoon|noon|evening|bedtime|night|(before bed)|hs|before': 1, \
    '(?i)water|juice|soda|liquid|non-carbonated|beverage': 1, '(as directed)|(adjust dose)|(hold if)|bridge|INR|(weight (gain|increase))|UTD': 2,\
    '(?i)taper|decrease|increase|wean|then|increasing|decreasing': 2, '(?i)(may repeat|(take additional))|([1-9]-[1-9])': 1,\
    '(?i)alternat|even|odd|(other days)': 2}

# loop and calculate scores
scoresA = []
scoresB = []
scoresC = []
counts = []
scoreA = 0
scoreB = 0
scoreC = 0
count = 0
i = 0

emrn = data.EMRN[i]
while i < data.shape[0]:
    
    if emrn==data.EMRN[i]:
        count+=1
        # ignore vaccine and inactive drug
        if (data['Dose'].isnull()[i] and data['SIG'].isnull()[i]) or data['Therapeutic Class'][i]=='MISCELLANEOUS MEDICAL SUPPLIES, DEVICES, NON-DRUG' or data['Therapeutic Class'][i]=='BIOLOGICALS':
            i = i + 1
            continue
        try:
            # for score A
            [form,route] = formSearch(data,i,drug)
            # for score B
            sig = data['SIG'][i]
            
        except:
            print(i)
            i = i + 1
            continue

        # calculating scoreA
        if route !='Invalid':
            # Medications can be found in NDC Database
            for j in scoreADict:
                try:
                    if re.search(j[0],form) and re.search(j[1],route):
                        scoreA = scoreA + scoreADict[j]
                        break
                except:
                    print("error: score A-1: ", form)
                    break
        else:
            # Medications cannot be found in NDC Database
            for j in scoreADict:
                try:
                    if re.search(j[0],form) and re.search(j[1],sig):
                        scoreA = scoreA + scoreADict[j]
                        break
                except:
                    print("error: score A-2: ", form)
                    break
            pass

        if sig !='':
            # calculating scoreB
            for j in scoreBDict:
                try:
                    if re.search(j,sig):
                        scoreB = scoreB + scoreBDict[j]
                        break
                except:
                    print("error: score B: ", sig)
                    break

            # calculating scoreC
            for j in scoreCDict:
                try:
                    if re.search(j,sig):
                        scoreC = scoreC + scoreCDict[j]
                        break
                except:
                    print("error: score C: ", sig)
                    break
            
        i = i + 1
    else:
        emrn = data.EMRN[i]
        scoresA.append(scoreA)
        scoresB.append(scoreB)
        scoresC.append(scoreC)
        counts.append(count)
        scoreA = 0
        scoreB = 0
        scoreC = 0
        count = 0
    
scoresA.append(scoreA)
scoresB.append(scoreB)
scoresC.append(scoreC)
counts.append(count)

totalScore = []
for i in range(len(scoresA)):
    totalScore.append(scoresA[i]+scoresB[i]+scoresC[i])

emrnlist = list(data.EMRN.unique())

df = pd.DataFrame({'EMRN':emrnlist, 'Medication Count': counts, 'Score A': scoresA, 'Score B': scoresB, 'Score C': scoresC, 'Total Score': totalScore})

df.to_csv('patient_score.csv', index = False)