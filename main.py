import streamlit as st
import pandas as pd
import xmlGenerator
import shutil

class Question:
	def __init__(self):
		self.correct_answer = ''
		self.question = ''
		self.answers = []

	def __str__(self):
		returnString = self.question + "\n"
		for i in range(0, len(self.answers)):
			answer = self.answers[i]
			if str(i) == self.correct_answer:
				returnString += i.__str__() + ")* " + answer + "\n"
			else:
				returnString += i.__str__() + ") " + answer + "\n"
		return returnString


def getQuestions(question_array):
    questions = []
    for row in question_array:
        question = Question()
        question.question = row[0]
        question.correct_answer = row[1]
        for i in range(2, len(row)):
            if row[i]=="nan":
                continue
            question.answers.append(row[i]);
        questions.append(question)
    return questions

st.title("CSV to QTI1.2 converter")
st.subheader("QTI1.2 can be imported into Macmillian(Cognero) Test Generator")
title = st.text_input('1. 請輸入將會顯示於Macmillan出題系統之標題', "2022-MB-1")
uploaded_file = st.file_uploader("2. 上傳eclass專用CSV檔案")
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file,skiprows=1, header=0)
    st.write(df.iloc[:,[3,4,7,8,9,10,11]])
    question_array = df.iloc[:,[3,4,7,8,9,10,11]].to_numpy()
    question_array = question_array.astype("str")
    questions = getQuestions(question_array)
    xmlGenerator.saveXML(questions, "./tmp/questions.xml")
    xmlGenerator.manifestXML(title, './tmp/imsmanifest.xml')
    shutil.make_archive("archive", 'zip', "./tmp")
    with open('archive.zip', 'rb') as f:
        st.download_button('Download Zip', f, file_name='archive.zip')  # Defaults to 'application/octet-stream'

# df = pd.read_csv('/Users/YLC/SynologyDrive/My_App/csv2qti/exam_import_csv_sample.csv')


