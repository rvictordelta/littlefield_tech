This program aids with Booth's Operations Strategy final project on Littlefield Technologies.
It scrapes data from a team's website and concentrates it an easy to read excel file.  The program sends the file out via email

Install requirements:
`python -m pip install -r requirements.txt`

Run:
`python tasks.py`

**Untracked files:**

You will need to create two files: `groups.csv` and `creds.py`

`groups.csv` has a single line for each group in this format: alias,username,password,email1,email2,email3,etc

`creds.py` has two variables, p and u. set them equal to a user name and password for a gmail account.  gmail account settings must be configured to allow for this type of access