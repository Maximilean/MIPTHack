from langchain.prompts import load_prompt
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents.base import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def summary(sum_llm, text):
	map_prompt = load_prompt('lc://prompts/summarize/map_reduce/map.yaml')
	combine_prompt = load_prompt('lc://prompts/summarize/map_reduce/combine.yaml')

	documents = Document(page_content=text, metadata={"source": "local"})

	text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 7000,
    chunk_overlap  = 0,
    length_function = len,
    is_separator_regex = False
    )

    documents = text_splitter.split_documents([documents])
    sum_chain = load_summarize_chain(sum_llm, chain_type="map_reduce", 
                             map_prompt=map_prompt,
                             combine_prompt=combine_prompt,
                             verbose=False)

    summary = sum_chain.invoke({"input_documents": documents})

    return summary 

