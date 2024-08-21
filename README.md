# kanaka-data-project
An ongoing project using Llama 3.1, AWS, and Streamlit to clean, unify, and visualize Native Hawaiian data. Analyzes data from multiple sources, highlighting key insights and trends through interactive visualizations. The various datasets used in this project are list below.

## Table of Contents
- [**Project Description and Goals**](#project-description-and-goals)
  - [Working With Tabbed Excel Files](#working-with-tabbed-excel-files)
  - [Expanding Data Interactivity](#expanding-data-interactivity)
- [**Installation and Usage**](#installation-and-usage)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Usage](#usage)
- [**Tools**](#tools)
   - [Llama 3.1](#llama-31)
   - [AWS](#aws-free-tier)
   - [Streamlit](#streamlit)
- [**Data**](#data)
   - [Native Hawaiian Data Book 2023](#native-hawaiian-data-book-2023)

## Project Description and Goals

The primary goal of this project is to clean, unify, and make data on Kanaka Maoli (Native Hawaiians) more accessible and interactive. Currently, these datasets are often scattered, difficult to access, and frequently stored in formats like PDFs or tabbed Excel sheets that are not easily machine-readable. This project seeks to address these challenges by creating a centralized repository of Kanaka Maoli data that can be easily used in modern data science and research projects. The repository will not only make the data easily accessible for data scientists and researchers but will also enhance interactivity to help a wider audience understand and explore the data. Given the complexity and scattered nature of the data, this will be a slow and ongoing process. All data sources used are listed under [data](#data) and the original, unprocessed data is stored in the `data` folder.[^bignote]

I want to emphasize that this project is not just about data cleaning and unification but also about making the data more engaging and accessible to a wider audience. I do not want to take away from the incredible work done by a variety of organizations, specifically the Office of Hawaiian Affairs, and individuals to collect and present the data as I found it. My inclusion of any data source in this project is not criticism of the organization or individual that collected the data. Rather, it is an attempt to make the data more accessible and engaging for a wider audience. If anything I hope that this project will encourage more people to explore the original data sources more and show these organizations and individuals the value of their work and what can be done with it.

Within this overarching goal, the project will also explore several specific questions. These questions are dynamic and will evolve as the project progresses. Current areas of focus include:

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
Cloud data and model storage, where needed, is provided by AWS. The free tier is used because I am poor :sob:. I fully understand that storing and servicing models using the free tier services is not optimal and that AWS offers more powerful services for a price (e.g. SageMaker). Listed below are the specific AWS services to be used in this project:
 - S3
 - Lambda
 - DynamoDB or RDS (TBD)

### [Streamlit](https://streamlit.io/)
Streamlit is a Python library that allows for the creation of interactive web applications. This project will use Streamlit to create interactive visualizations of the data, making it more accessible and engaging for users.

## Data
See the `README.md` file in the `data` folder for more information on the data used in this project, what portion of the data has been cleaned, the intended use of the data, and the original source of the data. An overview of the data used in this project is provided below.

### [Native Hawaiian Data Book 2023](https://www.ohadatabook.com/DB2023.html)
- **Description**: The Native Hawaiian Data Book 2023 is a comprehensive collection of data on Native Hawaiians in Hawaii. The data book includes information on population, education, health, and more. This data source is an invaluable consolidation of data on Kanaka Maoli and draws from county, state, and federal databases. The full list of data sources it draws from listed [here](https://ohadatabook.com/fr_statlinks.11.html).
- **Format**: Tabbed Excel file, with each tab representing a different dataset.
- **Ownership**: The Native Hawaiian Data Book is published by the Office of Hawaiian Affairs (OHA), a public agency that serves as a resource for Native Hawaiians. The data book is compiled by the Research Division of OHA.

----------------

[^bignote]: I may revisit the idea of storing all unprocessed data in the `data` folder. This may not be the best approach, as the data may, at some point, be too large to store in a GitHub repository. Storing in a cloud service like AWS may be a better approach or else simply pointing to the data source in the project and leaving it at that. I would like to prove some sense of data integrity, however, so I will likely store the data in the `data` folder until I can find a better solution.