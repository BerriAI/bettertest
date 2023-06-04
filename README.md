# bettertest 📝🔍

⚡ A Python testing library for automatically evaluating and tracing LLM applications ⚡

Our goal with bettertest is to simplify the process of testing and debugging LLM applications. It automatically evaluates your model’s responses against your solution answers (auto-eval) and provides tracing features out-of-the-box.

With bettertest, you can automatically test your LLM applications and view print statements for each run just by adding ‘bettertest’ to any print statement in your code.

## Getting Started

Before using BetterTest, you need to install it via pip:

```
pip install bettertest
```

After installation, import the BetterTest library in your Python project:

```python
from bettertest import BetterTest
```
## Using BetterTest

### Example Project

```
!pip install bettertest

from bettertest import BetterTest

questions = ['what does a complex QA instance mean?',
 'how can I train an instance based off of a websites documentation, without using PDF? could i web scrape the content and then upload that content? i am trying to ask questions based off of a websites documentation, and im not sure how to convert the data from the website easily',
 'how can i train an instance based off of a websites documentation?',
'What does the ai model see the data as? Does it see it as the large corpus of text it is trained on or something else?']

def call_openai(question):
    index = questions.index(question)

    model_answers = ['A complex QA instance refers to a type of search in which users ask questions that require multiple pieces of context. For example, if a user asks "What is the age of the actress who plays Meg in Family Guy?", the system needs to know both "Who plays Meg in Family Guy?" and "What is Mila Kunis\'s age?" to provide an accurate answer. To handle this, the user question is broken down into sub-components, and the most relevant chunks for each sub-question are found and fed into the chatGPT/GPT-4 model to get the answer.\n  \n  REFERENCES\n Discord Chat; https://docs.berri.ai/api-reference/app_configurations/file_configuration;',
 "To train an instance based off of a website's documentation without using a PDF, you can scrape the content from the website and then upload it as a data source. You can use web scraping tools such as Beautiful Soup or Scrapy to extract the text from the website and then upload it using the BerriAI API. Once you have uploaded the data source, you can use it to train your instance and ask questions based on the website's documentation. However, please note that web scraping may be subject to legal restrictions, so make sure to check the website's terms of service and consult with a legal professional if necessary.\n  \n  REFERENCES\n Discord Chat;",
 'To train an instance based off of a website\'s documentation, you can use the "Recursive URLs" feature provided by BerriAI. This feature allows you to recursively parse URLs and extract text data from them, which can then be used to train your instance. \n \n\n Here\'s an example of how you can use this feature:\n \n\n 1. First, create a data source using the "create_data_source" endpoint. You can specify the URL of the website you want to train your instance on as the "data_source" parameter. \n \n\n 2. Next, use the "create_app" endpoint to create an instance of your GPT-4 app. In the payload, specify the "data_source" parameter as the ID of the data source you created in step 1. \n \n\n 3. Finally, use the "finetune_instance" endpoint to fine-tune your instance using the data extracted from the website. You can pass in a list of JSON objects containing context and correct_response attributes to this endpoint. \n \n\n Keep in mind that the quality of the instance you train will depend on the quality of the data you extract from the website. It\'s important to ensure that the data you extract is relevant and accurate.\n  \n  REFERENCES\n Discord Chat;',
 'Hello, according to the BerriAI API documentation, the AI model sees the data as embeddings, which are numerical representations of the text. These embeddings are generated using a pre-trained language model, such as GPT-3, and are used to make predictions and generate responses. The model does not see the data as the large corpus of text it is trained on, but rather as a set of numerical vectors that represent the semantic meaning of the text.\n  \n  REFERENCES\n Discord Chat;']
    print("bettertest: testing if this works")
    return model_answers[index]

answers = ['Sometimes users ask questions that require multiple pieces of context (e.g. What is the age of the actress who plays Meg in Family Guy? -> This requires us to know - Who plays Meg in Family Guy? Mila Kunis + What is Mila Kunis’s age?). To tackle this, we first run the user question through chatGPT, and have it break down that question into sub-components (as seen in the previous example) -> Find the most relevant chunks for each sub-question -> Feed that into chatGPT/GPT-4/whichever model you chose to get the answer to the users question.',
 "You can either create an app with an input_url this way you won't need to scrape the website https://docs.berri.ai/api-reference/endpoint/create_app if this does not work you can also manually scrape the website yourself and create an instance with raw text by passing in JSON chunks to berri",
 "You can either create an app with an input_url this way you won't need to scrape the website https://docs.berri.ai/api-reference/endpoint/create_app if this does not work you can also manually scrape the website yourself and create an instance with raw text by passing in JSON chunks to berri",
 "Berri ingests your data, chunks it, creates embeddings. When user's ask questions, berri does a similarity search and retrieves the most similar chunks to answer the questions. These chunks are then fed into the llm to answer the question"]

bt = BetterTest("krrish@berri.ai", "YOUR_OPENAI_API_KEY")

bt.eval(questions, answers, call_openai)

```

### Initialize BetterTest

Create an instance of the BetterTest class with the user's email:

```python
bt = BetterTest("your_email@example.com", "your_openai_api_key")
```

Replace `"your_email@example.com"` with the appropriate email address.
Replace `"your_openai_api_key"` with your openai api key. [Here's where to find it](_https://platform.openai.com/account/api-keys_).

### Evaluate Model Responses

The `eval()` function takes in a list of questions, a list of answers, an LLM function, and an optional `num_runs` argument. It automatically evaluates the model's response against the solution answer and provides tracing for each run. Use it as follows:

```python
questions = [...]  # List of questions
answers = [...]    # List of corresponding solution answers

def llm_function(question):
    # Your custom LLM function implementation goes here
    pass

bt = BetterTest("your_email@example.com")
bt.eval(questions, answers, llm_function)
```

Replace the `llm_function` with your LLM function, and customize `num_runs` if necessary. By default, `num_runs` is set to 1.

## How does eval work?

Reliable + Fast testing is hard, and that's what we want to tackle.

Each question is evaluated 3 times. 

Each evaluation returns either True or False, along with the model's rationale for why it chose what it did. 

We pick the evaluation (True/False) that occurs most, along with the model rationale to explain reasoning. 

Each question is run in parallel and results are added to your dashboard in real-time. 


## Contributing

We welcome contributions to BetterTest! Feel free to create issues/PR's/or DM us (👋 Hi I'm Krrish - +17708783106)

## Changelog

The current version of BetterTest is `0.1.98`.

## License

BetterTest is released under the [MIT License](_https://github.com/bettertest/readme/blob/master/LICENSE_).

