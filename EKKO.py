#!/usr/bin/env python
# coding: utf-8

# In[24]:


from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredURLLoader
from dotenv import load_dotenv
import os
import textwrap
import csv
import pandas as pd
from transformers import pipeline


# In[31]:


load_dotenv()
OPENAI_API_KEY = "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"

# question = input("Input your question for ChatGPT: ")
# answer = llm(question)
# print(answer)

try:
    #Load URL data into Text
    url = "http://www.paulgraham.com/newideas.html"
    loader = UnstructuredURLLoader(urls=[url])
    data = loader.load()   
    #Build LLM
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)
    #Build Prompt
    prompt_template = """Write a summary of the key points of the following article in 100 words or less:

        {text}

    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
    #Cut Data into Chunks
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 256,
    chunk_overlap  = 20,
    length_function = len,
    )
    
    docs = text_splitter.create_documents([str(data)])
    #Create Chain and Run
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    summary = chain.run(docs)
    print(summary)
    with open('mentalmapM.csv', 'a', newline='') as file:
        EXISTING = False
        writer = csv.writer(file)
        with open('mentalmapM.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == url:
                    EXISTING = True
        if not EXISTING:
            writer.writerow([url, summary])

except Exception as err:
    print(err)


# In[32]:


with open("mentalmapM.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        print(row)


# In[2]:


def TakeSummary(url):
    try:
        #Load URL data into Text
        loader = UnstructuredURLLoader(urls=[url])
        data = loader.load()   
        #Build LLM
        llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo', openai_api_key=OPENAI_API_KEY)
        #Build Prompt
        prompt_template = """Write a summary of the key points of the following article in 100 words or less:

            {text}

        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        #Cut Data into Chunks
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 256,
        chunk_overlap  = 20,
        length_function = len,
        )

        docs = text_splitter.create_documents([str(data)])
        #Create Chain and Run
        chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
        summary = chain.run(docs)
        print(summary)
        return (summary)

    except Exception as err:
        print(err)


# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
# 
# ARTICLE = """ New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
# A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
# Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
# In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
# Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
# 2010 marriage license application, according to court documents.
# Prosecutors said the marriages were part of an immigration scam.
# On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
# After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
# Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
# All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
# Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
# Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
# The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
# Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
# Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
# If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
# """
# print(summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False))
# 

# In[ ]:




