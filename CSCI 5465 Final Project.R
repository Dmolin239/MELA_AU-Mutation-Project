#CSCI 5465 Final Project
#Multiple Logistic Regression
#David Moline 
#Last Updated: 12/21/2020

#install.packages("readxl")
#This package enables R to read excel sheets 
library(readxl)


#Logistic Regression


#Assigning the patient mutation data to a variable
patient.mutation = read_excel("CSCI 5465 Final Project Data.xlsx")
patient.mutation = data.frame(patient.mutation)

#Variable Key:
  #Mutation
    #Patient has EGR1 mutation = 1
    #Patient does not have EGR1 mutation = 0 
  #Sex
    #Male = 0
    #Female = 1
  #Patient exposure
    #Chronic = 2
    #Intermittent = 1
    #None = 0
  #Patient family history 
    #Patient has family history with cancer = 1
    #Patient does not have family history with cancer = 0

#Dummy variable for patient exposure (chronic, intermittent, none)
#This is done because the patient exposure level has more than two levels/outcomes
chronic = as.numeric(patient.mutation$exposure == "Chronic")
intermittent = as.numeric(patient.mutation$exposure == "Intermittent")
none = as.numeric(patient.mutation$exposure == "None") #omit; this is reference level

#Logistic Regression Formula 

#response (dependent) variable is mutation occurrence in EGR1 gene for the patient
#explanatory (independent) variables are age, sex, chronic, intermittent, history

log.regression = glm(mutation ~ age + sex + chronic + intermittent + history, data = patient.mutation, family = binomial)
summary(log.regression)

#None of the p-values are below 0.05.
#Therefore, with a 95% confidence level, we accept the 
#null hypothesis and state that the probability of a mutation in the donor's 
#EGR1 gene is not significantly dependent of the patient's age sex, exposure intensity 
#to light or family history of cancer. 





#Model Search 

#Determining the best model via the Akaike's Information Criterion (AIC)
#Lower AIC -> better model prediction 

#step() can be used to determining the best model by calculating the AIC values and dropping variables one by one

step(log.regression)

#best model is mutation ~ chronic

#Creating a logistic regression of just chronic
log.chronic = glm(mutation ~ chronic, data = patient.mutation, family = binomial)
summary(log.chronic)
#p-value doesn't change much, it actually increases! (0.252 -> 0.264)

#None of the p-values are below 0.05.
#Therefore, with a 95% confidence level, we accept the 
#null hypothesis and state that the probability of a mutation in the donor's 
#EGR1 gene is not significantly dependent of the patient's chronic exposure 
#intensity to light.





#Testing only the age and sex variables

#Several patients are missing exposure and family history data (i.e. the files/data do not exist)
#However, every donor does have an age and sex variable.

#log.test examines the p-values of age and sex to explain the EGR1 mutation occurrence 
log.test= glm(mutation ~ age + sex, data = patient.mutation, family = binomial)
summary(log.test)
#p-values increased further.

#Therefore, with 95% confidence level, we accept the null hypothesis and 
#state that the that the probability of a mutation in the donor's EGR1 gene 
#is not significantly dependent of the patient's age or sex.


