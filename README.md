Branch Navigator - AI-Powered Branch Analytics Platform

Overview
Branch Navigator is an end-to-end AI/ML analytics platform built on the Rossmann Store Sales dataset (~1M rows, 1,115 branches). It combines machine learning, time-series forecasting, anomaly detection, and LangChain-based intelligent agents to help businesses optimize branch performance and make data-driven decisions.

Features

Data cleaning, preprocessing, and exploratory data analysis (EDA) on 1M+ rows
KMeans customer segmentation to identify branch behavior patterns
Random Forest classifier with 94% accuracy for branch performance prediction
Prophet-based 90-day sales forecasting for future business planning
Isolation Forest anomaly detection to flag 56 underperforming branches
Custom branch scoring formula (0-100 scale) for business prioritization
LangChain multi-agent system (5 agents) with FAISS vector store and SentenceTransformer embeddings for intelligent semantic search
4-page interactive Streamlit dashboard for business stakeholders
Automated PDF report generation using ReportLab

Tech Stack

Language: Python
AI/ML: scikit-learn, Prophet, FAISS, SentenceTransformers, LangChain
Data Analysis: Pandas, NumPy
Visualization: Matplotlib, Seaborn, Streamlit
Reporting: ReportLab
Tools: Jupyter Notebook, VS Code, Anaconda, Git

Dataset
Rossmann Store Sales Dataset - 1,115 retail branches, approximately 1M rows of transaction data.
Key Results

94% accuracy on branch performance classification
90-day sales forecast per branch using Prophet
56 anomalous branches detected using Isolation Forest
Branch scoring system ranking all 1,115 branches from 0 to 100

