# -*- coding: utf-8 -*-
from app import mongo_utils
from pymongo import MongoClient
from progressbar import ProgressBar, Percentage, ETA, Counter, Bar
import csv


mongo = MongoClient()

db = mongo.kcsf

collection = db.cso_survey
collection.remove({})


class DataImporter(object):
    def run(self):
        print "\n\tImporting data...\n"
        questions = self.get_questions()
        answers = self.get_answers()
        self.get_data(questions, answers)

    def get_data(self, questions, answers):
        file_path = "importer/data/cso-data.csv"
        with open(file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = reader.next()
            counter = 0
            reader_list = list(reader)
            widgets = ['        Progress: ', Percentage(), ' ', Bar(marker='#', left='[', right=']'),
                   ' ', ETA(), " - ", Counter(), " Documents    "]
            pbar = ProgressBar(widgets=widgets)
            for row in pbar(reader_list):
                q2 = self.get_q2(row, questions)
                q7 = self.get_q7(header, row, questions, answers)
                q9 = self.get_q9(row, questions, answers)
                q11 = self.get_q11(row, questions)
                q14 = self.get_q14(row, questions, answers)
                q15 = self.get_q15(row, questions, answers)
                q18 = self.get_q18(row, questions, answers)
                q22 = self.get_q22(header, row, questions, answers)
                q23 = self.get_q23(row, questions, answers)
                q28 = self.get_q28(row, questions)
                json_data = self.build_json_doc(q2, q7, q9, q11, q14, q15, q18, q22, q23, q28)
                collection.insert(json_data)
                counter += 1

            print "\n\tDone. Imported %i documents.\n" % counter

    def build_json_doc(self, q2, q7, q9, q11, q14, q15, q18, q22, q23, q28):
        return {
            "q2": q2,
            "q7": q7,
            "q9": q9,
            "q11": q11,
            "q14": q14,
            "q15": q15,
            "q18": q18,
            "q22": q22,
            "q23": q23,
            "q28": q28
        }

    def question_json(self, question, questions):
        return {
            "question": questions[question]["en"]
        }

    def get_q2(self, row, questions):
        return {
            "question": questions['2']['en'],
            "answer": row[1]
        }

    def get_q7(self, header, row, questions, answers):
        q7_json = {
            "question": questions['7']['en'],
            "answer": []
        }
        for i in range(3, 40):
            if row[i] != "" and len(row[i]) == 1:
                if int(row[i]) != 0:
                    col_id = header[i][:5].strip()
                    q7_json['answer'].append(answers[col_id]['en'])
        return q7_json

    def get_q9(self, row, questions, answers):
        return self.build_question_json(row[40], "9", questions, answers)

    def get_q11(self, row, questions):
        return {
            "question": questions['11']['en'],
            "answer": row[41]
        }

    def get_q14(self, row, questions, answers):
        return self.build_question_json(row[42], "14", questions, answers)

    def get_q15(self, row, questions, answers):
        return self.build_question_json(row[43], "15", questions, answers)

    def get_q18(self, row, questions, answers):
        return self.build_question_json(row[44], "18", questions, answers)

    def get_q22(self, header, row, questions, answers):
        q22_json = {
            "question": questions['22']['en'],
            "answer": []
        }
        for i in range(1, 7):
            if row[i + 44] != "" and len(row[i + 44]) == 1:
                if int(row[i + 44]) != 0:
                    col_id = header[i + 44][:5].strip()
                    q22_json['answer'].append(answers[col_id + "1."]['en'])
        return q22_json

    def get_q23(self, row, questions, answers):
        return self.build_question_json(row[51], "23", questions, answers)

    def get_q28(self, row, questions):
        return {
            "question": questions['28']['en'],
            "answer": row[52]
        }

    def get_q29(self):
        # TODO: Implement the logic.
        return ""

    def get_q34(self):
        # TODO: Implement the logic.
        return ""

    def build_question_json(self, entry, question, questions, answers):
        question_json = {
            "question": questions[question]["en"]
        }
        if entry != "":
            question_json['answer'] = answers[question + "." + entry + "."]['en']
        return question_json


    def get_qa(self, file_path):
        json_result = {}
        with open(file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # Skip the header rows
            for row in reader:
                json_result[row[0]] = {
                    "en": row[3],
                    "sq": row[2],
                    "sr": row[1]
                }
        return json_result

    def get_questions(self):
        # get question json
        file_path = "importer/data/cso-questions.csv"
        return self.get_qa(file_path)

    def get_answers(self):
        # get answers json
        file_path = "importer/data/cso-answers.csv"
        return self.get_qa(file_path)
