# Regulations.gov Project

## Installation

1. First, create an EC2 instance.

2. Next, SSH into that EC2 instance.

3. Once connected, install Git by running the following command:
    ```
    sudo yum install git
    ```

4. After installing Git, clone the repository by running:
    ```
    git clone <repository_url>
    ```

5. Change directory into the cloned repository:
    ```
    cd DSP
    ```

6. Create a virtual environment named `.venv`:
    ```
    python3 -m venv .venv
    ```

7. Activate the virtual environment:
    ```
    source .venv/bin/activate
    ```

8. Install the project dependencies by running:
    ```
    pip install -r requirements.txt
    ```

9. Next, download and install the "en_core_web_lg" model for spaCy:
    ```
    python -m spacy download en_core_web_lg
    ```

10. To run the project, use the following command:
    ```
    ./all.sh
    ```

### This project will run through every organization and extract all of the names from each file. It will give you multiple files in many formats (csv, json) containing all of the information extracted. It has functionallity so that if you run it again and the data is in the same spot in the directory as your all.sh script, then it will skip all files it already extracted.
