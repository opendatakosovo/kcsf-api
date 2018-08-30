# -*- coding: utf-8 -*-
import pprint

from pymongo import MongoClient
from progressbar import ProgressBar, Percentage, ETA, Counter, Bar
import csv

mongo = MongoClient()

db = mongo.kcsf

collection = db.cso_survey



class DataImporter(object):
    def run(self, year):
        print "\n\tImporting data for year: %s ...\n" % year 
        questions = self.get_questions(year)
        answers = self.get_answers(year)
        self.get_data(questions, answers, "" , year)

    def get_data(self, questions, answers, fileName, year):
        if fileName != "":
            file_path = filename
        else:
            file_path = "importer/data/"+ year+"/cso-data.csv"
        with open(file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = reader.next()
            counter = 0
            reader_list = list(reader)
            widgets = ['        Progress: ', Percentage(), ' ', Bar(marker='#', left='[', right=']'),
                       ' ', ETA(), " - ", Counter(), " Documents    "]
            pbar = ProgressBar(widgets=widgets)
            for row in pbar(reader_list):
                id = row[0]
                q2 = self.get_q2(row, questions)
                q7 = self.get_q7(header, row, questions, answers)
                q9 = self.get_q9(row, questions, answers)
                q11 = self.get_q11(row, questions)
                q14 = self.get_q14(row, questions, answers)
                q15 = self.get_q15(row, questions, answers)
                q18 = self.get_q18(row, questions, answers)
                q22 = self.get_q22(header, row, questions, answers)
                q23 = self.get_q23(row, questions, answers)
                q26 = self.get_q26(row, questions)
                q32 = self.get_q32(header, row, questions,answers)
                q33 = self.get_q33(row, questions, answers)
                q34 = self.get_q34(row, questions, answers)
                q43 = self.get_q43(row, questions, answers)
                q45 = self.get_q45(row, questions)
                q48 = self.get_q48(row, questions)
                q50 = self.get_q50(row, questions)
                q58 = self.get_q58(row, questions, answers)
                q64 = self.get_q64(row, questions, answers)
                q65 = self.get_q65(row, questions, answers)
                q66 = self.get_q66(row, questions)
                q67 = self.get_q67(row, questions, answers)
                q68 = self.get_q68(row, questions, answers)
                q69_1 = self.get_q69_1(row, questions)
                q69_2 = self.get_q69_2(row, questions)
                q69_3 = self.get_q69_3(row, questions)
                q69_4 = self.get_q69_4(row, questions)
                q69_5 = self.get_q69_5(row, questions)
                q74 = self.get_q74(row, questions, answers)
                q78 = self.get_q78(row, questions, answers)
                q94 = self.get_q94(header, row, questions, answers)
                q96 = self.get_q96(row, questions, answers)
                q97 = self.get_q97(row, questions, answers)
                q102 = self.get_q102(row, questions, answers)
                q103 = self.get_q103(header, row, questions, answers)
                q104 = self.get_q104(row, questions, answers)
                q105 = self.get_q105(row, questions, answers)
                q106 = self.get_q106(row, questions, answers)
                q108 = self.get_q108(row, questions, answers)
                q111 = self.get_q111(row, questions, answers)
                q112 = self.get_q112(row, questions, answers)
                q113 = self.get_q113(header, row, questions, answers)
                q114 = self.get_q114(row, questions, answers)
                q119 = self.get_q119(header, row, questions, answers)
                q120 = self.get_q120(row, questions)
                q121 = self.get_q121(row, questions, answers)
                q124 = self.get_q124(row, questions, answers)
                q126 = self.get_q126(row, questions, answers)
                json_data = self.build_json_doc(id, q2, q7, q9, q11, q14, q15, q18, q22, q23, q26, q32, q33, q34, q43, q45, q48,
                       q50, q58, q64, q65, q66, q67, q68, q69_1, q69_2, q69_3, q69_4, q69_5, q74, q78, q94,
                       q96, q97, q102, q103, q104, q105, q106, q108, q111, q112, q113, q114, q119, q120, q121, q124, q126, year)
                collection.insert(json_data)
                counter += 1

            print "\n\tDone. Imported %i documents.\n" % counter

    def build_json_doc(self, id, q2, q7, q9, q11, q14, q15, q18, q22, q23, q26,q32, q33, q34, q43, q45, q48,
                       q50, q58, q64, q65, q66, q67, q68, q69_1, q69_2, q69_3, q69_4, q69_5, q74, q78, q94,
                       q96, q97, q102, q103, q104, q105, q106, q108, q111, q112, q113, q114, q119, q120, q121, q124, q126, year):
        json_obj = {
                "year": year,
                "id": id,
                "q2": q2,
                "q7": q7,
                "q9": q9,
                "q11": q11,
                "q14": q14,
                "q15": q15,
                "q18": q18,
                "q22": q22,
                "q23": q23,
                "q26": q26,
                "q32": q32,
                "q33": q33,
                "q34": q34,
                "q43": q43,
                "q45": q45,
                "q48": q48,
                "q50": q50,
                "q58": q58,
                "q64": q64,
                "q65": q65,
                "q66": q66,
                "q67": q67,
                "q68": q68,
                "q69_1": q69_1,
                "q69_2": q69_2,
                "q69_3": q69_3,
                "q69_4": q69_4,
                "q69_5": q69_5,
                "q74": q74,
                "q78": q78,
                "q94": q94,
                "q96": q96,
                "q97": q97,
                "q102": q102,
                "q103": q103,
                "q104": q104,
                "q105": q105,
                "q106": q106,
                "q108": q108,
                "q111": q111,
                "q112": q112,
                "q113": q113,
                "q114": q114,
                "q119": q119,
                "q120": q120,
                "q121": q121,
                "q124": q124,
                "q126": q126          
            }
        return json_obj

    def get_q2(self, row, questions):
        return self.build_regular_question(row, questions, "2", 1)

    def get_q7(self, header, row, questions, answers):
        # return self.build_array_questions(header, row, questions, answers, 3, "7", 1, 38)
        q7_json = {
            "question": {
                "en": questions['7']['en'],
                "sq": questions['7']['sq'],
                "sr": questions['7']['sr']
            },
            "answer": {
                "en": [],
                "sq": [],
                "sr": [],
            }
        }
        for i in range(2, 43):
            if row[i] != "" and len(row[i]) == 1:
                if int(row[i]) != 0:
                    col_id = header[i][:4].strip()
                    q7_json['answer']['en'].append(answers[col_id]['en'])
                    q7_json['answer']['sq'].append(answers[col_id]['sq'])
                    q7_json['answer']['sr'].append(answers[col_id]['sr'])
        return q7_json

    def get_q9(self, row, questions, answers):
        return self.build_questions_json(row[43], "9", questions, answers)

    def get_q11(self, row, questions):
        return self.build_regular_question(row, questions, "11", 44)

    def get_q14(self, row, questions, answers):
        return self.build_questions_json(row[45], "14", questions, answers)

    def get_q15(self, row, questions, answers):
        return self.build_questions_json(row[46], "15", questions, answers)

    def get_q18(self, row, questions, answers):
        return self.build_questions_json(row[47], "18", questions, answers)

    def get_q22(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 48, "22", 1, 7)

    def get_q23(self, row, questions, answers):
        return self.build_questions_json(row[54], "23", questions, answers)

    def get_q26(self, row, questions):
        return self.build_regular_question(row, questions, "26", 55)

    # def get_q29(self):
    #     # TODO: Implement the logic q29.
    #     return ""

    # def get_q34(self):
    #     # TODO: Implement the logic q34.
    #     return ""

    def get_q32(self,header,row,questions, answers):
        return self.build_array_questions_with_different_answers(header,row,questions, answers, 56 ,"32",0, 7)

    def get_q33(self, row, questions, answers):
        return self.build_questions_json(row[63], "33", questions, answers)

    def get_q34(self, row, questions, answers):
        return self.build_questions_json(row[64], "34", questions, answers)

    def get_q39(self):
        # TODO: Implement the logic q39.
        return ""

    def get_q43(self, row, questions, answers):
        return self.build_questions_json(row[65], "43", questions, answers)

    def get_q45(self, row, questions):
        return self.build_regular_question(row, questions, "45", 66)

    def get_q48(self, row, questions):
        return self.build_regular_question(row, questions, "48", 67)

    def get_q50(self, row, questions):
        return self.build_regular_question(row, questions, "50", 68)

    def get_q58(self, row, questions, answers):
        return self.build_questions_json(row[69], "58", questions, answers)

    def get_q64(self, row, questions, answers):
        return self.build_questions_json(row[70], "64", questions, answers)

    def get_q65(self, row, questions, answers):
        return self.build_questions_json(row[71], "65", questions, answers)

    def get_q66(self, row, questions):
        return self.build_regular_question(row, questions, "66", 72)

    def get_q67(self, row, questions, answers):
        return self.build_questions_json(row[73], "67", questions, answers)

    def get_q68(self, row, questions, answers):
        return self.build_questions_json(row[74], "68", questions, answers)

    def get_q69(self, row, questions):
        return self.build_array_questions(header, row, questions, answers, 75, "79", 1, 5)

    def get_q74(self, row, questions, answers):
        return self.build_questions_json(row[80], "74", questions, answers)

    def get_q78(self, row, questions, answers):
        return self.build_questions_json(row[81], "78", questions, answers)

    def get_q94(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 82, "94", 1, 4)

    def get_q96(self, row, questions, answers):
        return self.build_questions_json(row[85], "96", questions, answers)

    def get_q97(self, row, questions, answers):
        return self.build_questions_json(row[86], "97", questions, answers)

    def get_q102(self, row, questions, answers):
        return self.build_questions_json(row[87], "102", questions, answers)

    def get_q103(self, header, row, questions, answers):
          return self.build_array_questions_with_different_answers(header, row, questions, answers, 88, "103", 0, 3)

    def get_q104(self, row, questions, answers):
        return self.build_questions_json(row[91], "104", questions, answers)

    def get_q105(self, row, questions, answers):
        return self.build_questions_json(row[92], "105", questions, answers)

    def get_q106(self, row, questions, answers):
        return self.build_questions_json(row[93], "106", questions, answers)

    def get_q108(self, row, questions, answers):
        return self.build_questions_json(row[94], "108", questions, answers)

    def get_q111(self, row, questions, answers):
        return self.build_questions_json(row[95], "111", questions, answers)

    def get_q112(self, row, questions, answers):
        return self.build_questions_json(row[96], "112", questions, answers)

    def get_q113(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 97, "113", 1, 5)

    def get_q114(self, row, questions, answers):
        return self.build_questions_json(row[101], "114", questions, answers)

    def get_q119(self, header, row, questions, answers):
         return self.build_array_questions_with_different_answers(header, row, questions, answers, 102, "119", 0, 3)

    def get_q120(self, row, questions):
        return self.build_regular_question(row, questions, "120", 105)

    def get_q121(self, row, questions, answers):
        return self.build_questions_json(row[106], "121", questions, answers)

    def get_q124(self, row, questions, answers):
        return self.build_questions_json(row[107], "124", questions, answers)

    def get_q126(self, row, questions, answers):
        return self.build_questions_json(row[108], "126", questions, answers)

    def build_regular_question(self, row, questions, id, index):
        return {
            "question": {
                "en": questions[id]['en'],
                "sq": questions[id]['sq'],
                "sr": questions[id]['sr'],
            },
            "answer": {
                "en": row[index],
                "sq": row[index],
                "sr": row[index],
            }
        }

    def build_array_questions(self, header, row, questions, answers, index, q_id, range_start, range_end):
        question_json = {
            "question": {
                "en": questions[q_id]['en'],
                "sq": questions[q_id]['sq'],
                "sr": questions[q_id]['sr'],
            },
            "answer": {
                "en": [],
                "sq": [],
                "sr": []
            }
        }
        for i in range(range_start, range_end):
            if row[i + index] != "" and len(row[i + index]) == 1:
                if int(row[i + index]) != 0:
                    col_id = header[i + index][:5].strip()
                    if col_id[-1] == ".":
                        col_id = col_id[:-1]
                    question_json['answer']['en'].append(answers[col_id + ".1."]['en'])
                    question_json['answer']['sq'].append(answers[col_id + ".1."]['sq'])
                    question_json['answer']['sr'].append(answers[col_id + ".1."]['sr'])
        return question_json

    def build_array_questions_with_different_answers(self, header, row, questions, answers, index, q_id, range_start, range_end):
        question_json = {
            "question": {
                "en": questions[q_id]['en'],
                "sq": questions[q_id]['sq'],
                "sr": questions[q_id]['sr'],
            },
            "answer": {
                "en": [],
                "sq": [],
                "sr": []
            }
        }
        for i in range(range_start, range_end):
            if row[i + index] != "" and len(row[i + index]) == 1:
                if int(row[i + index]) != 0:
                    col_id = header[i + index][:5].strip()
                    if col_id[-1] == ".":
                        col_id = col_id[:-1]
                    question_json['answer']['en'].append(answers[col_id + "."+row[i + index]+"."]['en'])
                    question_json['answer']['sq'].append(answers[col_id + "."+row[i + index]+"."]['sq'])
                    question_json['answer']['sr'].append(answers[col_id + "."+row[i + index]+"."]['sr'])
        return question_json


    def build_questions_json(self, entry, question, questions, answers):
        question_json = {
            "question": {
                "en": questions[question]["en"],
                "sq": questions[question]["sq"],
                "sr": questions[question]["sr"]
            }
        }
        if entry != "":
            question_json['answer'] = {}
            if len(entry) > 5:
                question_json['answer']['sq'] = entry
                question_json['answer']['sr'] = entry
                question_json['answer']['en'] = entry
            else:
                question_json['answer']['en'] = answers[question + "." + entry + "."]['en']
                question_json['answer']['sq'] = answers[question + "." + entry + "."]['sq']
                question_json['answer']['sr'] = answers[question + "." + entry + "."]['sr']
        else:
            question_json["answer"] = {
                "en": "",
                "sq": "",
                "sr": ""
            }
        return question_json

    def get_qa(self, file_path):
        json_result = {}
        with open(file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # Skip the header rows
            for row in reader:
                json_result[row[0]] = {
                    "en": row[3],
                    "sq": row[1],
                    "sr": row[2]
                }
        return json_result

    def get_questions(self, year):
        # get question json
        file_path = "importer/data/"+year+"/cso-questions.csv"
        questions = self.get_qa(file_path)
        return questions

    def get_answers(self, year):
        # get answers json
        file_path = "importer/data/"+year+"/cso-answers.csv"
        return self.get_qa(file_path)
