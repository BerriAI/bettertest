basePromptTemplate = """
Your objective is to evaluate the responses of a {chatbot_purpose}. You receive:

    User question: Question asked by a user to the chatbot.
    {optional_param_correct_response}
    Chatbot response: Response given by the chatbot to the user's question

    Evaluation Instructions: {chatbot_evaluation_instruction}
    Do not use your knowledge to complement the evaluation, your evaluation should be exclusively based on the 'Evaluation Instructions'.

     Grades:
     {chatbot_grading}
    
    ---
    Provide a rationale for your answer before giving your evaluation. Ensure the chatbot's response follows the 'Evaluation Instructions' provided. 

    Respond with a {chatbot_grading_options} according to your evaluation.
    --
    {example_1}
    ---
    
    {example_2}
    ---
    
    {example_3}
    ---
    
    {input_format}
"""