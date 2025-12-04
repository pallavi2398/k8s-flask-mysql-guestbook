# Flask Guestbook with Kubernetes & MySQL

![Flask](https://img.shields.io/badge/Flask-Framework-blue)
![MySQL](https://img.shields.io/badge/MySQL-Database-orange)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-blue)
![Docker](https://img.shields.io/badge/Docker-Container-lightblue)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup & Deployment](#setup--deployment)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Project Overview

This project is a **Guestbook web application** built using **Python Flask** and **MySQL**. It is containerized with **Docker** and deployed on **Kubernetes**, demonstrating modern microservice deployment practices.

Key points:

- Microservice deployment with **Kubernetes Deployment and Service**
- Secure database credentials using **Kubernetes Secrets**
- Persistent and reliable storage for MySQL
- Easy to scale and deploy in any environment

---

## Features

- Submit guest entries with **Name** and **Message**
- View all saved entries in **reverse chronological order**
- Database connection handled safely and efficiently
- Fully containerized for seamless deployment on Kubernetes

---

## Architecture

```text
            +--------------------+
            |  Flask Guestbook   |
            |  Container (Pod)  |
            +---------+----------+
                      |
                      | DB_HOST=mysql
                      v
            +--------------------+
            |  MySQL Container   |
            |  Database (Pod)   |
            +--------------------+
                      ^
                      |
          Kubernetes Secret (mysql-user, mysql-pass, mysql-db)

Flask App: Handles HTTP requests and stores/retrieves guestbook entries

MySQL: Stores guest entries persistently

Kubernetes Secrets: Securely provides database credentials to the Flask pod

Prerequisites

Docker

Kubernetes cluster (Minikube / Kind / Cloud Kubernetes)

kubectl CLI

Python 3.10+ (for local development)

Setup & Deployment
1. Clone the repository
git clone https://github.com/<your-username>/k8s-flask-guestbook.git
cd k8s-flask-guestbook

2. Build and push Docker image
docker build -t <your-docker-username>/flask-app:latest .
docker push <your-docker-username>/flask-app:latest

3. Deploy MySQL
kubectl apply -f mysql-secret.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-service.yaml

4. Deploy Flask Application
kubectl apply -f flask-deployment.yml

5. Verify Pods
kubectl get pods
kubectl logs -f <flask-pod-name>

6. Access the Guestbook
kubectl port-forward <flask-pod-name> 5000:5000


Open in your browser:

http://localhost:5000

Project Structure
k8s-flask-mysql/
├── app.py                 # Flask application
├── Dockerfile             # Dockerfile for Flask app
├── flask-deployment.yml   # Kubernetes Deployment for Flask
├── mysql-deployment.yaml  # Kubernetes Deployment for MySQL
├── mysql-service.yaml     # Kubernetes Service for MySQL
├── mysql-secret.yaml      # Kubernetes Secret for DB credentials
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

Future Improvements

Add PersistentVolume for MySQL to retain data across pod restarts

Implement HTTPS with an Ingress Controller

Add authentication for guest entries

Add unit and integration tests for Flask endpoints

Automate deployment with a CI/CD pipeline

Author
Pallavi Agarwal
