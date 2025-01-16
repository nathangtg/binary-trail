# Binary Trails 🚀

A hands-on developer playground for experimenting with modern development tools, APIs, and software engineering concepts. Binary Trails offers an engaging way to practice real-world development scenarios through interactive challenges.

## 🌟 Overview

Binary Trails is a personal project designed to provide a fun, pressure-free environment for developers to experiment with various technical concepts. Unlike traditional learning platforms, Binary Trails focuses on hands-on experimentation and practical application of modern development tools.

### 🛠️ Tech Stack

- **Frontend:**
  - Nuxt.js 3
  - TypeScript
  - Tailwind CSS
  - Vue 3 Composition API

- **Backend:**
  - Flask (Python)
  - RESTful API design
  - JWT Authentication
  - Cryptographic functions for API challenges

- **Infrastructure:**
  - DynamoDB
  - Terraform for IaC
  - AWS Services

### ✨ Key Features

- **API Warrior Game:**
  - Dynamic API challenge generation
  - Hash verification system
  - Encrypted endpoints
  - Real-time response validation
  - Progressive difficulty levels

- **Interactive Challenges:** Hands-on exercises covering:
  - API Integration
  - Encryption Implementation
  - Algorithm Design
  - Testing Practices
  - Postman Usage
  - GitHub Gists Integration

- **Modern UI:**
  - Responsive design
  - Dark theme with green accents
  - Glassmorphism effects
  - Smooth animations

- **Infrastructure:**
  - Infrastructure as Code using Terraform
  - DynamoDB configuration for challenge and user data
  - Scalable AWS architecture

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/binary-trails.git
```

2. Install frontend dependencies:
```bash
cd binary-trails/frontend
npm install
```

3. Set up Python backend:
```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Set up your AWS credentials and Terraform:
```bash
cd ../terraform
terraform init
terraform apply
```

5. Start the development servers:
```bash
# Terminal 1 - Frontend
cd frontend
npm run dev

# Terminal 2 - Backend
cd backend
flask run
```

## 📁 Project Structure

```
binary-trails/
├── frontend/
│   ├── components/
│   │   ├── HeroSection.vue
│   │   └── FeaturesSection.vue
│   ├── layouts/
│   │   └── default.vue
│   └── pages/
│       ├── index.vue
│       └── challenges.vue
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── challenges.py
│   │   └── verification.py
│   ├── utils/
│   │   ├── encryption.py
│   │   └── validators.py
│   └── requirements.txt
├── terraform/
│   ├── main.tf
│   ├── dynamodb.tf
│   └── variables.tf
└── ...
```

## 🔧 Backend Architecture

The Flask backend serves as the core of the API Warrior game, providing:

- **Challenge Generation:**
  - Dynamic API endpoint creation
  - Response validation
  - Hash verification system

- **Authentication:**
  - JWT-based user authentication
  - Secure session management
  - Role-based access control

- **API Features:**
  - Rate limiting
  - Request validation
  - Error handling
  - Logging system
  - DynamoDB Connection

## 🌐 Infrastructure

The project utilizes AWS DynamoDB for data storage, with the infrastructure managed through Terraform. Key components include:

- DynamoDB tables for challenges and user progress
- Terraform configurations for infrastructure management
- AWS services integration
- API Gateway configuration

## 🤝 Contributing

Feel free to fork the project and submit pull requests. This is an open playground for everyone to learn and experiment!
