# 🛠️ Internal Portal Web Application Backend

## 📋 Introduction
Welcome to the backend of the **Internal Portal Web Application**—a robust platform that centralizes and streamlines various business operations within the organization. By integrating multiple data sources, this backend service enables efficient data access, management, and analysis. The frontend counterpart of this application can be found [here](https://github.com/a-dirir/wep-app-frontend).

## 🚀 Installation

To get started with the backend setup, follow these steps:

1. **Navigate to the Backend Directory:**
   ```bash
   cd wep-app-backend

2. **Create a virtual environment:**

    #### Linux
    ```bash
    python3 -m venv .venv 
    ```
    #### Windows
    ```bash
    python -m venv .venv
    ```
3. **Activate the virtual environment:**

    #### Linux
    ```bash
    source .venv/bin/activate  
    ```
    #### Windows
    ```bash
    .venv\Scripts\activate
    ```
4. **Install the required package:**

    #### Linux
    ```bash
    python3 -m pip install -r requirements.txt
    ```
    #### Windows
    ```bash
    python -m pip install -r requirements.txt
    ```

## ⚙️ Configuration
### MySQL Database Setup

1. Create a file named config.env in the root directory of the project.
2. Add your MySQL database credentials to the config.env file

    ```env
    MYSQL_HOST=localhost
    MYSQL_USER=3306
    MYSQL_PASSWORD=xxxx
    MYSQL_DATABASE_NAME=yyyy
    ```

## ▶️ Running the Web Application
To run the Web Application, you need to run the **main.py** file.

#### Linux
```bash
python3 main.py
```
#### Windows
```bash
python main.py
```

