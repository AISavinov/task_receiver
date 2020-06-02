import requests
import argparse
import re
import os


class Receiver:
    def __init__(self, args: argparse.Namespace):
        self.course_name, self.task_name = self.getTaskName(args.repo_title)
        self.student_email = args.student_email
        self.code = self.getCode()
        self.grader_url = "http://51.15.104.77:10801/pass_task"
        self.submission_url = "http://51.15.104.77:3333/submission"

    def getCode(self) -> str:
        regex = re.compile('solution')
        for root, dirs, files in os.walk(".."):
            for file in files:
                if regex.match(file):
                    with open(os.path.dirname(os.path.abspath(__file__)) + "/../" + file) as f:
                        return ''.join(f.readlines())

    @classmethod
    def getTaskName(cls, repo_title: str) -> list:
        return repo_title.split('_')

    def __isDataValid(self):
        return self.course_name and self.task_name and self.student_email and self.code

    def getGradeInfo(self):
        try:
            headers = {
                'email': self.student_email,
                'content-type': 'application/json; charset=utf-8'
            }
            grade_info = requests.post(self.grader_url, headers=headers, data=self.code).json()
            return [float(grade_info['mark']), grade_info['additional_message']]
        except Exception as e:
            print("Error with grader:", e, "\nContact tg: @dvanyshkin")

    def sendGrade(self, mark: float):
        try:
            response = requests.get(self.submission_url, params={"course_name": self.course_name,
                                                                 "task_name": self.task_name,
                                                                 "student_email": self.student_email,
                                                                 "mark": mark})
            print(response.text)
        except Exception as e:
            print("Error during submission:", e, "\nContact tg: @mujov")

    def receive(self):
        print("Course name:", self.course_name)
        print("Task name:", self.task_name)
        print("Student email:", self.student_email)
        print("Submission: \n", self.code)
        if not self.__isDataValid():
            raise Exception("You specified wrong parameter.")
        mark, additional_info = self.getGradeInfo()
        print("Your grade is: ", mark)
        print("Additional message: ", additional_info)
        self.sendGrade(mark)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Send parameters (task_name=repo name, student_name=branch, code) to grader.')
    parser.add_argument('--repo_title', type=str, help='Current git repository url which invokes this task.')
    parser.add_argument('--student_email', type=str, help='Student name (same as in LMS, example: asavinov).')
    args = parser.parse_args()
    Receiver(args).receive()
