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
   git clone https://github.com/your-username/acc_part1.git
   ```
2. Navigate into the project directory.
   ```
   cd acc_part1
   ```
3. Install the Python dependencies (consider doing this inside a virtual environment).
   ```
   python -m pip install --upgrade pip
   pip install requests python-dotenv
   ```
4. Create the `.env` file in the project root and populate it with your DemoQA credentials once they are generated.
   ```
   .env
   ```
   ```
   DEMOQA_USERNAME=
   DEMOQA_PASSWORD=
   DEMOQA_USER_ID=
   DEMOQA_TOKEN=
   ```

## Running the Application
Execute the orchestrated workflow with:
```
python test_runner.py
```

## Usage (Optional)
The entry point `test_runner.py` invokes the sequence of scripts that create a user, generate and authorize a token, fetch book data, and rent titles. Inspect intermediate artifacts such as `test_books.json` or rerun individual scripts (for example, `python test_fetch_books.py`) to validate specific steps during development.


