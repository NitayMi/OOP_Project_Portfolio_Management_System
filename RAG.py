from langchain.llms import Ollama
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

llm = Ollama(model="deepseek-r1:7b", base_url="http://127.0.0.1:11434")

embed_model = OllamaEmbeddings(
    model="deepseek-r1:7b",
    base_url='http://127.0.0.1:11434'
)

text = """
    In the lush canopy of a tropical rainforest, two mischievous monkeys, Coco and Mango, swung from branch to branch, their playful antics echoing through the trees. They were inseparable companions, sharing everything from juicy fruits to secret hideouts high above the forest floor. One day, while exploring a new part of the forest, Coco stumbled upon a beautiful orchid hidden among the foliage. Entranced by its delicate petals, Coco plucked it and presented it to Mango with a wide grin. Overwhelmed by Coco's gesture of friendship, Mango hugged Coco tightly, cherishing the bond they shared. From that day on, Coco and Mango ventured through the forest together, their friendship growing stronger with each passing adventure. As they watched the sun dip below the horizon, casting a golden glow over the treetops, they knew that no matter what challenges lay ahead, they would always have each other, and their hearts brimmed with joy.
    """

text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128)
chunks = text_splitter.split_text(text)

vector_store = Chroma.from_texts(chunks, embed_model)

retriever = vector_store.as_retriever()
retrieval_qa_chat_prompt = PromptTemplate(
    input_variables=["query"],
    template="Please provide the names of the monkeys and their habitat."
)

llm_chain = LLMChain(
    llm=llm, prompt=retrieval_qa_chat_prompt
)

chain = RetrievalQA(combine_documents_chain=llm_chain, retriever=retriever)

response = chain.run({"query": retrieval_qa_chat_prompt})

print(response['answer'])