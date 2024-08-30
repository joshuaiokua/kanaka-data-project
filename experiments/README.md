# Experiments

Within this project's overarching goal to centralize, clean, and make data on Kanaka Maoli (Native Hawaiians) more accessible and interactive, I also explore more general ideas that help guide development. All are listed and described below.

- [**Current Experiments**](#current-experiments)
  - [**Enhancing Data Exploration and Interactivity with LLMs**](#enhancing-data-exploration-and-interactivity-with-llms)
  - [**Summarizing and Representing Numerical Data for LLM Integration**](#summarizing-and-representing-numerical-data-for-llm-integration)
  - [**Domain-Specific Fine-Tuning of LLMs**](#domain-specific-fine-tuning-of-llms)
  - [**Streamlining Multi-DataFrame Workflows in Jupyter Notebooks**](#streamlining-multi-dataframe-workflows-in-jupyter-notebooks)
- [**Completed Experiments**](#completed-experiments)

## Current Experiments

### **Enhancing Data Exploration and Interactivity with LLMs**

This experiment will investigate how LLMs can be leveraged to enhance the exploration and interactivity of numerical datasets, particularly in the context of Kanaka Maoli data. The goal is to develop methods that allow users to engage with data conversationally, enabling them to ask questions, receive insights, and interact with dynamic visualizations in real-time. This approach aims to transform static datasets into engaging, open-ended experiences, making data exploration more intuitive and accessible to a wider audience.

### **Summarizing and Representing Numerical Data for LLM Integration**

This experiment will investigate the best methods for summarizing numerical data so that it can be effectively utilized by LLMs. The focus will be on exploring and or developing techniques to create concise, meaningful summaries of numerical datasets that are compatible with LLMs, especially in contexts like retrieval-augmented generation (RAG). The goal is to determine how to best structure and represent these summaries with the understanding that the model will also have access to the underlying data itself.

### **Domain-Specific Fine-Tuning of LLMs**

This experiment will explore the specific requirements for fine-tuning LLMs to work with domain-specific data, such as population data or other specialized datasets. The goal is to determine how to optimize LLMs for handling narrowly focused data, which may require tailored training data and specialized fine-tuning techniques to enhance performance and relevance within a particular domain.

### **Streamlining Multi-DataFrame Workflows in Jupyter Notebooks**

This experiment will explore the complexities of iteratively working with multiple, yet related, DataFrames in Jupyter Notebooks (e.g. Excel files with multiple tabs). In this exploration I may develop a Python library or extension that simplifies the management and transformation of grouped DataFrames by allowing users to apply operations across multiple datasets simultaneously, update them as needed, and easily export or import data. I think this experiment, and the extension that comes from it, might  be particularly valuable for data scientists and analysts who work with small to medium-sized datasets and need a more efficient way to keep related DataFrames synchronized and consistently transformed without the overhead of more complex tools or storage infrastructure.

> **Note**: Ongoing work related to this experiment is mainly done in `src/datacore/` specifically the `DataFrameManager` and `DataFrameEntry` classes.

## Completed Experiments
