# import streamlit as st
# # from streamlit_extras.add_vertical_space import add_vertical_space
# from PyPDF2 import PdfReader
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # sidebar
# with st.sidebar:
#     st.title('Cream Cheese Chat App with PDF')
#     st.markdown('''
#         ## About
#         You are welcome to LLM Chat Bot built with Bagel finetuned model:
#         -[Bagel](https://bagel.net)
                    
#     ''')
#     st.markdown ('''
#         ## Team Members
#         Here we are:
#         - [Halo](https://twitter.com)
#         - [Emmanuel](https://twitter.com)
#         - [Wani](https://twitter.com)
#         - [sukrutudilr](https://twitter.com)    
#     ''')
#     # add_vertical_space(4)
#     st.write('Created by Team Cheese')
    
    
# def main():
#     st.header('Chat with your PDF my dear friend!')
#     upload_file = st.file_uploader('Upload your file', type='pdf')
    
#     if upload_file is not None:
#         pdfreader = PdfReader(upload_file)
#         st.write(pdfreader)
#         # extract the content of the pdf
#         text = ''
#         for page in pdfreader.pages:
#             text += page.extract_text()
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size = 1000,
#             chunk_overlap = 200,
#             length_function = len
#         )
#         chunks = text_splitter.split_text(text=text)
#         st.write(chunks)

# if __name__ == "__main__":
#     main()
            

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os
import hashlib
from load_transformers import generate_response



# Sidebar
with st.sidebar:
    st.title('Cream Cheese Chat App with PDF')
    st.markdown('''
        ## About
        You are welcome to LLM Chat Bot built with Bagel finetuned model:
        -[Bagel](https://bagel.net)
                    
    ''')
    st.markdown ('''
        ## Team Members
        Here we are:
        - [Halo](https://twitter.com)
        - [Emmanuel](https://twitter.com)
        - [Wani](https://twitter.com)
        - [sukrutudilr](https://twitter.com)    
    ''')
    st.write('Created by Team Cheese')
    
    st.write('Clear logged file')
    

    
# clear log file
def clear_log(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write('')

# calculates file hash to check if file has been uplaoded and finetuned before        
def calculate_file_hash(uploaded_file):
    """Calculate the SHA256 hash of the uploaded file."""
    hasher = hashlib.sha256()
    chunk_size = 8192  # Read file in chunks
    while True:
        chunk = uploaded_file.read(chunk_size)
        if not chunk:
            break
        hasher.update(chunk)
    # Reset file position for potential further use
    uploaded_file.seek(0)
    return hasher.hexdigest()

# check if file is processed
def is_file_processed(file_name, file_hash, log_file_path):
    """Check if the file or content has been processed."""
    if not os.path.exists(log_file_path):
        return False

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            logged_name, logged_hash = line.strip().split('\t')
            if file_name == logged_name and file_hash == logged_hash:
                return True
    return False

# log processed file
def log_processed_file(file_name, file_hash, log_file_path):
    """Log the file name and hash."""
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"{file_name}\t{file_hash}\n")


# main function to be ran
def main(log_file_path):
    
    st.header('Chat with your PDF my dear friend!')
    upload_file = st.file_uploader('Upload your file', type='pdf')
    
    st.title('Log File Manager')

    log_file_path = '/content/pdf_chat_assistant/processed_files.log'

    # Button to clear the log file
    if st.button('Clear Log'):
        clear_log(log_file_path)
        st.success(f'Log file: \t{log_file_path} has been cleared.')
    
    # Display the content of the log file (optional)
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()
        st.text_area('Log File Content:', log_content, height=200)
    else:
        st.write(f'Log file: {log_file_path} does not exist.')
    
    
    # check if file has been uplaoded and proceed
    if upload_file is not None:
        # Ensure file is at the beginning of the stream
        upload_file.seek(0)
        pdfreader = PdfReader(upload_file)
        
        # checking wether file is processed.
        file_name = upload_file.name
        file_hash = calculate_file_hash(upload_file)
        
        if is_file_processed(file_name, file_hash, log_file_path):
            st.warning(f"File {file_name} with the same content has already been processed. Use another file or clear log file: \tSkipping...")
        else:

        # Initialize empty text string
            text = ''
            
            # Extract text from all pages
            for page in pdfreader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    st.warning(f"Could not extract text from some pages.")
            
            # Split the text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 1000,
                chunk_overlap = 200,
                length_function = len
            )
            chunks = text_splitter.split_text(text)
            
            st.write("Extracted and split text:")
            st.write(chunks)
            
            
            
            # Converting text into .parquet file for finetuning purpose
            df = pd.DataFrame(chunks, columns=['text'])

            # Drop rows that are now empty
            df = df[df['text'] != '\n']

            # Reset index after dropping rows
            df = df.reset_index(drop=True)
            df.head()
            table = pa.Table.from_pandas(df)

            # Write to Parquet file
            pq.write_table(table, '/content/pdf_chat_assistant/generated_from_txt.parquet')
            
            # Read back the Parquet file to verify
            read_df = pd.read_parquet('/content/pdf_chat_assistant/generated_from_txt.parquet')
            st.write(read_df.head())
            
            # Log the processed file
            log_processed_file(file_name, file_hash, log_file_path)
            st.write(f"File {file_name} processed and logged.")
            

def chatbot():
    st.write("Chatbot: Hello! I'm your AI assistant. How can I help you today? (Type 'quit' to exit)")

    while True:
        conversation = ''
        user_input = st.text_input("You: ").strip()

        
        if user_input.lower() == 'quit':
            st.write("Chatbot: Goodbye! Have a great day!")
            break
        
        st.write(user_input)
        
        conversation = f"{user_input}\n"
        response = generate_response(conversation)
        st.write("Chatbot:", response)          
      

if __name__ == "__main__":
    log_file_path = '/content/pdf_chat_assistant/processed_files.log'
    
    main(log_file_path)
    chatbot()
