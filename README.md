# AI-Powered Career Recommendation System

An end-to-end, full-stack AI application that delivers **personalized career path recommendations** using machine learning and **Retrieval-Augmented Generation (RAG)**. The system combines a production-grade **FastAPI backend** with a modern **Vite + React frontend** to provide confidence-aware, explainable career guidance.

---

## Overview

This project is designed to analyze user-provided structured and free-text inputs, infer suitable career paths using trained ML models, and return ranked recommendations with contextual explanations. It follows a **scalable, real-world architecture** commonly used in modern AI-driven products.

---

## Key Features

- End-to-end full-stack architecture
- ML-powered career classification
- Confidence-aware recommendations using regression modeling
- RAG-enhanced explanations and chatbot-style guidance
- Secure authentication and authorization
- Admin support for managing users, models, and configurations
- Clean, responsive frontend built with React
- Designed for scalability and extensibility

---

## System Architecture

1. Users submit structured and free-text inputs through the React frontend.
2. Inputs are securely sent to the FastAPI backend via REST APIs.
3. The backend preprocesses inputs and loads pre-trained ML artifacts.
4. A classification model predicts relevant career paths.
5. A regression model estimates confidence scores for each recommendation.
6. RAG and chatbot components enrich results with contextual explanations.
7. Ranked, confidence-aware recommendations are returned to the frontend for display.

---

## Backend

The backend is implemented using **FastAPI** and provides:

- Authentication and authorization
- Database integration for user data and history
- Admin-level controls for system and model management
- High-performance REST APIs for inference and data exchange

### Machine Learning Components

The backend loads and serves the following ML artifacts:

- TF-IDF / vectorizer for text feature extraction
- Label encoder for career class mapping
- Classification model for predicting career paths
- Confidence regression model to estimate reliability of recommendations

These components enable accurate, explainable, and confidence-aware predictions.

---

## RAG and AI Reasoning

To improve explainability and user experience, the system integrates:

- Retrieval-Augmented Generation (RAG) pipelines
- Chatbot-style reasoning for contextual insights and follow-up guidance
- Natural language responses aligned with predicted career paths

This hybrid approach combines deterministic ML predictions with generative AI reasoning.

---

## Frontend

The frontend is built with **Vite + React** and focuses on usability and performance:

- Collects structured and free-text user inputs
- Communicates securely with backend APIs
- Displays ranked career recommendations
- Presents confidence scores and AI-generated explanations
- Responsive and scalable UI design

---

## Tech Stack

### Backend
- FastAPI
- Python
- REST APIs
- Authentication & Authorization
- Database (SQL / NoSQL)
- Machine Learning Inference
- Retrieval-Augmented Generation (RAG)

### Machine Learning
- TF-IDF / Vectorizer
- Label Encoder
- Classification Model
- Confidence Regression Model
- NLP-based input processing

### Frontend
- Vite
- React
- JavaScript / TypeScript
- Responsive UI Design
- API Integration

### Dev & Tooling
- VS Code
- Git & GitHub
- Environment-based configuration

---

## Setup & Installation

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup
cd frontend
npm install
npm run dev
