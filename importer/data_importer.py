# -*- coding: utf-8 -*-
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
                q28 = self.get_q28(row, questions)
                q36 = self.get_q36(row, questions, answers)
                q37 = self.get_q37(row, questions, answers)
                q48 = self.get_q48(row, questions, answers)
                q51 = self.get_q51(row, questions)
                q54 = self.get_q54(row, questions)
                q56 = self.get_q56(row, questions)
                q65 = self.get_q65(row, questions, answers)
                q72 = self.get_q72(row, questions, answers)
                q73 = self.get_q73(row, questions, answers)
                q74 = self.get_q74(row, questions)
                q75 = self.get_q75(row, questions, answers)
                q76_1 = self.get_q76_1(row, questions, answers)
                q76_2 = self.get_q76_2(row, questions, answers)
                q77 = self.get_q77(header, row, questions, answers)
                q81 = self.get_q81(row, questions, answers)
                q82 = self.get_q82(row, questions, answers)
                q84 = self.get_q84(row, questions, answers)
                q88 = self.get_q88(row, questions, answers)
                q104 = self.get_q104(row, questions, answers)
                q109 = self.get_q109(header, row, questions, answers)
                q112 = self.get_q112(row, questions, answers)
                q113 = self.get_q113(row, questions, answers)
                q118 = self.get_q118(row, questions, answers)
                q120 = self.get_q120(row, questions, answers)
                q121 = self.get_q121(row, questions, answers)
                q122 = self.get_q122(row, questions, answers)
                q124 = self.get_q124(row, questions, answers)
                q126 = self.get_q126(row, questions, answers)
                q127 = self.get_q127(row, questions, answers)
                q128 = self.get_q128(header, row, questions, answers)
                q129 = self.get_q129(row, questions, answers)
                q136 = self.get_q136(row, questions)
                q136_1 = self.get_q136_1(row, questions, answers)
                q138 = self.get_q138(row, questions, answers)
                q140 = self.get_q140(row, questions, answers)
                json_data = self.build_json_doc(id, q2, q7, q9, q11, q14, q15, q18, q22, q23, q28, q36, q37, q48,
                                                q51, q54, q56, q65, q72, q73, q74, q75, q76_1, q76_2, q77, q81,
                                                q82, q84, q88, q104, q109, q112, q113, q118, q120, q121, q122,
                                                q124, q126, q127, q128, q129, q136, q136_1, q138, q140)
                collection.insert(json_data)
                counter += 1

            print "\n\tDone. Imported %i documents.\n" % counter

    def build_json_doc(self, id, q2, q7, q9, q11, q14, q15, q18, q22, q23, q28, q36, q37, q48, q51, q54,
                       q56, q65, q72, q73, q74, q75, q76_1, q76_2, q77, q81, q82, q84, q88, q104, q109,
                       q112, q113, q118, q120, q121, q122, q124, q126, q127, q128, q129, q136, q136_1, q138, q140):
        return {
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
            "q28": q28,
            "q36": q36,
            "q37": q37,
            "q48": q48,
            "q51": q51,
            "q54": q54,
            "q56": q56,
            "q65": q65,
            "q72": q72,
            "q73": q73,
            "q74": q74,
            "q75": q75,
            "q76_1": q76_1,
            "q76_2": q76_2,
            "q77": q77,
            "q81": q81,
            "q82": q82,
            "q84": q84,
            "q88": q88,
            "q104": q104,
            "q109": q109,
            "q112": q112,
            "q113": q113,
            "q118": q118,
            "q120": q120,
            "q121": q121,
            "q122": q122,
            "q124": q124,
            "q126": q126,
            "q127": q127,
            "q128": q128,
            "q129": q129,
            "q136": q136,
            "q136_1": q136_1,
            "q138": q138,
            "q140": q140
        }

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
        for i in range(3, 40):
            if row[i] != "" and len(row[i]) == 1:
                if int(row[i]) != 0:
                    col_id = header[i][:5].strip()
                    q7_json['answer']['en'].append(answers[col_id]['en'])
                    q7_json['answer']['sq'].append(answers[col_id]['sq'])
                    q7_json['answer']['sr'].append(answers[col_id]['sr'])
        return q7_json

    def get_q9(self, row, questions, answers):
        return self.build_questions_json(row[40], "9", questions, answers)

    def get_q11(self, row, questions):
        return self.build_regular_question(row, questions, "11", 41)

    def get_q14(self, row, questions, answers):
        return self.build_questions_json(row[42], "14", questions, answers)

    def get_q15(self, row, questions, answers):
        return self.build_questions_json(row[43], "15", questions, answers)

    def get_q18(self, row, questions, answers):
        return self.build_questions_json(row[44], "18", questions, answers)

    def get_q22(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 44, "22", 1, 7)

    def get_q23(self, row, questions, answers):
        return self.build_questions_json(row[51], "23", questions, answers)

    def get_q28(self, row, questions):
        return self.build_regular_question(row, questions, "28", 52)

    def get_q29(self):
        # TODO: Implement the logic q29.
        return ""

    def get_q34(self):
        # TODO: Implement the logic q34.
        return ""

    def get_q35(self):
        # TODO: Implement the logic q35.
        return ""

    def get_q36(self, row, questions, answers):
        return self.build_questions_json(row[72], "36", questions, answers)

    def get_q37(self, row, questions, answers):
        return self.build_questions_json(row[73], "37", questions, answers)

    def get_q39(self):
        # TODO: Implement the logic q39.
        return ""

    def get_q48(self, row, questions, answers):
        return self.build_questions_json(row[80], "48", questions, answers)

    def get_q51(self, row, questions):
        return self.build_regular_question(row, questions, "51", 81)

    def get_q54(self, row, questions):
        return self.build_regular_question(row, questions, "54", 82)

    def get_q56(self, row, questions):
        return self.build_regular_question(row, questions, "56", 83)

    def get_q65(self, row, questions, answers):
        return self.build_questions_json(row[84], "65", questions, answers)

    def get_q72(self, row, questions, answers):
        return self.build_questions_json(row[85], "72", questions, answers)

    def get_q73(self, row, questions, answers):
        return self.build_questions_json(row[86], "73", questions, answers)

    def get_q74(self, row, questions):
        return self.build_regular_question(row, questions, "74", 87)

    def get_q75(self, row, questions, answers):
        return self.build_questions_json(row[88], "75", questions, answers)

    def get_q76_1(self, row, questions, answers):
        return self.build_questions_json(row[89], "76.1", questions, answers)

    def get_q76_2(self, row, questions, answers):
        return self.build_questions_json(row[90], "76.2", questions, answers)

    def get_q77(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 90, "77", 1, 5)

    def get_q81(self, row, questions, answers):
        return self.build_questions_json(row[105], "81", questions, answers)

    def get_q82(self, row, questions, answers):
        return self.build_questions_json(row[106], "82", questions, answers)

    def get_q84(self, row, questions, answers):
        return self.build_questions_json(row[107], "84", questions, answers)

    def get_q88(self, row, questions, answers):
        return self.build_questions_json(row[108], "88", questions, answers)

    def get_q104(self, row, questions, answers):
        return self.build_questions_json(row[109], "104", questions, answers)

    def get_q109(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 109, "109", 1, 4)

    def get_q112(self, row, questions, answers):
        return self.build_questions_json(row[113], "112", questions, answers)

    def get_q113(self, row, questions, answers):
        return self.build_questions_json(row[114], "113", questions, answers)

    def get_q117(self):
        # TODO: Implement the logic q117
        return ""

    def get_q118(self, row, questions, answers):
        return self.build_questions_json(row[123], "118", questions, answers)

    def get_q119(self):
        # TODO: Implement the logic q119
        return ""

    def get_q120(self, row, questions, answers):
        return self.build_questions_json(row[127], "120", questions, answers)

    def get_q121(self, row, questions, answers):
        return self.build_questions_json(row[128], "121", questions, answers)

    def get_q122(self, row, questions, answers):
        return self.build_questions_json(row[129], "122", questions, answers)

    def get_q124(self, row, questions, answers):
        return self.build_questions_json(row[130], "124", questions, answers)

    def get_q126(self, row, questions, answers):
        return self.build_questions_json(row[131], "126", questions, answers)

    def get_q127(self, row, questions, answers):
        return self.build_questions_json(row[132], "127", questions, answers)

    def get_q128(self, header, row, questions, answers):
        return self.build_array_questions(header, row, questions, answers, 132, "128", 1, 5)

    def get_q129(self, row, questions, answers):
        return self.build_questions_json(row[137], "129", questions, answers)

    def get_q135(self):
        # TODO: Implement the logic q135
        return ""

    def get_q136(self, row, questions):
        return self.build_regular_question(row, questions, "136", 141)

    def get_q136_1(self, row, questions, answers):
        return self.build_questions_json(row[142], "136.1", questions, answers)

    def get_q138(self, row, questions, answers):
        return self.build_questions_json(row[143], "138", questions, answers)

    def get_q140(self, row, questions, answers):
        return self.build_questions_json(row[144], "140", questions, answers)

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
            else:
                question_json['answer']['en'] = answers[question + "." + entry + "."]['en']
                question_json['answer']['sq'] = answers[question + "." + entry + "."]['sq']
                question_json['answer']['sr'] = answers[question + "." + entry + "."]['sr']
        else:
            question_json["answer"] = ""
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
        questions = self.get_qa(file_path)
        return questions

    def get_answers(self):
        # get answers json
        file_path = "importer/data/cso-answers.csv"
        return self.get_qa(file_path)
