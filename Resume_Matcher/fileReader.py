from operator import index
from pandas._config.config import options
import Cleaner
import textract as tx
import pandas as pd
import numpy
import os
import tf_idf

user = os.getcwd()
print(user)


resume_dir = "/home/goyal/Projects/Mini_Project_Semester_7/media/Resume/"
job_desc_dir = "/home/goyal/Projects/Mini_Project_Semester_7/media/JobDesc/"
resume_names = os.listdir(resume_dir)
job_description_names = os.listdir(job_desc_dir)
print(resume_names)
print(job_description_names)
document = []


def read_resumes(list_of_resumes, resume_directory):
    placeholder = []
    for res in list_of_resumes:
        temp = []
        temp.append(res)
        text = tx.process(resume_directory+res, encoding='ascii')
        text = str(text, 'utf-8')
        temp.append(text)
        placeholder.append(temp)
    return placeholder


document = read_resumes(resume_names, resume_dir)


def get_cleaned_words(document):
    for i in range(len(document)):
        raw = Cleaner.Cleaner(document[i][1])
        document[i].append(" ".join(raw[0]))
        document[i].append(" ".join(raw[1]))
        document[i].append(" ".join(raw[2]))
        sentence = tf_idf.do_tfidf(document[i][3].split(" "))
        document[i].append(sentence)
    return document


Doc = get_cleaned_words(document)

Database = pd.DataFrame(document, columns=[
                        "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"])

Database.to_csv(
    "/home/goyal/Projects/Mini_Project_Semester_7/Resume_Matcher/Job_Data.csv", index=False)

# Database.to_json("Resume_Data.json", index=False)


def read_jobdescriptions(job_description_names, job_desc_dir):
    placeholder = []
    for tes in job_description_names:
        temp = []
        temp.append(tes)
        text = tx.process(job_desc_dir+tes, encoding='ascii')
        text = str(text, 'utf-8')
        temp.append(text)
        placeholder.append(temp)
    return placeholder


job_document = read_jobdescriptions(job_description_names, job_desc_dir)

Jd = get_cleaned_words(job_document)

jd_database = pd.DataFrame(Jd, columns=[
                           "Name", "Context", "Cleaned", "Selective", "Selective_Reduced", "TF_Based"])

jd_database.to_csv(
    "/home/goyal/Projects/Mini_Project_Semester_7/Resume_Matcher/Job_Data.csv", index=False)
