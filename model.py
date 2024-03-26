import logging
import os
import json

import boto3
from langchain.prompts import PromptTemplate
from langchain.llms.bedrock import Bedrock

from prompt_template.prompt import *

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class BedrockModel:

    def __init__(self):
        logger.info("Initializing Bedrock client....")
        print("Model")
        self.bedrock_client = boto3.client(service_name='bedrock-runtime')

    def generate_content(self, request_params):
        payload = self.construct_payload(request_params)
        logger.info(f"Invoking {os.environ['MODEL_NAME']} Model")
        response = self.bedrock_client.invoke_model(**payload)

        response_body = json.loads(response.get('body').read())
        print(response_body)
        return response_body

    def construct_payload(self, params):

        prompt_template = get_prompt(params)
        prompt = PromptTemplate(
            input_variables=["structured_markup", "words", "keywords", "grade_level"], template=prompt_template
        )

        print(prompt)

        payload = {
            "modelId": os.environ['MODEL_NAME'],
            "contentType": os.environ['CONTENT_TYPE'],
            "accept": os.environ['ACCEPT'],
            "body": json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"{prompt}"
                            }
                        ]
                    }
                ],
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 8000,
                "temperature": 1,
                "top_k": 250,
                "top_p": 0.999,
                "stop_sequences": []
            })
        }

        return payload
