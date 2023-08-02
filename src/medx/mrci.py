import pandas as pd
from collections import OrderedDict
import re

########################  LOCAL ONLY FUNCTIONS ########################
# Load med list data for calculation
def load(ifilename):
    try:
        df = pd.read_csv(ifilename)
        df.fillna('', inplace = True)
        return df
    except:
        print("Read File Error\n")
        exit
    return None

# Write mrci score to an output file
def write(df, ofilename):
    try:
        df.to_csv(ofilename, index = False)
    except:
        print("Write File Error\n")
        exit

    return 1

# Supporting function: Get dosage form and route for Score A
def formSearch(data, i, drug, ndcCol = 'NDC Code', medCol = 'Medication Name'):
    # Search NDC code for dosage form if ndc exist
    if ndcCol in data.columns:
 
        code = data[ndcCol][i]
    
        if data[ndcCol].isnull()[i]:
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
            # return just the medication name when NDC presented but no corresponding dosage form is found
            return [data[medCol][i], 'Invalid']
        else:
            # return the dosage form and route of the medication
            dosage = index['DOSAGEFORMNAME'].astype('string').item()
            route = index['ROUTENAME'].astype('string').item()
            return [dosage,route]
    else:
        # return just the medication name when NDC not presented
        return [data[medCol][i], 'Invalid']

# Initialize supporting data for Medication Complexity Calculation
def init():

    # initialize supporting keyword list for MRCI score A, B and C
    # score A dictionary {(form regex, route regex)): score}
    keywordsA = pd.DataFrame()
    try:
        keywordsA = pd.read_csv('src/medx/data/keywordsA.csv')    
    except:
        print("Read File Error: Keywords A\n")
        exit

    scoreADict = OrderedDict()
    for _, row in keywordsA.iterrows():
        scoreADict[(row['Form'], row['Route'])] = row['Weighting']

    # score B dictionary {frequency regex: score}
    keywordsB = pd.DataFrame()
    try:
        keywordsB = pd.read_csv('src/medx/data/keywordsB.csv', encoding= 'unicode_escape')
    except:
        print("Read File Error: Keywords B\n")
        exit

    scoreBDict = OrderedDict()
    for _,row in keywordsB.iterrows():
        scoreBDict[row['Frequency']] = row['Weighting']

    # score C dictionary {additional directions regex: score}
    keywordsC = pd.DataFrame()
    try:
        keywordsC = pd.read_csv('src/medx/data/keywordsC.csv', encoding='unicode_escape')
    except:
        print("Read File Error: Keywords C\n")
        exit

    scoreCDict = OrderedDict()
    for _,row in keywordsC.iterrows():
        scoreCDict[row['Additional Directions']] = row['Weighting']
    
    # initialize supporting NDC directory
    drug = pd.DataFrame()
    try:
        drug = pd.read_excel('src/medx/data/ndc_database.xlsx')
        drug.fillna('', inplace = True)
    except:
        print("Read File Error: NDC\n")
        exit

    return scoreADict, scoreBDict, scoreCDict, drug

############ GLOBAL ###################

