__version__ = '0.1.98'
from supabase import create_client
import traceback
import csv 
from tenacity import wait_random_exponential, retry, stop_after_attempt
import asyncio 
import time 
import openai 
import os 
from collections import Counter
from bettertest.promptTemplate import promptTemplate
# from promptTemplate import promptTemplate
import concurrent.futures
import threading
import uuid
import builtins
import inspect
import webbrowser


supa_url = "https://gwfhoxolvmhoszkvddnv.supabase.co"
supa_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imd3ZmhveG9sdm1ob3N6a3ZkZG52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODU3MzU0OTgsImV4cCI6MjAwMTMxMTQ5OH0.gFJSZGvGPx2Prr9bu4TxpkRT1Z7ezDZL-x6zVN1_SE0"

import time

supabase = create_client(supa_url, supa_key)

class LogPrintCalls:

  def __init__(self):
    self.response_obj = {}

  def __enter__(self):
    self.original_print = builtins.print

    def new_print(*args, **kwargs):
        caller_name = inspect.stack()[1].function
        if caller_name in self.response_obj:  # assume already initialized
            self.response_obj[caller_name].append(args)
        else:
            self.response_obj[caller_name] = [args]

    builtins.print = new_print

  def __exit__(self, exc_type, exc_value, traceback):
    builtins.print = self.original_print

  def return_response_obj(self):
    return self.response_obj


class BetterTest: 
    def __init__(self, user_email: str, openai_api_key: str):
        self.user_email = user_email
        self.run_id = uuid.uuid4()
        openai.api_key = openai_api_key
    def __enter__(self):
        self.original_print = builtins.print

        def new_print(*args, **kwargs):
            self.log_function("print", *args)
            self.original_print(*args, **kwargs)

        builtins.print = new_print

    def eval(self, questions, answers, llm_function, num_runs=1):
        try:
            start_time = time.time()
            try:
                print("🧪 Generating your answers")
                print("🚀 Go to see your logs: https://better-test.vercel.app/"+str(self.run_id))
                print("⌛️ It might take 4-5s for your results to start loading...")
                link = "https://better-test.vercel.app/" + str(self.run_id)
                print("🚀 Go to see your logs:", link)
                # Open the link in the browser
                webbrowser.open(link)
                model_answer_start_time = time.time()
                model_answers = self.llm_query_async(questions, answers, llm_function)
                model_answer_end_time = time.time()
                print("model answer time: ", model_answer_end_time - model_answer_start_time)
            except:
                traceback.print_exc()
            # accuracy_scores = []
            # for i in range(num_runs):
            #   response = internal_eval(questions, model_answers, answers, start_time)
            #   print("🎉 Accuracy score in run " + str(i + 1) + ": ", response["accuracy_score"])
            #   accuracy_scores.append(response["accuracy_score"])
            # return "🚀 You're average accuracy score is: " + str(int(sum(accuracy_scores)/len(accuracy_scores))) + "%."
            return model_answers
        except Exception as e:
            traceback.print_exc()

    def write_to_supabase(self, run_object): 
        # print("writing to supabase: ", run_object)
        data = {
            'user_email': self.user_email,
            'run_uuid': str(self.run_id),
            'run_data': run_object
        }
        supabase.table('test_runs').insert(data).execute()

    async def async_get_data(self, llm_function, question):
        data = await asyncio.to_thread(llm_function, question)
        return data
    
    def run_test_func(self, llm_function, question, solution_answer): 
        # Run the test function against each question
        log_print_calls = LogPrintCalls()
        with log_print_calls:
            result = llm_function(question)
        # log the results here
        log_output = log_print_calls.return_response_obj()
        tmp_obj = self.async_inner_func_internal_eval(question, result, solution_answer)
        for key in log_output.keys(): 
            if "bettertest" in log_output[key][0][0]:
                tmp_obj["function_"+key] = log_output[key]
        self.write_to_supabase(tmp_obj)
        return "Done!"


    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def llm_query_async(self, question_list, answer_list, llm_function):
        try:
            answers = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                for batch in range(0, len(question_list), 250):  # batch process 250 at a time
                    tasks = [
                        executor.submit(self.run_test_func, llm_function, question, answer_list[batch+i])
                        for i, question in enumerate(question_list[batch:batch + 250])
                    ]
                    answer = [task.result() for task in tasks]
                    answers.extend(answer)
            return answers
        except:
            traceback.print_exc()

    def async_inner_func_internal_eval(self, question, model_answer, solution_answer):
        rationale = []
        decisions = []
        model_run_time = []
        for i in range(3):
            output = self.temp_eval_model(question, model_answer, solution_answer)
            rationale.append(output["model_rationale"])
            decisions.append(output["model_decision"])
            model_run_time.append(output["model_run_time"])
        value, idx = self.most_frequent_value(decisions)
        response_object = {
            "question": question,
            "model_answer": model_answer, 
            "solution_answer": solution_answer, 
            "model_decision": value, 
            "model_rationale": rationale[idx]
        }
        return response_object

    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
    def simple_openai_api_call(self, prompt):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        return completion.choices[0].message["content"]


    def temp_eval_model(self, question, model_answer, solution_answer): 
        model_run_start_time = time.time()
        pt = promptTemplate.replace("{{question}}", question)
        pt = pt.replace("{{model_answer}}", model_answer)
        pt = pt.replace("{{solution_answer}}", solution_answer)
        rationale = self.simple_openai_api_call(pt)
        if "decision" in rationale.lower(): 
            decision_part = rationale.lower().split("decision")[1]
            if "true" in decision_part.lower() or "false" in decision_part.lower(): 
                decision = decision_part
            else: 
                pt_with_rationale = pt + "\n\n" + rationale + "\n\n" + "what was the last decision? answer either 'True' or 'False'"
                decision = self.simple_openai_api_call(pt_with_rationale)
        else: 
            pt_with_rationale = pt + "\n\n" + rationale + "\n\n" + "what was the last decision? answer either 'True' or 'False'"
            decision = self.simple_openai_api_call(pt_with_rationale)
        model_run_end_time = time.time()
        output = {
            "model_decision": decision,
            "model_rationale": rationale,
            "model_run_time": model_run_end_time - model_run_start_time
        }
        return output


    def most_frequent_value(self, decisions):
        true_count = 0
        true_idx = -1
        false_count = 0
        false_idx = -1
        for idx, decision in enumerate(decisions): 
            decision_lowercase = decision.lower()
            if "true" in decision_lowercase: 
                true_count += 1
                if true_idx == -1: 
                    true_idx = idx
            else: 
                false_count += 1 
                if false_idx == -1: 
                    false_idx = idx
        if true_count > false_count:
            most_freq_val = 'True'
            most_freq_index = true_idx
        else:
            most_freq_val = 'False'
            most_freq_index = false_idx
        return most_freq_val, most_freq_index