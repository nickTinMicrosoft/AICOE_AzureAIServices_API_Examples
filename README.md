# AI Summit - App + AI Innovation - Empower Citizens with AI Powered Applications on Azure
## All code is written using Jupyter Notebooks, you will need to install the Jupyter Notebooks extension in VS Code
### Included in this Repo
Example code from MS docs Quickstarts on how to use Azure Cognitive Services APIs. 

* aoai code
    * image generation using DALL-E 3 Azure Open AI Model --- must have Azure Open AI and DALL-E model deployed

* Asynchronous API
    * Document Translator (both Async and Sync in notebook)
        * Synchronized API will read all documents in a container, within a storage account, translate them and save them to a different container.
        * Async will create a button, when clicked you can "Upload" a document, it will read document, translate and return the translated text to the output. It does not save a translated copy to anything. At this time (Jan 2025) it is only reading .txt files.
    * Text to Speech
    * Speech to Text

* Synchronous API
    * Text analysis Keywords
    * Text analysis Sentiment Analysis

### Pre Reqs
In Azure you will need the following services 

* Azure Open AI

* Azure AI Services | Azure AI services multi-service account
    Used for Text_Sentiment and Text_Keywords notebooks

* Azure AI Services | Speech Service
    Used for Speech_to_text and Text_to_Speech notebooks

* Azure AI Services | Translatator
    Used for Document_Translation notebook

Make sure to create your Pyton environment and .env files. env_example.env.txt is a sample .env file. Rename to .env and enter your Azure service information.

To create, activate and update python virtual environment
1. Open new Terminal
2. Execute the following in terminal: ``` virtualenv venv ```
    * If virtualenv is not installed you may have to pip install it ``` pip install virtualenv ```
3. Activate environment by executing the following: 
   * In Windows: ``` .\venv\Scripts\activate ```
   * In Linux or Mac:``` source venv/bin/activate ```
4. Install Required Packages:``` pip install -r requirements.txt ```

## At this time all code examples are writen in Python using Jupyter notebooks. 
## The examples provided are for learning purposes only, and are NOT concidered "Production Ready", use examples at your own risk.