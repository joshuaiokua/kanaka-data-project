# kanaka-data-project

An ongoing project using Llama 3.1, AWS, and Streamlit to clean, unify, and visualize Native Hawaiian data. Analyzes data from multiple sources, highlighting key insights and trends through interactive visualizations. The various datasets used in this project are list below.

## Table of Contents

- [**Project Description and Goals**](#project-description-and-goals)
  - [Research Experiments](#research-experiments)
- [**Installation and Usage**](#installation-and-usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [**Tools**](#tools)
  - [Llama 3.1](#llama-31)
  - [AWS](#aws-free-tier)
  - [Qdrant](#qdrant)
  - [Streamlit](#streamlit)
- [**Data**](#data)
  - [Native Hawaiian Data Book 2023](#native-hawaiian-data-book-2023)

## Project Description and Goals

This project aims to centralize, clean, and make data on Kanaka Maoli (Native Hawaiians) more accessible and interactive. Currently, these datasets are scattered and, where centralized, often stored in formats (e.g. PDFs, tabbed Excel sheets, etc.) that are difficult to use in modern data science environments. The goal is to not only make the data more accessible for data scientists and researchers but also make it more interactive to help a wider audience understand and explore data on Kanaka Maoli. All data sources used are listed in this document's [Data section](#data) and the original, unprocessed data is stored in the `data` folder.[^bignote1]

This project respects the original work of organizations like the Office of Hawaiian Affairs and seeks to build on their efforts, not critique them. By making the data more accessible, the project hopes to inspire more exploration of the original sources and highlight the value of the work done by these organizations.[^bignote2]

### Research Experiments

Within this project's overarching goal, I will also explore several specific ideas, listed below, which help to guide development and, as such, are likely to change as the project progresses. See `experiments/README.md` for more information.

- Question-Answering Over Numerical Datasets
- Vectorizing Numerical Data for LLMs
- Leveraging LLMs to Expand Data Interactivity
- Fine-Tuning LLMs for Population Data

### **Working With Tabbed Excel Files**

- **Methodology:** Many datasets, such as those provided in the Native Hawaiian Data Book 2023 (described in the [data](#data) section), are stored in tabbed Excel files, which present challenges for data manipulation. This project will investigate the best approaches for cleaning and unifying this data while preserving its original tabular structure and making it more compatible with modern data science tools.
- **Tracking Cleaning Progress:** A key consideration is how to effectively track the progress of cleaning and unifying large datasets, such as the Native Hawaiian Data Book 2023, which contains over 100 tabs of data. The project will develop methods for easily identifying which data has been processed and what still needs attention.

### **Expanding Data Interactivity**

- **LLM Application:** The project will explore how to leverage Llama 3.1 to create interactive visualizations that allow users to engage with the data conversationally, enhancing traditional data visualizations. The goal is to identify or develop methodologies and frameworks that facilitate this kind of interactivity.

## Installation and Usage

### Prerequisites

### Installation

### Usage

## Tools

### [Llama 3.1](https://llama.meta.com/)

Meta's newest LLM, Llama 3.1, is the primary LLM used in this project. Other models may be explored in the future. The specific models used and explored in this project are listed below:

- Meta-Llama-3.1-8B
- Meta-Llama-3.1-70B
- Meta-Llama-3.1-8B-Instruct
- Meta-Llama-3.1-70B-Instruct

### [AWS](https://aws.amazon.com/) (Free Tier)

Cloud data and model training and provision, where needed, is provided by AWS. I'm using the free tier services and any free trials they offer because I am poor :sob:. I fully understand that AWS offers better products to accomplish what I intend but alas. Listed below are the specific AWS services to be used in this project:

- S3
- Lambda
- (TBD) DynamoDB or RDS
- (TBD) SageMaker[^bignote3]

> **Note:** As I have a few separate projects that interact with AWS, I've centralized all code I've written for AWS in a single repository listed in the `pyproject.toml` file as `awshucks`. As of now (8/24), the repository is private, but I may make it public in the future if only for the sake of transparency. I can assure you that the code is not particularly interesting and simply caters to my idiosyncrasies.

### [Qdrant](https://qdrant.com/)

Qdrant is an open-source vector search engine that allows for the efficient storage and retrieval of high-dimensional vectors. This project will explore the effectiveness of vectorizing numerical data for hybrid model RAG.

### [Streamlit](https://streamlit.io/)

Streamlit is a Python library that allows for the creation of interactive web applications. This project will use Streamlit to create interactive visualizations of the data, making it more accessible and engaging for users.

## Data

See the `README.md` file in the `data` folder for more information on the data used in this project, what portion of the data has been cleaned, the intended use of the data, and the original source of the data. An overview of the data used in this project is provided below.

### [Native Hawaiian Data Book 2023](https://www.ohadatabook.com/DB2023.html)

- **Description**: The Native Hawaiian Data Book 2023 is a comprehensive collection of data on Native Hawaiians in Hawaii. The data book includes information on population, education, health, and more. This data source is an invaluable consolidation of data on Kanaka Maoli and draws from county, state, and federal databases. The full list of data sources it draws from listed [here](https://ohadatabook.com/fr_statlinks.11.html).
- **Format**: Tabbed Excel file, with each tab representing a different dataset.
- **Ownership**: The Native Hawaiian Data Book is published by the Office of Hawaiian Affairs (OHA), a public agency that serves as a resource for Native Hawaiians. The data book is compiled by the Research Division of OHA.

[^bignote1]: I may revisit the idea of storing all unprocessed data in the `data` folder. This may not be the best approach, as the data may, at some point, be too large to store in a GitHub repository. Storing in a cloud service like AWS may be a better approach or else simply pointing to the data source in the project and leaving it at that. I would like to prove some sense of data integrity, however, so I will likely store the data in the `data` folder until I can find a better solution.

[^bignote2]: I do not want to take away from the incredible work done by a variety of organizations, specifically the Office of Hawaiian Affairs, and individuals to collect and present the data as I found it. My inclusion of any data source in this project is not criticism of the organization or individual that collected the data. Rather, it is an attempt to make the data more accessible and engaging for a wider audience. If anything I hope that this project will encourage more people to explore the original data sources more and show these organizations and individuals the value of their work and what can be done with it.

[^bignote3]: AWS offers a 2-month free trial for SageMaker, which I may use to fine-tune models and or deploy them. I want to wait until I have everything else organized across all my projects that could make use of this service before I start the trial, however. I may continue using SageMaker after the trial if it proves useful given the pricing for serverless inference is quite reasonable.
