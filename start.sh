#!/bin/sh
uvicorn api.working:app --host 0.0.0.0 --port 10000 &
streamlit run streamlit_app.py --server.port 8501 --server.enableCORS false
