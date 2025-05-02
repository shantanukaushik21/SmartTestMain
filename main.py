import openai
import os
from dotenv import load_dotenv
from prompts import system_prompt, user_prompt

# # Load API key from .env file (if using dotenv)
# load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# print()
# # Initialize OpenAI client
# client = openai.OpenAI(api_key=OPENAI_API_KEY)

# # Make an API call
# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",  # Change from gpt-4 to gpt-3.5-turbo
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content":user_prompt }
#     ],
#     temperature=0.7
# )

# print(response.choices[0].message.content)


# def sample_chat_completions():
#     import os
#     # Load API key from .env file (if using dotenv)
#     load_dotenv()
#     AZURE_AI_CHAT_ENDPOINT = os.getenv("AZURE_AI_CHAT_ENDPOINT")
#     AZURE_AI_CHAT_KEY = os.getenv("AZURE_AI_CHAT_KEY")
#     model_name = "gpt-4o"
#     try:
#         endpoint = os.environ["AZURE_AI_CHAT_ENDPOINT"]
#         key = os.environ["AZURE_AI_CHAT_KEY"]
#     except KeyError:
#         print("Missing environment variable 'AZURE_AI_CHAT_ENDPOINT' or 'AZURE_AI_CHAT_KEY'")
#         print("Set them before running this sample.")
#         exit()

#     # [START chat_completions]
#     from azure.ai.inference import ChatCompletionsClient
#     from azure.ai.inference.models import SystemMessage, UserMessage
#     from azure.core.credentials import AzureKeyCredential

#     client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

#     response = client.complete(
#         messages=[
#             SystemMessage(system_prompt),
#             UserMessage(user_prompt),
#         ],
#         model=model_name
#     )

#     print(response.choices[0].message.content)
#     print(f"\nToken usage: {response.usage}")
#     # [END chat_completions]


# if __name__ == "__main__":
#     sample_chat_completions()


# import os
# from dotenv import load_dotenv
# from prompts import system_prompt, user_prompt

# from azure.ai.inference import ChatCompletionsClient
# from azure.ai.inference.models import SystemMessage, UserMessage
# from azure.core.credentials import AzureKeyCredential

# from azure.ai.evaluation import AzureOpenAIModelConfiguration
# from qa_evaluator import QAEvaluator  # Adjust import as needed


# def sample_chat_completions_and_evaluate():
#     # Load environment variables
#     load_dotenv()
#     endpoint = os.getenv("AZURE_AI_CHAT_ENDPOINT")
#     key = os.getenv("AZURE_AI_CHAT_KEY")

#     if not endpoint or not key:
#         print("Missing endpoint or key in environment variables.")
#         exit()

#     # Set up the model config for evaluation
#     # model_config = AzureOpenAIModelConfiguration(
#     #     azure_deployment="gpt-4o",  # Change if your deployment name differs
#     #     azure_endpoint=endpoint,
#     #     azure_api_key=key,
#     # )


#     model_config = {
#         "api_key": key,
#         "api_version": "2023-12-01-preview",  # or your Azure OpenAI version
#         "endpoint": endpoint,
#         "deployment": "gpt-4o"  # <- IMPORTANT: must match your deployment name exactly
#     }


#     # Set up chat completions client
#     client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

#     # Generate response
#     response = client.complete(
#         messages=[
#             SystemMessage(system_prompt),
#             UserMessage(user_prompt),
#         ],
#         model="gpt-4o"
#     )

#     generated_answer = response.choices[0].message.content
#     print("\nGenerated Answer:\n", generated_answer)
#     print(f"\nToken Usage: {response.usage}")

#     # -------------------------
#     # Evaluation Section
#     # -------------------------

#     # Define the context and ground truth (this might come from a dataset or be hardcoded for now)
#     context = "Any background knowledge you fed the model during prompt or sample input data."  # optional
#     ground_truth = "Expected test cases for the given user story."  # You can refine this

#     # Initialize evaluator
#     evaluator = QAEvaluator(model_config=model_config, _parallel=True)  # Parallel for performance

#     # Run evaluation
#     scores = evaluator(
#         query=user_prompt,
#         response=generated_answer,
#         context=context,
#         ground_truth=ground_truth,
#     )

#     # Print evaluation results
#     print("\n--- Evaluation Metrics ---")
#     for metric, score in scores.items():
#         print(f"{metric}: {score}")


# if __name__ == "__main__":
#     sample_chat_completions_and_evaluate()



from dotenv import load_dotenv
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from prompts import system_prompt, user_prompt
from qa_evaluator import QAEvaluator  # Import the class you pasted above
from azure.ai.evaluation import BleuScoreEvaluator




def sample_chat_completions_and_evaluate():
    load_dotenv()
    endpoint = os.getenv("AZURE_AI_CHAT_ENDPOINT")
    key = os.getenv("AZURE_AI_CHAT_KEY")
    deployment_name = "gpt-4o"
    AZURE_OPENAI_ENDPOINT=os.getenv("AAZURE_OPENAI_ENDPOINT")

    # os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
    os.environ["AZURE_DEPLOYMENT_NAME"] = "gpt-4o"
    # os.environ["AZURE_API_VERSION"] = azure_openai_api_version
    os.environ["AZUREML_EVALUATION_API_KEY"] = key

    os.environ["AZURE_CLIENT_ID"] = "asst_AN372bQcCYdTh69IDUoxCU5w"
    os.environ["AZURE_TENANT_ID"] = "b9c426c9-72ba-4e20-8815-372b2d87f31d"
    os.environ["AZURE_CLIENT_SECRET"] = key


    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    # 1. Generate response
    response = client.complete(
        messages=[
            SystemMessage(system_prompt),
            UserMessage(user_prompt),
        ],
        model=deployment_name
    )

    generated_answer = response.choices[0].message.content
    print("\nGenerated Answer:\n", generated_answer)
    print(f"\nToken Usage: {response.usage}")

    

    # # 2. Evaluation model config
    # model_config = {
    #     "api_key": key,
    #     "api_version": "2023-12-01-preview",  # Adjust if needed
    #     "endpoint": endpoint,
    #     "deployment": deployment_name
    # }

# https://smarttesthub2117192922.openai.azure.com/
    model_config = {
       "azure_endpoint": AZURE_OPENAI_ENDPOINT,
       "api_key": key,
       "azure_deployment": deployment_name
   }


    # 3. Set evaluation inputs
    context = "Context if any or keep it empty for now"
    ground_truth = "Expected answer or sample test cases you want to compare against"

    evaluator = QAEvaluator(model_config=model_config, _parallel=True)

    bleu_evaluator = BleuScoreEvaluator()
    print(bleu_evaluator(response=generated_answer, ground_truth=user_prompt))

    # 4. Evaluate
    scores = evaluator(
        query=user_prompt,
        response=generated_answer,
        context=context,
        ground_truth=user_prompt
    )

    # 5. Print metrics
    print("\n--- Evaluation Results ---")
    for metric, score in scores.items():
        print(f"{metric}: {score}")


if __name__ == "__main__":
    sample_chat_completions_and_evaluate()
