# Stats_Chatbot

## Overview
This repository contains the source code for a chatbot that understands PDF documents uploaded by users and provides answers based on the data extracted from the PDFs. The chatbot leverages FAISS (Facebook AI Similarity Search) vector database for efficient similarity search and utilizes Google Flan model for training and generating responses.

## Features
- Upload PDF documents for analysis.
- Extract relevant information from PDFs using NLP techniques.
- Train and fine-tune the chatbot model using Google Flan.
- Use FAISS vector database for fast and efficient similarity search.
- Provide responses based on the content of uploaded PDFs.

## Installation
- Clone the repository:
- Install the required dependencies
```
pip install -r requirements.txt
```
## Usage
- Run the main script to start the chatbot application:
```
python app.py
```
- Add files to the pdf uploaded and click `Process`
- Once processing is done ask the questions to the chatbot
