from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

from qa_evaluator import QAEvaluator
from azure.ai.evaluation import BleuScoreEvaluator

# Setup Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
endpoint = os.getenv("AZURE_AI_CHAT_ENDPOINT")
key = os.getenv("AZURE_AI_CHAT_KEY")
deployment_name = "gpt-4o"
AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT")
# Initialize Azure OpenAI client
client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Initialize evaluators once
model_config = {
    "azure_endpoint": AZURE_OPENAI_ENDPOINT,
    "api_key": key,
    "azure_deployment": deployment_name
}

qa_evaluator = QAEvaluator(model_config=model_config, _parallel=True)
bleu_evaluator = BleuScoreEvaluator()


@app.route('/generate_and_evaluate', methods=['POST'])
def generate_and_evaluate():
    data = request.get_json()

    system_prompt = data.get("system_prompt")
    user_prompt = data.get("user_prompt")
    ground_truth = data.get("ground_truth", user_prompt)  # if ground_truth not given, use user_prompt

    if not system_prompt or not user_prompt:
        return jsonify({"error": "system_prompt and user_prompt are required."}), 400

    # 1. Generate Answer
    response = client.complete(
        messages=[
            SystemMessage(system_prompt),
            UserMessage(user_prompt),
        ],
        model=deployment_name
    )

    generated_answer = response.choices[0].message.content
    usage = response.usage

    # 2. Evaluate
    bleu_score = bleu_evaluator(response=generated_answer, ground_truth=ground_truth)
    qa_scores = qa_evaluator(
        query=user_prompt,
        response=generated_answer,
        context="",
        ground_truth=ground_truth
    )

    # 3. Return Results
    return jsonify({
        "generated_answer": generated_answer,
        "bleu_score": bleu_score,
        "qa_scores": qa_scores,
        "token_usage": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }
    })
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    system_prompt = data.get("system_prompt")
    user_prompt = data.get("user_prompt")

    if not system_prompt or not user_prompt:
        return jsonify({"error": "system_prompt and user_prompt are required."}), 400

    try:
        response = client.complete(
            messages=[
                SystemMessage(system_prompt),
                UserMessage(user_prompt),
            ],
            model=deployment_name
        )

        generated_answer = response.choices[0].message.content
        usage = response.usage

        return jsonify({
            "generated_answer": generated_answer,
            "token_usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)