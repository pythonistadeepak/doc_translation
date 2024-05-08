

### [Get started](https://doctranslation-by-deepak.streamlit.app/) 

This is a web app to **Translate documents (.docx and .pdf) from Engish to German Langauge** and **Automatically download translated document upon user Submission**. 

<br> 
Technologies used to built are: 
<br>  

-  Python <br>
- [Steamlit](https://docs.streamlit.io/) framework.<br>
 NO LLM have been used in the solution

### Setup for running on local machine

Step 1:

- Open your command prompt/bash.
- Fork The Github [Repository](https://github.com/pythonistadeepak/doc_translation).
- Clone the repo from your repository use Command `git clone` repo link.
<br>


Step 2:

- Install all necessary libraries from requirements.txt
<br>


### Approach To the Solution
Before going to a solution, we need to understand the limitations:
<br>

•	**Token limitations:** A Chat-gpt3-like model has token limitations of 4096 to be precise.This means that they can only process a certain number of words at a time. This can make it difficult to summarize longer documents.
<br>

•	**Memory issues:** As with other language models, Chat GPT models may have difficulty retaining information over a long conversation or summarization task. This can lead to the model producing a summary that differs from the original text or misses important details.
<br>

•	**Hallucinations:** Chat GPT models have been known to "hallucinate" or generate text that is not directly related to the input. This can lead to inaccurate or misleading summaries.
<br>

• **Limited understanding:** Chat GPT models may struggle with understanding the context and nuances of the text, particularly in cases where the language is highly technical or specialized. This can lead to inaccurate or incomplete summaries.	These LLMs have large amounts of data from different fields and certain terminologies might mean something or a particular field and something else for the other.

### Solution
•	Our goal is to create a Summarization tool that takes the long text and gives concise output. But during summarization we do not want to hit the token limit, for we take the .txt file and **divide it into chunks** so that it fits in the **size of the token** and we embed these chunks with **openai embeddings**.

•	As these models have **memory issues** after embedding the chunks, we make a **semantic index of these embeddings** and store them in a **vector database** this can solve the memory issue.

•	As for **hallucination**, we set the **temperature** of the model at a **minimum** as we do not need much creativity and need only to summarize the given file .

•	For this issue I made the LLMs access to the **knowledge base** of the model only to return output and if some terminology is asked it will reply based on the knowledge base provided. 


### The architecture of the model
 
![](https://github.com/singhjaspreetb/Summerization-LLM/blob/master/Arch.png)     

### Usage Instruction:
1. [Go the hosted application](https://doctranslation-by-deepak.streamlit.app/)
2. Upload the file you wish to translate (Supported Formats - .docx and .pdf)
3. Wiat for a while to let the system upload your file
4. Click on SUBMIT button to translate the file
5. The translated file will be automatically downloaded to your DOWNLOAD folder
