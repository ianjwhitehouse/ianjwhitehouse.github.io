# Imports
from subprocess import run, Popen, PIPE
from os import chdir
import urllib3
# from markdownify import markdownify as md
from bs4 import BeautifulSoup
from vllm import LLM, SamplingParams
import os
import numpy as np

# Global Vars
PROMPT = """You are a machine learning agent (refered to as assistant) in a conversation with 2 other agents - the user, who asks you questions, and the system, which can help you respond and instructs you on your responses.
You interact with the system through a series of commands.  To communicate with the user, just respond as normal.  To communicate with the system, use %, immediately followed by a command.  After the command itself, arguments can be added with spaces, i.e. CMD ARG1 ARG2 ARG3 ARG4  The available commands are:
 - "LIST": Lists the files in the current folder.  There are no arguments for this command.  Equivalent to "ls -l" linux command.
 - "CD": Change the current directory.  The only argument for this command is the linux-style path to the directory you want to move to.  Equivalent to the "cd" linux command.
 - "READ": Read a file.  The only argument for this command is the linux-style path to the file you want to read.  Equivalent to the "cat" linux command.
 - "WRITE": Write a file.  The first argument to this command is the linux-style path to the file you want to write, and all other arguments are the text of the file.  Rougly equivilent to the "echo" command, i.e. "echo ARG2...ARGN > ARG1.
 - "READ_WEB": Read a webpage as a text file. The only argument to this command is the url of the webpage.
 - "SEARCH_WEB": Search the web using Google. All arguments to this command are the text of the search.

Some examples of conversations are below:
user: What is in the file dogs.txt in my home directory?
assistant: %READ ~/dogs.txt
system: Rufus\nCaptain\nBella
system: Summarize my previous output to answer the users question or statement.  If you need more detail, you can run another command
assistant: Dogs.txt is a list of dog names

user: What files are on my Desktop?
assistant %CD ~\Desktop
system: Changed directory to ~\Desktop
system: Either report to the user or run another command for more information
assistant: %LIST
system hello_world.py Essays Folder
system: Summarize my previous output to answer the users question or statement.  If you need more detail, you can run another command
assistant: Your essays and hello_world.py are on the desktop

user: What is the capital of New Zealand?
assistant: %SEARCH Capital of New Zealand
system: [Text Output that includes the Capital of New Zealand]
system: either report to the user or run another command for more information
assistant: the capital of New Zealand is Wellington
user: Can you write that to a file called New_Zealand.txt?
assistant: %WRITE New_Zealand.txt The Capital of New Zealand is Wellington
system: File New_Zealand.txt successfully written
system: Summarize my previous output to answer the users question or statement.  If you need more detail, you can run another command
assistant: I have saved the information to New_Zealand.txt


Below this is the transcript of the conversation so far.  End your reply with a new line.
"""

LLM_SERVER = LLM(model="mistralai/Mistral-7B-v0.1")

# Class to query it
class ToolingModel:
    def __init__(self, pass_in_llm=False, debug=0):
        self.pass_in_llm = pass_in_llm
        self.debug = debug
        self.previous_system_outs = {}
        self.log = []

    def main_loop(self):
        llm_in = PROMPT
        turn = 0 # 0 for user, 1 for llm

        while True:
            if turn == 0:
                # User's turn
                inp = input("> ")
                user_inp = inp
                llm_in += ("\nuser: %s" % inp)
                self.log.append("user: %s" % inp)
                
                if len(llm_in) > 2 * len(PROMPT) and len(self.previous_system_outs.items()) > 0:
                    k, v = list(self.previous_system_outs.items())[0]
                    llm_in = llm_in.replace(k, v)
                    del self.previous_system_outs[k]
            else:
                llm_in += "\nassistant:"
                inp = self.ask_llm(llm_in, user_question=user_inp)
                llm_in += inp
                if not self.pass_in_llm:
                    print("assistant: " + inp)
                self.log.append("assistant: %s" % inp)

            if inp[0] == " " and inp[1] == "%":
                llm_in = self.process_command(inp[2:], llm_in, turn==0 or self.debug > 0, self.debug > 1)
            elif inp[0] == "%":
                llm_in = self.process_command(inp[1:], llm_in, turn==0 or self.debug > 0, self.debug > 1)
            # elif turn == 1 and not self.debug and not self.pass_in_llm:
            #     print("assistant: " + llm_in)
            else:
                turn += 1
                turn %= 2

    def ask_llm(self, question, user_question):
        # Asks the LLM a bunch of times and returns the most popular result
        if self.pass_in_llm:
            print("COPY INTO LLM")
            print(question)
            print("END COPY")
            return input("assistant: ")
        else:
            sampling_params = SamplingParams(n=32, max_tokens=150)# temperature=0.8, top_p=0.90, n=16, max_tokens=50)
            outputs = LLM_SERVER.generate([question], sampling_params)[0]
            outputs = [output.text.split("\n")[0].strip() for output in outputs.outputs]
            outputs = [output for output in outputs if len(output) > 0]
            min_len = min([len(output) for output in outputs])

            def most_shared_words(sentence, lst):
                count = 0
                usr_count = 0
                for word in sentence.lower().split(" "):
                    for sent in lst:
                        if word in sent.lower().split(" "):
                            count += 1/len(lst) #len(sent.split(" "))
                for word in user_question.lower().split(" "):
                    if word in sentence.lower().split(" "):
                        usr_count += 1

                count *= 1 + (0.2 * usr_count)
                count /= np.sqrt(len(sentence))
                
                cmds = ["%LIST", "%CD", "%READ", "%WRITE", "%READ_WEB", "%SEARCH_WEB"]
                if any([sentence.startswith(c) for c in cmds]):
                    count *= 1.5
                elif sentence.startswith("%") or sentence.startswith(" %"):
                    return 0
                return count

            outputs = [(most_shared_words(output, outputs), output) for output in outputs]
            # for output in outputs:
            #     cmds = ["%LIST", "%CD", "%READ", "%WRITE", "%READ_WEB", "%SEARCH_WEB"]
            #     if any([c in output[1] for c in cmds]) and output[0] > 0.25:
            #         return output[1]
            if self.debug > 1:
                print(outputs)
            
            return max(outputs, key=lambda x: x[0])[1]
            

    def process_command(self, input, llm_in, show_output, show_intermediate):
        cmd, *args = input.split(" ")

        # Process command
        if cmd == "LIST":
            if show_intermediate:
                print("debug:", ["ls"])#, "-l"])
            res = run(["ls"], capture_output=True).stdout.decode("UTF-8").replace("\n", r"; ")
        
        elif cmd == "CD":
            try:
                path = os.path.realpath(r"\ ".join(args[0:]))
                if show_intermediate:
                    print("debug: chdir %s" % path)
                chdir(path)
                res = "Changed directory to " + path
            except FileNotFoundError: 
                res = "ERR - directory not found"
            except OSError:
                res = "ERR - issue changing directory"
        
        elif cmd == "READ":
            if show_intermediate:
                print("debug:", ["cat", args[0]])
            res = run(["cat", args[0]], capture_output=True).stdout.decode("UTF-8").replace("\n", r"\n")
            if res == "":
                res = "ERR - file not found"

        elif cmd == "WRITE":
            if show_intermediate:
                print("debug:", 'echo "%s" > %s' % (" ".join(args[1:]), args[0]))
            res = Popen('echo "%s" > %s' % (" ".join(args[1:]), args[0]), shell=True, stdout=PIPE).communicate()[0].decode("UTF-8")
            if res == "":
                res = "File %s successfully written" % args[0]

        elif cmd == "READ_WEB":
            if show_intermediate:
                print("debug: self.load_web(%s)" % args[0])
            res = 'The website says "%s"' % self.load_web(args[0])

        elif cmd == "SEARCH_WEB":
            res = "+".join(args[0:])
            res = "https://google.com/search?q=%s" % res
            if show_intermediate:
                print("debug: self.load_web(%s)" % res)
            res = 'The website says "%s"' % self.load_web(res)
        else:
            res = "ERR - %%%s in not a command.  The available commands are %%LIST, %%CD, %%READ, %%WRITE, %%READ_WEB, %%SEARCH_WEB.  Choose one of those commands." % cmd

        # Report results
        if res.startswith("ERR"):
            res = "system: %s\nsystem: Try command again" % res
        else:
            self.previous_system_outs[res] = "[The output to %s was displayed here, but was removed]" % input
            res = "system: %s\nsystem: Summarize my previous output to answer the users question or statement.  If you need more detail, you can run another command" % res

        if show_output:
            print(res)

        return llm_in + "\n" + res

    def load_web(self, url):
        try:
            req = urllib3.request("GET", url, headers={"User-Agent": "Chrome", "Accept-Encoding": "UTF-8"}).data.decode("utf-8", errors="ignore")
            # markdown = md(
            #     "".join([str(tag) for tag in BeautifulSoup(req).find_all([
            #         "a", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6"
            #     ], hidden=False, recursive=True)])
            # )
            return " ".join([el.get_text() for el in BeautifulSoup(req).find_all([
                "a", "p", "div", "h1", "h2", "h3", "h4", "h5", "h6"
            ], hidden=False, recursive=True)])[150:][:5000]
            return markdown.replace("\n", ";").replace("/url?q=", "")
        except urllib3.exceptions.MaxRetryError:
            return "ERR - website not found"

    def save_log(self, filename):
        with open(filename, "w+") as f:
            f.write("\n".join(self.log))
        print("Saved")

if __name__ == "__main__":
    try:
        tm = ToolingModel(pass_in_llm=False, debug=0)
        tm.main_loop()
    except KeyboardInterrupt:
        tm.save_log("log.txt")