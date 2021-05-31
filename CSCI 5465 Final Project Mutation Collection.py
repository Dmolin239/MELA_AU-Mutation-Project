#CSCI 5465 Final Project Data Collection
#David Moline
#Last updated: 12/21/2020

#The purpose of this code is to collect the patient data aquired from the ICGC Data Portal 
#into a text document that can be used in R for a multiple linear regression model

#Note: This file operates by gathering patient information of individual patients and their associated files
#(i.e. patient mutations, patient information, patient exposure, etc.)
#The patient file format is provided by the ICGC Data Portal 


import pandas                          #Data Frames is how we'll be filtering, storing, and manipulating the patient data
from openpyxl import load_workbook     #Enables the data to be exported to an excel file


def filter_patient_file(patient_mutations):
    #This function filters the patient mutation file to only collect mutations
    #located on chromosome 5 (EGR1 is located on chromosome 5)
    
    chr_filter = patient_mutations["chromosome"] == "5"       #Filtering for only Chromosome 5
    filtered_patient_file = patient_mutations[chr_filter]     #Keeping only the patien's Chromosome 5 mutations 
        
    return filtered_patient_file


def check_mutations(EGR1_mutations, patient_mutations):
    #This function checks to see if the EGR1 mutations exist in the current patient's 
    #dataframe of all chromosome 5 mutations
    
    #check to see if any of the EGR1 mutations is present within the patient's mutation file
    check = EGR1_mutations.assign(result=EGR1_mutations["Mutation ID"].isin(patient_mutations["icgc_mutation_id"]).astype(int))
    
    #returns an integer as true or false
    #0 means mutation is not present 
    #1 means mutation is present
    return check



#Gathering the EGR1 mutation information
EGR1_mutant_file = pandas.read_csv("EGR1_MELA_AU_Mutation_Information.txt", sep ="\t")[["Mutation ID",
                "Genomic DNA Change", "Type", "Consequences", "Donors affected"]]

#Gathering the patient's mutation information (Initially this contains ALL of the patient's mutations on ALL chromosomes)
patient_mutations = pandas.read_csv("simple_somatic_mutation.open.tsv", sep ="\t")[["icgc_mutation_id",
                "icgc_donor_id", "chromosome", "chromosome_start", "chromosome_end", "chromosome_strand",
                "mutation_type", "reference_genome_allele", "mutated_from_allele", "mutated_to_allele"]]



#Gathering the patient's general information (i.e. id, age, sex)
patient_info = pandas.read_csv("donor.tsv", sep ="\t")[["icgc_donor_id", "donor_sex", 
                "donor_age_at_diagnosis"]]

#Collecting the patient's ID
patient_id = patient_info["icgc_donor_id"][0]

#Collecting the patient's age 
patient_age = patient_info["donor_age_at_diagnosis"][0]



#Gathering the patient's exposure intensity
#This file does not exist for all patients so the try statement tests to see if the file is present
try:
    patient_exposure = pandas.read_csv("donor_exposure.tsv", sep ="\t")[["icgc_donor_id", "exposure_type",
                "exposure_intensity"]]
    
    #Establishing variables for patient's exposure intensity
    #These will be converted into dummy variables later in R for the regression analysis
    if "Chronic" in patient_exposure["exposure_intensity"][0]:
        #Chronic = 2
        patient_exposure_level = "Chronic" 
    elif "Intermittent" in patient_exposure["exposure_intensity"][0]:
        #Intermittent = 1
        patient_exposure_level = "Intermittent"
    else:
        #None or unknown exposure intensity = 0
        patient_exposure_level = "None/Unknown"
except:
    print("donor_exposure.tsv is not present. Exposure level set to NA")
    patient_exposure_level = "NA"
    
    
#Gathering the patient's family history
#This file does not exist for all patients so the try statement tests to see if the file is present
try:
    patient_family = pandas.read_csv("donor_family.tsv", sep ="\t")
    
    #Establishing dummy variables for the patient's family history
    if "yes" in patient_family["donor_has_relative_with_cancer_history"][0]:
        #Patient has family history with cancer = 1
        is_patient_family_mutated = 1
    else:
        #Patient does not have family history with cancer = 0
        is_patient_family_mutated = 0
except:
    print("donor_family.tsv is not present. History level set to NA")
    is_patient_family_mutated = "NA"



#Filtering the patient's mutation file to only contain mutations on chr 5 
chr5_patient_mutations = filter_patient_file(patient_mutations)
   
#Collecting the patient's EGR1 mutation information (based on ALL of the patient's chr 5 mutations)
new_patient_mutation = check_mutations(EGR1_mutant_file, chr5_patient_mutations)


#Establishing dummy variables for patient's mutation; Used in the regression analysis
if 1 in new_patient_mutation.result.values:
    #Patient has a mutated EGR1 = 1
    is_patient_mutated = 1
else:
    #Patient has a non-mutated EGR1 = 0
    is_patient_mutated = 0

    
#Establishing dummy variables for the patient's sex
if "female" in patient_info["donor_sex"][0]:
    #female = 1
    patient_sex = 1
else:
    #male = 0
    patient_sex = 0



#Exporting the patient information to excel for the regression analysis in R

#List containing the information
export_patient_information = [patient_id, is_patient_mutated, patient_age, patient_sex, 
                              patient_exposure_level, is_patient_family_mutated]

#Creating a new data rame form the list so Pandas and transport the information to an excel sheet
export_df = pandas.DataFrame(export_patient_information)
export_df = export_df.transpose() #transpose the dataframe to fill by columnn 



#Writing to the Excel sheet

#The following code was modified from the skeleton code by Nensi Trambadiya 

#Citation:
#Trambadiya N. 2019. Using Python Pandas With Excel Sheet. BetterProgramming. Accessed on 2020 Dec 19. https://medium.com/better-programming/using-python-pandas-with-excel-d5082102ca27

writer = pandas.ExcelWriter("CSCI 5465 Final Project Data.xlsx", engine = "openpyxl")

#Loading the file as our workbook
writer.book = load_workbook("CSCI 5465 Final Project Data.xlsx")

#Copies the existing sheets to preserve previously appended content
writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

#Read the file
reader = pandas.read_excel("CSCI 5465 Final Project Data.xlsx")

#Exporting the data frame to the excel sheet 
export_df.to_excel(writer,sheet_name = "Data", index = False, header = False, startrow=len(reader)+1)

#Closing the writer 
writer.close()




 