# Calculation of single time point MRCI
def mrciCalc(ifilename, ofilename, doseCol = 'Dose', sigCol = 'SIG', ndcCol = 'NDC Code', medCol = 'Medication Name', idenCol = 'MRN', includeMC = True):

    # initialize supporting data for calculation
    [scoreADict, scoreBDict, scoreCDict, drug] = init()

    # read in medication list data
    data = load(ifilename)
    
    # Score Calculation
    # Initialize 
    scoresA = []
    scoresB = []
    scoresC = []
    counts = []
    scoreA = 0
    scoreB = 0
    scoreC = 0
    count = 0
    i = 0

    # initialize separate dictionary for each patient
    dictAb = scoreADict.copy()
    dictCb = scoreCDict.copy()

    try:
        iden = data[idenCol][0]
    except:
        print("Invalid patient identifier.\n")
        exit

    while i < data.shape[0]:

        if iden == data[idenCol][i]:
            
            # initial data filtering and processing
            # ignore vaccine and inactive drug
            if (data[doseCol].isnull()[i] and data[sigCol].isnull()[i]):
                i = i + 1
                continue
            elif 'Therapeutic Class' in data.columns:
                if data['Therapeutic Class'][i] == 'MISCELLANEOUS MEDICAL SUPPLIES, DEVICES, NON-DRUG' or data['Therapeutic Class'][i] == 'BIOLOGICALS':
                    i = i + 1
                    continue
            try:
                # for score A
                [form, route] = formSearch(data, i, drug, ndcCol, medCol)
                # for score B
                sig = data[sigCol][i]
                
            except:
                i = i + 1
                continue
            
            # Temporarily offset for MC regarding human error in data collections
            if data['Therapeutic Class'][i] != 'DIAGNOSTIC':
                count = count + 1

            # calculating scoreA
            if route != 'Invalid':
                # Medications can be found in NDC Database
                for j in scoreADict:
                    if re.search(j[0],form) and re.search(j[1],route):
                        scoreA = scoreA + dictAb[j]
                        dictAb[j] = 0
                        break
            else:
                # Medications cannot be found in NDC Database
                for j in scoreADict:
                    if re.search(j[0],form) and re.search(j[1],sig):
                        scoreA = scoreA + dictAb[j]
                        dictAb[j] = 0
                        break
            
            if sig != '':
                # calculating scoreB
                for b in scoreBDict:
                    if re.search(b, sig):
                        scoreB = scoreB + scoreBDict[b]
                        break
    
                # calculating scoreC
                for c in scoreCDict:
                    if re.search(c,sig):
                        scoreC = scoreC + dictCb[c]
                        dictCb[c] = 0
            i = i + 1
        else:
            iden = data[idenCol][i]
            scoresA.append(scoreA)
            scoresB.append(scoreB)
            scoresC.append(scoreC)
            counts.append(count)
            
            scoreA = 0
            scoreB = 0
            scoreC = 0
            count = 0

            # reset mrci form
            dictAb = scoreADict.copy()
            dictCb = scoreCDict.copy()
        
    # append scores of last item
    scoresA.append(scoreA)
    scoresB.append(scoreB)
    scoresC.append(scoreC)
    counts.append(count)

    totalScore = []
    for i in range(len(scoresA)):
        totalScore.append(scoresA[i] + scoresB[i] + scoresC[i])

    idenlist = list(data[idenCol].unique())
    if includeMC:
        df = pd.DataFrame({idenCol : idenlist, 'valid_med_count': counts, 'sec_a_score': scoresA, 'sec_b_score': scoresB, 'sec_c_score': scoresC, 'pmrci_score': totalScore})
    else:
        df = pd.DataFrame({idenCol : idenlist, 'sec_a_score': scoresA, 'sec_b_score': scoresB, 'sec_c_score': scoresC, 'pmrci_score': totalScore})
    
    # write calculation results to ouput csv file
    write(df, ofilename)

    return 1

