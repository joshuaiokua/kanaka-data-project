# kanaka-data-project

This project uses Llama 3.1, AWS, and Streamlit to centralize, clean, and visualize data on Kanaka Maoli (Native Hawaiians). By transforming fragmented datasets into accessible formats, it facilitates integration with LLMs and enhances data exploration through interactive visualizations. The goal is to create a conversational interface that allows users to explore key insights and trends in real-time.

## Table of Contents

- [**Project Description and Goals**](#project-description-and-goals)
  - [Research Experiments](#research-experiments)
- [**Installation and Usage**](#installation-and-usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [**Tools**](#tools)
  - [Llama 3.1](#llama-31)
  - [LangChain](#langchain)
  - [AWS](#aws-free-tier)
  - [CockroachDB](#cockroachdb)
  - [Qdrant](#qdrant)
  - [Streamlit](#streamlit)
- [**Data**](#data)
  - [Native Hawaiian Data Book 2023](#native-hawaiian-data-book-2023)

## Project Description and Goals

This project is dedicated to centralizing and cleaning data related to Kanaka Maoli (Native Hawaiians) to make it accessible and compatible with large language model (LLM) systems. Currently, these datasets are fragmented and, when centralized, are often stored in formats (e.g., PDFs, multi-tab Excel sheets) that are challenging to use in modern data science environments. By transforming this data into more usable formats, the project not only improves user accessibility but also facilitates seamless integration with LLM systems and applications.

While LLMs are commonly recognized for their generative capabilities, I believe they hold significant potential in making interacting with data--or more broadly, knowledge domains--more engaging and dynamic. I'm enamored with this idea of data exploration being a curated yet open-ended experience, where users can interact with data in a conversational manner, asking questions and receiving insights in real-time. Almost like a choose-your-own-adventure book or a Dungeons & Dragons campaign!

By leveraging techniques like retrieval-augmented generation (RAG) and domain adaptation fine-tuning, I aim to develop a Streamlit-LLM application that allows users to interact with Kanaka Maoli data in this dynamic way—a true ["talk story"/mo'olelo](https://education.nationalgeographic.org/resource/storytelling-and-cultural-traditions/)experience.

> **Note**: This project deeply respects the original work of organizations like the Office of Hawaiian Affairs and seeks to build on their efforts, not critique them. By making the data more accessible, the project hopes to inspire more exploration of the original sources and highlight the value of the work done by these organizations.[^bignote2]

### Research Experiments

Within this project's overarching goal, I will also explore several specific ideas, listed below, which help to guide development and, as such, are likely to change as the project progresses. See `experiments/README.md` for more information.

- Optimizing Table and Column Names for LLM SQL Agent Applications
- Enhancing Data Exploration and Interactivity with LLMs
- Summarizing and Representing Numerical Data for LLM Integration
- Domain-Specific Fine-Tuning of LLMs
- Streamlining Multi-DataFrame Workflows in Jupyter Notebooks

## Installation and Usage

### Prerequisites

### Installation

### Usage

## Tools

### [Llama 3.1](https://llama.meta.com/)

Meta's newest LLM, Llama 3.1, is the primary LLM used in this project. Other models may be explored in the future. The specific models used and explored in this project are listed below, all of which are serviced by Groq.

- Meta-Llama-3.1-8B
- Meta-Llama-3.1-70B
- Meta-Llama-3.1-8B-Instruct
- Meta-Llama-3.1-70B-Instruct

### [LangChain](https://langchain.com/)

LangChain is a framework designed to simplify the development, productionization, and deployment of applications powered by large language models (LLMs). This project will use LangChain to streamline the integration of LLMs into the data exploration and visualization application, making it easier to leverage the capabilities of these models in real-time interactions with users.

### [AWS](https://aws.amazon.com/) (Free Tier)

Cloud data and model training and provision, where needed, is provided by AWS. I'm using the free tier services and any free trials they offer because I am poor :sob:. I fully understand that AWS offers better products to accomplish what I intend but alas. Listed below are the specific AWS services to be used in this project:

- **Simple Storage Service (S3)**
  - **Purpose**: Store raw and cleaned data.
  - **Note**: Functionality has already been implemented to interact with S3 but this may be revisited as the project progresses and other cloud services (e.g. Qdrant, CockroachDB) are explored and/or integrated.
- **Lambda**
  - **Purpose**: Simple serverless compute for base data processing.
- (TBD) SageMaker[^bignote3]

> **Note:** As I have a few separate projects that interact with AWS and other cloud services, I've centralized all code I've written for working with cloud services in a single repository listed in the `pyproject.toml` file as `cloudbozo`. As of now (8/24), the repository is private, but I may make it public in the future if only for the sake of transparency. I can assure you that the code is not particularly interesting and simply caters to my idiosyncrasies.

### [CockroachDB](https://www.cockroachlabs.com/)

CockroachDB is a distributed SQL database that provides consistency, scalability, and high availability. This project will use CockroachDB to store and manage the data used in the project, making it easier to access and query the data for the LLM agent.

### [Qdrant](https://qdrant.com/)

Qdrant is an open-source vector search engine that allows for the efficient storage and retrieval of high-dimensional vectors. This project will use Qdrant to store and manage the vectorized data (e.g. contextual information separate from the datasets themselves), making it easier to work with LLMs and other machine learning models. Qdrant is also already integrated into the LangChain framework, simplifying the process of working with vectorized data in the application.

### [Streamlit](https://streamlit.io/)

Streamlit is a Python library that allows for the creation of interactive web applications. This project will use Streamlit to create a web application that allows users to interact with the data conversationally, exploring key insights and trends through interactive visualizations.

## Data

See the `README.md` file in the `data` folder for more information on the data used in this project, what portion of the data has been cleaned, the intended use of the data, and the original source of the data. An overview of the data used in this project is provided below.

### [Native Hawaiian Data Book 2023](https://www.ohadatabook.com/DB2023.html)

- **Description**: The Native Hawaiian Data Book 2023 is a comprehensive collection of data on Native Hawaiians in Hawaii. The data book includes information on population, education, health, and more. This data source is an invaluable consolidation of data on Kanaka Maoli and draws from county, state, and federal databases. The full list of data sources it draws from listed [here](https://ohadatabook.com/fr_statlinks.11.html).
- **Format**: Tabbed Excel file, with each tab representing a different dataset.
- **Ownership**: The Native Hawaiian Data Book is published by the Office of Hawaiian Affairs (OHA), a public agency that serves as a resource for Native Hawaiians. The data book is compiled by the Research Division of OHA.

[^bignote2]: I do not want to take away from the incredible work done by a variety of organizations, specifically the Office of Hawaiian Affairs, and individuals to collect and present the data as I found it. My inclusion of any data source in this project is not criticism of the organization or individual that collected the data. Rather, it is an attempt to make the data more accessible and engaging for a wider audience. If anything I hope that this project will encourage more people to explore the original data sources more and show these organizations and individuals the value of their work and what can be done with it.

[^bignote3]: AWS offers a 2-month free trial for SageMaker, which I may use to fine-tune models and or deploy them. I want to wait until I have everything else organized across all my projects that could make use of this service before I start the trial, however. I may continue using SageMaker after the trial if it proves useful given the pricing for serverless inference is quite reasonable.
