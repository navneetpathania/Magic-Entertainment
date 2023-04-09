Project setup instruction:
1.	Install the latest version of Python from the following link
https://www.python.org/downloads/

2.	Open the command prompt and check for the python package manager is installed or not using following command
pip –version

3.	If pip is not installed use following command to install pip
python -m ensurepip --default-pip

4.	Install virtualenv, a tool for creating isolated python environments:
pip install virtualenv

5.	Create a new virtual environment for your Django project:
virtualenv myenv

6.	Activate the virtual environment:
myenv\Scripts\activate

7.	Download the git CLI:
https://git-scm.com/downloads

8.	Initialize a new Git repository:
git init

9.	Clone the project from github repository:
git clone https://github.com/navneetpathania/Magic-Entertainment.git

10.	Navigate to magic folder:
cd/magic
for example
C:\Users\HP\Desktop\AIP-project
cd/magic
C:\Users\HP\Desktop\AIP-project\magic>

11.	Now run
pip install -r requirements.txt

12.	create an stripe account and get the stripe api keys and replace them with project stripe public and private key
STRIPE_PUBLIC_KEY=” your_stripe_public_key”
STRIPE_SECRET_KEY=”your_stripe_secret_key”
DJSTRIPE_WEBHOOK_SECRET = your stripe webhook secret

13.	Now replace user sent mail address with you email and password.
EMAIL_HOST_PASSWORD = “ your password ”
EMAIL_HOST_USER = "your email"

14. now run:
Python manage.py runserver
Once the local server starts open your browser and type http://localhost:8000/	

