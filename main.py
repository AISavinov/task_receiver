import requests
import argparse
import re
import os


class Receiver:
    def __init__(self, args: argparse.Namespace):
        self.task_name = self.getTaskName(args.repo_url)
        self.student_name = args.student_name
        self.code = self.getCode()

    def getCode(self) -> str:
        regex = re.compile('solution')
        for root, dirs, files in os.walk(".."):
            for file in files:
                if regex.match(file):
                    with open(os.path.dirname(os.path.abspath(__file__)) +"/../"+ file) as f:
                        return ''.join(f.readlines())

    @classmethod
    def getTaskName(cls, repo_url: str) -> str:
        match = re.search(r'.*\/(?P<name>.*)\.git', repo_url)
        return match.group('name')

    def __isDataValid(self):
        return self.task_name and self.student_name and self.code

    def receive(self):
        print(self.task_name)
        print(self.student_name)
        print(self.code)
        if not self.__isDataValid():
            raise Exception("You specified wrong parameter.")

        submission_url = "http://51.15.104.77:3333/submission"
        try:
            response = requests.get(submission_url, params={"task_name": self.task_name,
                                                            "student_name": self.student_name,
                                                            "code": self.code})
            print(response.text)
        except Exception as e:
            print("Error during submission:", e, "\nContact tg: @mujov")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Send parameters (task_name=repo name, student_name=branch, code) to grader.')
    parser.add_argument('--repo_url', type=str, help='Current git repository url which invokes this task.')
    parser.add_argument('--student_name', type=str, help='Student name (same as in LMS, example: asavinov).')
    args = parser.parse_args()
    Receiver(args).receive()
