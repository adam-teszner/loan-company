
# **LoanCompany** website

This website is my first Django project, created for learning purposes. Some parts of the code, especially the oldest ones, should be rewritten due to their poor quality. However, they do showcase my progression over time.

---

## Features
The website mimics the debt management service of a loan company, intended for internal use by the company's workers. 
After logging in, a user who is presumed to be a company worker can create "customers" and sell loans to them. 
Once a loan is sold, the user can monitor its repayment schedule, including payment dates and amounts etc. 
Additionally, the user has the ability to sort, filter, and search customers, as well as generate PDF and XLS files with detailed information.

## Live version available at:

##### https://loan-co.xyz

## Installation


- Open terminal and navigate to desired directory and type:
	`git clone https://github.com/adam-teszner/loan-company.git .`
	`docker-compose up`

After docker finishes building containers, you have to make migrations and migrate. 
If you wish to populate the database with fake data there is a management command for that:
`manage.py populate` 
it takes 4 (integer) arguments - more info inside the file

---

There is a `DEFAULT_SETTINGS` directory, where `prod_settings.py`, `settings.py`,  and `.env` files are stored. Be sure to define your settings and move those files to correct directories before running application. 
