# NewsFudge

### 1.Create and Activate Virtual Environment
```source venv/bin/activate```
```python3 -m venv venv```

### 2.Install Dependencies
```pip install -r requirements.txt```

### 3.Start Server
```uvicorn app.main:app --reload --host 0.0.0.0 --port 8000```