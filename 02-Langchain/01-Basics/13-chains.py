from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini", model_provider="openai")
analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")
chain = analysis_prompt

composed_chain_with_lambda = (
    chain
    | (lambda input: {"joke": input})
    | analysis_prompt
    | model
    | StrOutputParser()
)

reply = composed_chain_with_lambda.invoke({"joke": "beets"})
print(reply)
