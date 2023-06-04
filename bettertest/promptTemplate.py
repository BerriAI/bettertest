promptTemplate = """
Your objective is to evaluate the responses of a chatbot that answers questions over an API that creates a vector db qa app for developers. You receive:

    User question: Question asked by a user to the chatbot.
    Correct response: Correct response that should be given to that question
    Chatbot response: Response given by the chatbot to the user's question

    You must compare the chatbot's response with the correct response, and make an evaluation that can be True or False.
    Do not use your knowledge to complement the evaluation, your evaluation should be exclusively based on the correct response.

     Grades:
    True: Indicates that the chatbot's response is correct and complete, matching the correct response provided.
    False: Indicates that the chatbot's response is incorrect, incomplete, or does not match the correct response. The chatbot might invent new information (i.e. 'hallucinate'). If there is information in the chatbot, not seen in the solution answer, mark it as 'False'.
    
    ---
    Provide a rationale for your answer before giving your evaluation. Be sure to compare the chatbot's response to the correct response to determine if the chatbot's response is correct and complete, matching the correct response provided

    Respond with a either True/False according to your evaluation.
    --
    User question: what does a complex QA instance mean?
    Correct response: Sometimes users ask questions that require multiple pieces of context (e.g. What is the age of the actress who plays Meg in Family Guy? -> This requires us to know - Who plays Meg in Family Guy? Mila Kunis + What is Mila Kunis’s age?). To tackle this, we first run the user question through chatGPT, and have it break down that question into sub-components (as seen in the previous example) -> Find the most relevant chunks for each sub-question -> Feed that into chatGPT/GPT-4/whichever model you chose to get the answer to the users question.
    Chatbot response:A complex QA instance refers to a type of search in which users ask questions that require multiple pieces of context. For example, if a user asks "What is the age of the actress who plays Meg in Family Guy?", the system needs to know both "Who plays Meg in Family Guy?" and "What is Mila Kunis's age?" to provide an accurate answer. To handle this, the user question is broken down into sub-components, and the most relevant chunks for each sub-question are found and fed into the chatGPT/GPT-4 model to get the answer.
    Rationale: Yes, the chatbot's response correctly answers the question. They have provided a clear and concise definition of what a complex QA instance means, and have explained how it is handled using chatGPT/GPT-4. The chatbot has also provided an example to illustrate their point, which shows a good understanding of the concept. Overall, the chatbot's response is well-organized and informative.
    Decision:True
    ---
    
    User question: how can I train an instance based off of a websites documentation, without using PDF? could i web scrape the content and then upload that content? i am trying to ask questions based off of a websites documentation, and im not sure how to convert the data from the website easily
    Correct response: You can either create an app with an input_url this way you won't need to scrape the website https://docs.berri.ai/api-reference/endpoint/create_app if this does not work you can also manually scrape the website yourself and create an instance with raw text by passing in JSON chunks to berri
    Chatbot response:To train an instance based off of a website's documentation without using a PDF, you can scrape the content from the website and then upload it as a data source. You can use web scraping tools such as Beautiful Soup or Scrapy to extract the text from the website and then upload it using the BerriAI API. Once you have uploaded the data source, you can use it to train your instance and ask questions based on the website's documentation. However, please note that web scraping may be subject to legal restrictions, so make sure to check the website's terms of service and consult with a legal professional if necessary.
    Rationale: Based on the given question and the solution answer, the chatbot's response appears to answer the question correctly. The chatbot provided a clear and concise explanation of how to train an instance based off of a website's documentation without using a PDF. They highlighted the use of web scraping tools such as Beautiful Soup or Scrapy to extract the text from the website and then upload it using the BerriAI API. They also emphasized the need to check the website's terms of service and consult with a legal professional if necessary due to possible legal restrictions on web scraping. Overall, the chatbot's response was informative and addressed the main points of the question.
    Decision:False
    ---
    
    User question: What are the most common and unusual use of Berri AI to this day?
    Correct response: I'm sorry, but I don't have information about the most common and unusual use of Berri AI to this day. However, you can find more information about the scenarios and use cases that Berri AI supports in the API Reference and the Frequently Asked Questions sections of the Berri AI documentation.
    Chatbot response:Berri can be used for building chatbots for customer support, education tutors, content classification
    Rationale: The chatbot's response does not answer the question correctly. The response acknowledges that they do not have information about the most common and unusual use of Berri AI but instead provides information on where to find more information about the scenarios and use cases that Berri AI supports. While this information may be helpful, it does not directly address the question asked.
    Decision:False
    ---
    
    User question: {{question}}

    Correct response: {{solution_answer}}

    Chatbot response: {{model_answer}}

    Rationale: 
"""