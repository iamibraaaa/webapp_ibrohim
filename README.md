1. Database setup

Installing dataset from Kaggle https://www.kaggle.com/datasets

Launching database in RDS and connecting it with Debeaver

Creating table named tbl_<your_first_name>_<dataset_name>

Importing CSV file to the database in Debeaver

2. S3 Static Hosting

Create an S3 bucket for static website hosting

Uploading HTML and file should be named: index_<your_first_name>.html

Set up the correct S3 bucket policy to make it public

3. EC2 Deployment:

Launch a new EC2 instance (Ubuntu )

The project folder name should also include your name (e.g., webapp_xusanboy)

SSH into EC2:

Run:
ssh -i "/Users/Mac/Desktop/your_key_2_ec2.pem" ubuntu@<EC2_Public_IP>
Create Project Directory and Flask Application:

Create the project directory and Python file:
mkdir my_project
cd my_project
touch app.py
Edit app.py.
Create app.py put app.py file code and change these parts with your data
conn = pymysql.connect(
    host='your-rds-endpoint',
    user='admin',
    password='admin1234',
    db='studentdb'
Set Up Python Virtual Environment:

Set up and activate the virtual environment:
python3 -m venv venv
source venv/bin/activate
Install Python Dependencies:

Install the necessary libraries:
pip3 install --upgrade pip
pip3 install flask psycopg2-binary
Run Flask Application:

Run the Flask app:
python app.py
Access the Application:

Open the browser and put it and test it in browser http://<EC2_Public_IP>:8000.
S3 Bucket part

Create and upload index_xusanboy.html to your S3 bucket
Enable Static Website Hosting
Make the bucket public
Add public read policy to the bucket
Open your S3 website endpoint — you should see the list of books fetched from RDS.
