# Ops-Programming-and-Database-Lab

# Flask + MySQL App in Docker on AWS EC2

This project runs a Flask web application inside a Docker container on an AWS EC2 instance. The application connects to a MySQL-compatible Amazon RDS database using **PyMySQL**.

---

✅ Prerequisites

- An AWS EC2 instance with Docker installed
- An Amazon RDS (MySQL) instance accessible from the EC2 instance
- EC2 security group with port **5000** open
- RDS security group that allows traffic from the EC2 instance
- This repo contains:

  - `app.py` – Flask app (with DB config inside)
  - `requirements.txt` – Lists Flask and PyMySQL
  - `dockerfile` – Builds the container

---

📦 Setup & Deployment

1. Connect to the EC2 Instance

```bash
ssh ec2-user@<your-ec2-public-ip>
```

2. Clone the Repository

```bash
git clone https://github.com/Delvin-Yamoah/Ops-Programming-and-Database-Lab.git
cd Ops-Programming-and-Database-Lab
```

3. Build the Docker Image

```bash
sudo docker build -t flasksql .
```

4. Run the Container

```bash
sudo docker run -d -p 5000:5000 flasksql
```

---

🌐 Access the App

Once the container is running, open:

```
http://<your-ec2-public-ip>:5000
```

You should see the Flask app running, and if the database is reachable, any related functionality should work as expected.

🛡️ Security Checklist

- ✅ Port 5000 open in EC2 security group
- ✅ RDS security group allows traffic from EC2 instance (or same VPC)
- 🔒 Store credentials securely inside the container (use `.env`, config files, or secrets management)
- 🔄 Periodically update `requirements.txt` and review dependencies
