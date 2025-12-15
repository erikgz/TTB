# Project TTB - AI-Powered Alcohol Label Verification App

This application provides a web form for the Alcohol and Tobacco Tax and Trade Bureau (TTB).

The user can provide a label image and information about the alcohol beverage. The app will use OCR to verify whether the image content matches the submitted data. 

A report is shown after the verification to inform the level of matching. The report will return a table with the match level ("Full Match", "Partial Match" or "No Match") and one match result for each data item provided.


## Links

[GitHub repository](https://github.com/erikgz/TTB)<br>
[Label Verification App](http://178.156.154.10/)<br>
[Kaggle Test Images used in the project](https://www.kaggle.com/datasets/jenlooper/bottles?resource=download)


## Getting Started

These instructions will get a copy of the project up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

*   Python 3.12 (3.12.3 works)
*   `pip` (Python package manager)
*   Virtual Environment manager `venv`

### Installation (Linux Ubuntu)

0. **Prerequisites**
sudo apt install python3-venv
sudo apt install libgl1 -y
sudo apt install libgomp1 -y


1.  **Clone the repository:**

    ```
    git clone https://github.com/erikgz/TTB.git
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Flask Environment variables**

    ```bash
    export FLASK_APP=TTB.app
    export FLASK_ENV=production
    ```

5.  **Run the Backend**

    From the root directory of the App /TBB, enter:
    ```bash
    flask run --host=0.0.0.0 --port=8000
    ```

6.  **Run the App**
    From a web browser, connect to [TBB](127.0.0.1:8000)
    

### Installation (Windows 10, 11)

0. **Prerequisites**
 Ensure Python 3.12 is installed and on the path.


1.  **Clone the repository:**

    ```
    git clone https://github.com/erikgz/TTB.git
    ```

2.  **Create a virtual environment** (recommended):

    ```cmd
    py -3.12 -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```cmd
    pip install -r requirements.txt
    ```

4.  **Set Flask Environment variables**

    ```cmd
    set FLASK_APP=TTB.app
    set FLASK_ENV=production
    ```

5.  **Run the Backend**

    From the root directory of the App /TBB, enter:
    ```bash
    flask run --host=0.0.0.0 --port=8000
    ```

7.  **Run the App**
    From a web browser, connect to [TBB](127.0.0.1:8000)


### Suggested Improvements
*   Use TTB data of label images and matching text to train improved AI models in house.
*   Store images and data in a database to support compliance officers when they have to lookup results weeks later. It would also allow officers to track the history of a brand.
*   Speed-up match analysis with better hardware.