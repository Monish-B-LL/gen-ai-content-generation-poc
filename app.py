import logging
import os

from flask import Flask, request, jsonify

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from model import BedrockModel
from utils.jira import create_jira_task
from utils.html_processor import get_title
import os

app = Flask(__name__)

logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/generate_content', methods=['POST'])
def process_pdf():
    request_json = request.json
    print(request_json)

    if not request_json:
        return jsonify({"Status": 400, "Message": "Bad Request"}), 400
    try:
        model = BedrockModel()

        result = model.generate_content(request_json)

        html_content = "\n".join(result['content'][0]['text'].replace("\n", "").split(":")[1:])
        title = get_title(html_content)
        if title is None:
            title = os.environ['KEYWORDS'].split(",")[0]
        create_jira_task(html_content, title)

        return jsonify({"content": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
