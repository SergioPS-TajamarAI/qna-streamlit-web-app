from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

def load_env_variables():
    load_dotenv(override=True)
    return {
        'ai_endpoint': os.getenv('AI_SERVICE_ENDPOINT'),
        'ai_key': os.getenv('AI_SERVICE_KEY'),
        'ai_project_name': os.getenv('QA_PROJECT_NAME'),
        'ai_deployment_name': os.getenv('QA_DEPLOYMENT_NAME')
    }

def create_ai_client(ai_endpoint, ai_key):
    credential = AzureKeyCredential(ai_key)
    return QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

def get_answer_from_bot(ai_client, ai_project_name, ai_deployment_name, user_question):
    response = ai_client.get_answers(
        question=user_question,
        project_name=ai_project_name,
        deployment_name=ai_deployment_name
    )
    for answer in response.answers:
        print(f"Answer: {answer.answer}")
        print(f"Confidence: {answer.confidence}")
    return response.answers


