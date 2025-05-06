# WebApp Ibrahim

## Overview
This project is a full-stack web application hosted on AWS that integrates:
- Static frontend (HTML/CSS/JS) served via S3.
- Backend powered by Flask, running on an EC2 instance.
- PostgreSQL database hosted on RDS.

The backend connects to a PostgreSQL database and supports CRUD operations for movie data. The frontend (index.html) displays this data to users.

## How to Run the Application

### 1. Clone the repository
```bash
git clone git@github.com:iamibraaaa/webapp_ibrohim.git
Run the Flask app (if running locally):
python app.py
The app will run on http://localhost:8000. (This is mainly for development purposes. For production, use EC2.)

Deployed Links

Frontend (S3 Static Website): S3 Static Site URL
Backend (EC2): EC2 App URL
Database (RDS): PostgreSQL database hosted on Amazon RDS (connected to Flask backend)
Project Files

app.py: Flask backend code.
index_ibrohim.html: Frontend HTML.
import_data.py: Script used to import data into PostgreSQL.
requirements.txt: Python dependencies.
EC2 Setup (Backend)

The Flask app (app.py) is hosted on an EC2 instance and connected to a PostgreSQL database on Amazon RDS. The EC2 instance runs the Flask app on port 8000 and is accessible publicly.

Steps for EC2 Setup:
SSH into EC2 instance:
ssh -i your-key.pem ec2-user@your-ec2-public-ip
Set up the environment, install dependencies:
pip install -r requirements.txt
Start the app:
python app.py
PostgreSQL (RDS) Setup:
Make sure the RDS instance is publicly accessible or use an EC2 instance in the same VPC.
Ensure security groups allow inbound traffic on port 5432 from your EC2 instance.
Notes

Static Files: The index_ibrohim.html and CSS/JS are hosted on an S3 bucket as a static website.
Backend: Flask application on EC2 communicates with PostgreSQL to serve and store data.
Security: Ensure that sensitive information such as database credentials is securely managed (using AWS Secrets Manager or environment variables).
Additional Resources

AWS EC2 Documentation
AWS RDS Documentation
Flask Documentation

#### 2. **Push Everything to GitHub**
Make sure you have:
- `app.py`
- `index_ibrohim.html`
- `import_data.py` (if relevant)
- `requirements.txt`
- `README.md`

Then, commit and push your changes:

```bash
git add .
git commit -m "Initial commit with Flask app and static files"
git push -u origin main
3. Test Your Deployment

Ensure the following:

S3: index_ibrohim.html is live and accessible through the static hosting URL.
EC2: Your Flask app is accessible via the public IP of your EC2 instance (e.g., http://ec2-your-ip:8000).
RDS: Check that your Flask app can interact with the database properly.
