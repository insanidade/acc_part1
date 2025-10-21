# DemoQA Bookstore Automation Toolkit

This project is a Python automation toolkit that walks through the DemoQA Book Store API workflow end to end, from user creation to renting books, so new developers can validate each step quickly.

## Getting Started

### Prerequisites
- Python 3.11+
- pip (bundled with recent Python distributions)
- Optional: virtualenv or another environment manager for isolated installs

### Installation
1. Clone the repository.
   ```
   git clone git@github.com:insanidade/acc_part1.git
   ```
2. Navigate into the project directory.
   ```
   cd acc_part1
   ```
3. Install the Python dependencies (consider doing this inside a virtual environment).
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Environment setup is optional at this stage. If a `.env` file does not exist, the scripts that rely on it will create one automatically when credentials are generated. You can still prepare an empty file up front if preferred.
   ```
   # Optional: create an empty .env file
   touch .env
   ```

## Running the Application
Execute the orchestrated workflow with:
```
python test_runner.py
```

## Usage (Optional)
The entry point `test_runner.py` invokes the sequence of scripts that create a user, generate and authorize a token, fetch book data, and rent titles. You can also run individual scripts (for example, `python test_fetch_books.py`) when debugging specific steps—just ensure a populated `.env` file is present, because most scripts load credentials from it.


