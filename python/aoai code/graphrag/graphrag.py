import os
import io
import json
import time
import requests
import random
import uuid
import shutil
import zipfile
from collections import OrderedDict
import urllib.request
from tqdm import tqdm

from typing import List

from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from operator import itemgetter

from common.utils import upload_file_to_blob, extract_zip_file, upload_directory_to_blob
from common.utils import parse_pdf, read_pdf_files
from common.prompts import DOCSEARCH_PROMPT_TEXT
from common.utils import CustomAzureSearchRetriever


from IPython.display import Markdown, HTML, display  

from dotenv import load_dotenv
load_dotenv()


### this is how to use GraphRag with Lang Chain library
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_experimental.graph_transformers import LLMGraphTransformer
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader,  PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
# from neo4j import GraphDatabase
import logging
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders.text import TextLoader

# load_dotenv(find_dotenv('.env'), override=True)
 
 
neo4j_uri =  os.environ["NEO4J_URI"] 
neo4j_username = os.environ["NEO4J_USERNAME"] 
neo4j_password = os.environ["NEO4J_PASSWORD"] 
 
llm = AzureChatOpenAI(
        azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT'],
        azure_deployment="gpt-4o",
        api_key=os.environ['AZURE_OPENAI_API_KEY'],
        api_version=os.environ['AZURE_OPENAI_API_VERSION'],
)
 
llm_transformer = LLMGraphTransformer(llm=llm)
 
embeddings = AzureOpenAIEmbeddings(deployment="text-embedding-ada-002", model="text-embedding-ada-002", chunk_size=10)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
sem_text_splitter = SemanticChunker(
   embeddings, breakpoint_threshold_type="interquartile"
)
 