# Calculation of multiple time points (2 for now)
def mrciCompa(ifilename, ofilename, doseCol = 'Dose', sigCol = 'SIG', ndcCol = 'NDC Code', medCol = 'Medication Name', idenCol = 'MRN', timeCol = 'Time_period', time1 = "current at enrollment", includeMC = True):

    # initialize supporting data for calculation
    [scoreADict, scoreBDict, scoreCDict, drug] = init()

    data = load(ifilename)

    # Score Calculation
    # Initialize 
    scoresA = []
    scoresB = []
    scoresC = []
    counts = []
    scoreA = 0
    scoreB = 0
    scoreC = 0
    scoresA_after = []
    scoresB_after = []
    scoresC_after = []
    counts_after = []
    scoreA_after = 0
    scoreB_after = 0
    scoreC_after = 0
    count = 0
    count_after = 0
    i = 0

    # initialize separate dictionary for each person to avoid double counting issue in score A & C
    dictAb = scoreADict.copy()
    dictA3mo = scoreADict.copy()
    dictCb = scoreCDict.copy()
    dictC3mo = scoreCDict.copy()

    try:
        iden = data[idenCol][0]
    except:
        print("Invalid patient identifier.\n")
        exit

    while i < data.shape[0]:

        if iden == data[idenCol][i]:
            
            # initial data filtering and processing
            # ignore vaccine and inactive drug
            if (data[doseCol].isnull()[i] and data[sigCol].isnull()[i]) or data['Therapeutic Class'][i]=='MISCELLANEOUS MEDICAL SUPPLIES, DEVICES, NON-DRUG' or data['Therapeutic Class'][i]=='BIOLOGICALS':
                i = i + 1
                continue
            try:
                # for score A
                [form, route] = formSearch(data, i, drug, ndcCol, medCol)
                # for score B
                sig = data[sigCol][i]
                
            except:
                print(i)
                i = i + 1
                continue
            
            # baseline (current at enrollment)
            if data[timeCol][i] == time1:

                count = count + 1

                # calculating scoreA
                if route != 'Invalid':
                    # Medications can be found in NDC Database
                    for j in scoreADict:
                        if re.search(j[0], form) and re.search(j[1], route):
                            scoreA = scoreA + dictAb[j]
                            dictAb[j] = 0
                            break
                else:
                    # Medications cannot be found in NDC Database
                    for j in scoreADict:
                        # try:
                        if re.search(j[0],form) and re.search(j[1],sig):
                            scoreA = scoreA + dictAb[j]
                            dictAb[j] = 0
                            break
                
                # calculating scoreB
                if sig != '':
                    for b in scoreBDict:
                        if re.search(b, sig):
                            scoreB = scoreB + scoreBDict[b]
                            break
        
                    # calculating scoreC
                    for c in scoreCDict:
                        if re.search(c,sig):
                            scoreC = scoreC + dictCb[c]
                            dictCb[c] = 0
                    
            # three month later
            else:
                count_after = count_after + 1
                
                # calculating scoreA
                if route != 'Invalid':
                    # Medications can be found in NDC Database
                    for j in scoreADict:
                        if re.search(j[1], route) and re.search(j[0], form) :
                            scoreA_after = scoreA_after + dictA3mo[j]
                            dictA3mo[j] = 0
                            break
                else:
                    # Medications cannot be found in NDC Database
                    for j in scoreADict:
                        if re.search(j[0],form) and re.search(j[1],sig):
                            scoreA_after = scoreA_after + dictA3mo[j]
                            dictA3mo[j] = 0
                            break
                
                # calculating scoreB
                if sig != '':
                    for j in scoreBDict:
                        if re.search(j, sig):
                            scoreB_after = scoreB_after + scoreBDict[j]
                            break

                    # calculating scoreC
                    for j in scoreCDict:
                        if re.search(j, sig):
                            scoreC_after = scoreC_after + dictC3mo[j]
                            dictC3mo[j] = 0
            i = i + 1
            
        else:
            iden = data[idenCol][i]
            scoresA.append(scoreA)
            scoresB.append(scoreB)
            scoresC.append(scoreC)
            scoresA_after.append(scoreA_after)
            scoresB_after.append(scoreB_after)
            scoresC_after.append(scoreC_after)
            counts.append(count)
            counts_after.append(count_after)
            
            scoreA = 0
            scoreB = 0
            scoreC = 0
            scoreA_after = 0
            scoreB_after = 0
            scoreC_after = 0
            count = 0
            count_after = 0

            # reset mrci form
            dictAb = scoreADict.copy()
            dictA3mo = scoreADict.copy()
            dictCb = scoreCDict.copy()
            dictC3mo = scoreCDict.copy()
    
    # append scores of last item
    scoresA.append(scoreA)
    scoresB.append(scoreB)
    scoresC.append(scoreC)
    scoresA_after.append(scoreA_after)
    scoresB_after.append(scoreB_after)
    scoresC_after.append(scoreC_after)
    counts.append(count)
    counts_after.append(count_after)

    totalScore = []
    for i in range(len(scoresA)):
        totalScore.append(scoresA[i] + scoresB[i] + scoresC[i])

    totalScore_after = []
    for i in range(len(scoresA)):
        totalScore_after.append(scoresA_after[i] + scoresB_after[i] + scoresC_after[i])

    idenlist = list(data[idenCol].unique())

    if includeMC:
        df = pd.DataFrame({idenCol : idenlist, 'valid_med_count_t1': counts, 'sec_a_score_t1' : scoresA, 'sec_b_score_t1' : scoresB, 'sec_c_score_t1': scoresC, 'pmrci_score_t1': totalScore, 'valid_med_count_t2': counts_after, 'sec_a_score_t2': scoresA_after, 'sec_b_score_t2': scoresB_after, 'sec_c_score_t2': scoresC_after, 'pmrci_score_t2': totalScore_after})
    else:
        df = pd.DataFrame({idenCol : idenlist, 'sec_a_score_t1' : scoresA, 'sec_b_score_t1' : scoresB, 'sec_c_score_t1': scoresC, 'pmrci_score_t1': totalScore, 'sec_a_score_t2': scoresA_after, 'sec_b_score_t2': scoresB_after, 'sec_c_score_t2': scoresC_after, 'pmrci_score_t2': totalScore_after})

    # write calculation results to ouput csv file
    write(df, ofilename)

    return 1