vector_index = Neo4jVector.from_existing_graph(
    embeddings,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

graph = Neo4jGraph(refresh_schema=False)
 
text = """
The Fundamental Principles of Classical Mechanics
Classical mechanics is one of the foundational pillars of physics, providing a systematic framework for understanding the motion of objects under the influence of forces. Rooted in centuries of observation, experimentation, and mathematical formulation, classical mechanics has been instrumental in shaping our understanding of the natural world and has practical applications in engineering, astronomy, and various fields of technology.
 
At its core, classical mechanics is governed by the principles established by Sir Isaac Newton, whose three laws of motion provide a comprehensive description of how objects behave when subjected to external forces. These laws, along with additional concepts such as energy conservation, momentum, and rotational dynamics, form the basis of what is often referred to as Newtonian Mechanics.
 
1. Newton's Laws of Motion
Newton's three laws of motion serve as the cornerstone of classical mechanics. These laws describe the fundamental relationship between an object's motion and the forces acting upon it.
 
First Law: The Law of Inertia
Statement: An object at rest stays at rest, and an object in motion continues in uniform motion with the same speed and in the same direction unless acted upon by an external force.
 
This law, first conceptualized by Galileo Galilei, establishes the concept of inertia—the tendency of an object to resist changes in its motion. In a frictionless environment, an object will move indefinitely at constant velocity unless disturbed by an external force. This contradicts the Aristotelian notion that force is always required to maintain motion.
 
Example: A spacecraft moving through deep space at constant velocity will continue indefinitely unless acted upon by gravitational forces or collisions with other objects.
 
Second Law: The Law of Acceleration
Statement: The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. Mathematically, this is expressed as:
 

F is the net force applied to the object,
 
m is the mass of the object,
 
a is the resulting acceleration.
This equation quantifies how forces affect motion. A larger force results in greater acceleration, and a larger mass requires more force to achieve the same acceleration.
 
 
This law is critical in predicting the motion of objects under various forces, whether it be a falling apple or a car accelerating on a highway.
 
Third Law: Action and Reaction
Statement: For every action, there is an equal and opposite reaction.
 
This principle emphasizes that forces always occur in pairs. If object A exerts a force on object B, object B simultaneously exerts a force of equal magnitude but in the opposite direction on object A.
 
Example: When a person jumps off a boat, they push the boat backward while propelling themselves forward.
 
This law is crucial in understanding interactions such as rocket propulsion, where exhaust gases are expelled backward, producing thrust that propels the rocket forward.
2. Conservation Laws in Classical Mechanics
Beyond Newton's laws, classical mechanics is also governed by fundamental conservation principles that describe quantities that remain constant in a system, provided no external forces interfere.
Conservation of Momentum
Momentum (
p is defined as the product of an object's mass and velocity:
p=mv
The law of conservation of momentum states that in an isolated system (one with no external forces), the total momentum before and after a collision remains constant.
This principle is crucial in analyzing collisions in physics, whether they be elastic (kinetic energy is conserved) or inelastic (kinetic energy is not conserved).
Example: When two ice skaters push off each other, they move in opposite directions with momenta that are equal in magnitude but opposite in direction.
Conservation of Energy
Energy exists in various forms, but in mechanics, we primarily deal with kinetic energy (
KE and potential energy
PE.
Kinetic Energy: The energy of motion
Potential Energy: The energy stored due to position (e.g., gravitational potential energy)
PE=mgh
The law of conservation of energy states that in an isolated system, the total energy remains constant:
This principle underlies much of classical physics, explaining phenomena from pendulum motion to roller coaster dynamics.
Example: A ball dropped from a height converts gravitational potential energy into kinetic energy as it falls.
Work-Energy Theorem
The work-energy theorem states that the work (
Work done on an object is equal to the change in its kinetic energy:
This concept is particularly useful in understanding how forces influence the motion of objects.
Example: When a car brakes, friction does work on the car, reducing its kinetic energy and bringing it to a stop.
3. Rotational Motion and Dynamics
Classical mechanics also extends to rotational motion, which follows principles analogous to linear motion.
Torque and Angular Momentum
Torque is The rotational equivalent of force
The law of conservation of angular momentum explains why figure skaters spin faster when they pull their arms inward.
4. Applications and Limitations of Classical Mechanics
Applications
Classical mechanics governs a vast range of phenomena, including:
Projectile motion (ballistics, sports physics)
Orbital mechanics (planetary motion, satellites)
Engineering mechanics (bridge construction, vehicle dynamics)
Biomechanics (motion of limbs, joint stress analysis)
Limitations
Despite its success, classical mechanics has its limits:
It fails at very high speeds approaching the speed of light, where relativistic mechanics (Einstein's theory of relativity) takes over.
It fails at microscopic scales, where quantum mechanics is required.
Conclusion
Classical mechanics remains one of the most fundamental and widely applicable branches of physics.
Rooted in Newton's three laws,
it describes the motion of objects with remarkable precision, providing
the foundation for engineering, astronomy, and countless technological advancements.
While it has been superseded in extreme conditions by relativity and quantum mechanics,
its principles remain indispensable in understanding the macroscopic world.
"""

file_path = "classical_mechanics.txt"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(text)

# Load the file using TextLoader
loader = TextLoader(file_path, encoding="utf-8")
docs = loader.load()


# loader = TextLoader(text, encoding="utf-8")
# docs = loader.load()
text_splitter=RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
documents = text_splitter.split_documents(docs)

graph_documents = llm_transformer.convert_to_graph_documents(documents)
print(f"Nodes:{graph_documents[0].nodes}")
print(f"Relationships:{graph_documents[0].relationships}")

graph.add_graph_documents(graph_documents, baseEntityLabel=True, include_source=True)
 
vector_retriever = vector_index.as_retriever()
 
def graph_retriever(question: str):
    vector_data = [el.page_content for el in vector_retriever.invoke(question)]
    final_data = f"""
    vector data:
    {"#Document ".join(vector_data)}
    """
    return final_data
 
question = "How is Newton's Third Law related to Principles of Mechanics?"
 
template = """Answer the question based only on the following context:
{context}
 
Question: {question}
Use natural language and be concise.
Answer:"""
 
prompt = ChatPromptTemplate.from_template(template)
 
chain = (
    {
        "context": graph_retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)
 
response =chain.invoke(input = question)
 
print(response)
 