# 🛡️ SATI API

**Scam Analysis & Threat Intelligence API** - ระบบ AI สำหรับวิเคราะห์และตรวจจับข้อความหลอกลวง (Scam) ด้วย Google Gemini AI

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0-green.svg)](https://mongodb.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 ภาพรวม

SATI API เป็น RESTful API ที่พัฒนาด้วย Flask และใช้ Google Gemini AI ในการวิเคราะห์ข้อความเพื่อตรวจจับรูปแบบการหลอกลวงต่างๆ เช่น:

- 🎣 **Phishing** - ข้อความหลอกเอาข้อมูลส่วนตัว
- 💸 **Financial Scam** - หลอกลวงทางการเงิน
- 🎁 **Prize Scam** - หลอกลวงเรื่องรางวัล/โชคดี
- 💼 **Job Scam** - หลอกลวงเรื่องงาน
- 💕 **Romance Scam** - หลอกลวงด้วยความรัก
- 📦 **Delivery Scam** - หลอกลวงเรื่องจัดส่งสินค้า

---

## ✨ คุณสมบัติหลัก

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Analysis** | วิเคราะห์ด้วย Google Gemini AI |
| 🔐 **JWT Authentication** | ระบบยืนยันตัวตนด้วย JWT |
| 📊 **History Tracking** | บันทึกประวัติการวิเคราะห์ |
| 📈 **Statistics** | สถิติการใช้งานของผู้ใช้ |
| 📝 **Swagger Docs** | เอกสาร API แบบ Interactive |
| 🚦 **Rate Limiting** | ป้องกันการใช้งานเกินขีดจำกัด |
| 🐳 **Docker Ready** | พร้อม Deploy ด้วย Docker |

---

## 🏗️ สถาปัตยกรรม

```
┌─────────────────────────────────────────────────────────────┐
│                         Nginx                                │
│                    (Reverse Proxy)                          │
│              Rate Limiting / Load Balancing                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      SATI API (Flask)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │    Auth     │  │    Scam     │  │     Middleware      │ │
│  │   Module    │  │  Detection  │  │ (JWT, Rate Limit)   │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │                    │
         ▼                    ▼
┌─────────────────┐   ┌─────────────────┐
│    MongoDB      │   │  Google Gemini  │
│   (Database)    │   │      AI         │
└─────────────────┘   └─────────────────┘
```

---

## 🚀 การติดตั้ง

### ข้อกำหนดเบื้องต้น

- Python 3.11+
- MongoDB 7.0+
- Docker & Docker Compose (สำหรับ Container)
- Google API Key (สำหรับ Gemini AI)

### วิธีที่ 1: Docker Compose (แนะนำ)

```bash
# Clone repository
git clone https://github.com/your-username/sati-api.git
cd sati-api

# สร้างไฟล์ .env
cp .env.example .env

# แก้ไขค่าใน .env (โดยเฉพาะ GOOGLE_API_KEY)
nano .env

# รัน containers
docker compose up -d

# ดู logs
docker compose logs -f
```

### วิธีที่ 2: การติดตั้งแบบ Manual

```bash
# Clone repository
git clone https://github.com/your-username/sati-api.git
cd sati-api

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# หรือ venv\Scripts\activate  # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt

# สร้างไฟล์ .env
cp .env.example .env
nano .env

# รันแอพพลิเคชั่น
python app.py
```

---

## ⚙️ การตั้งค่า Environment Variables

สร้างไฟล์ `.env` จาก `.env.example` และกำหนดค่าต่อไปนี้:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `FLASK_ENV` | โหมดการทำงาน (`development`, `production`) | ❌ | `development` |
| `SECRET_KEY` | Flask secret key | ✅ (production) | `dev-secret-key...` |
| `JWT_SECRET_KEY` | JWT signing key | ✅ (production) | `jwt-secret-key...` |
| `JWT_ACCESS_TOKEN_EXPIRES` | อายุ token (วินาที) | ❌ | `86400` (24 ชม.) |
| `MONGO_URI` | MongoDB connection string | ❌ | `mongodb://localhost:27017/sati_api` |
| `GOOGLE_API_KEY` | Google Gemini API key | ✅ | - |
| `PORT` | Port ที่รัน server | ❌ | `3000` |
| `HOST` | Host address | ❌ | `0.0.0.0` |

---

## 📚 API Endpoints

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/auth/register` | ลงทะเบียนผู้ใช้ใหม่ |
| `POST` | `/api/v1/auth/login` | เข้าสู่ระบบ |
| `GET` | `/api/v1/auth/me` | ดูข้อมูลผู้ใช้ปัจจุบัน |

### 🛡️ Scam Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/scam/analyze` | วิเคราะห์ข้อความ |
| `GET` | `/api/v1/scam/history` | ดูประวัติการวิเคราะห์ |
| `GET` | `/api/v1/scam/history/:id` | ดูรายละเอียดรายงาน |
| `GET` | `/api/v1/scam/statistics` | ดูสถิติผู้ใช้ |

### ❤️ Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | ตรวจสอบสถานะ service |
| `GET` | `/api/v1/health` | Health check endpoint |

### 📖 Documentation

- **Swagger UI**: [http://localhost:3000/apidocs](http://localhost:3000/apidocs)

---

## 💡 ตัวอย่างการใช้งาน

### ลงทะเบียนผู้ใช้

```bash
curl -X POST http://localhost:3000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
```

### เข้าสู่ระบบ

```bash
curl -X POST http://localhost:3000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!"
  }'
```

### วิเคราะห์ข้อความ

```bash
curl -X POST http://localhost:3000/api/v1/scam/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "text": "คุณได้รับรางวัล iPhone 15 Pro Max! กรุณาโอนค่าจัดส่ง 500 บาท"
  }'
```

### ตัวอย่าง Response

```json
{
  "success": true,
  "data": {
    "report_id": "507f1f77bcf86cd799439011",
    "is_scam": true,
    "confidence": 0.95,
    "scam_type": "prize_scam",
    "risk_level": "high",
    "analysis": "ข้อความนี้มีลักษณะเป็นการหลอกลวงประเภทรางวัล...",
    "red_flags": [
      "ขอให้โอนเงิน",
      "รางวัลที่ไม่ได้สมัคร",
      "สร้างความเร่งด่วน"
    ],
    "recommendation": "ไม่ควรโอนเงินหรือให้ข้อมูลส่วนตัว"
  }
}
```

---

## 🐳 Docker Commands

```bash
# Build และ Start containers
docker compose up -d --build

# Stop containers
docker compose down

# ดู logs
docker compose logs -f sati-api

# เข้า container
docker compose exec sati-api sh

# Restart services
docker compose restart
```

---

## 📁 โครงสร้างโปรเจค

```
sati-api/
├── app/
│   ├── __init__.py          # Application factory
│   ├── auth/                 # Authentication module
│   │   ├── models.py         # User model
│   │   └── routes.py         # Auth endpoints
│   ├── scam_detection/       # Scam detection module
│   │   ├── models.py         # Scam report model
│   │   ├── routes.py         # Scam endpoints
│   │   └── services.py       # AI analysis service
│   ├── database/             # Database layer
│   │   ├── connection.py     # MongoDB connection
│   │   └── repositories.py   # Data repositories
│   ├── middleware/           # Middleware
│   │   ├── errors.py         # Error handlers
│   │   └── rate_limit.py     # Rate limiting
│   ├── schemas/              # Request/Response schemas
│   └── utils/                # Utilities
│       ├── helpers.py        # Helper functions
│       └── logger.py         # Logging setup
├── nginx/
│   └── nginx.conf            # Nginx configuration
├── app.py                    # Entry point
├── config.py                 # Configuration
├── swagger_config.py         # Swagger/OpenAPI config
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker image
├── docker-compose.yml        # Docker Compose
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 🔒 ความปลอดภัย

- ✅ Password hashing ด้วย bcrypt
- ✅ JWT-based authentication
- ✅ Rate limiting ป้องกัน brute force
- ✅ Input sanitization
- ✅ CORS configuration
- ✅ Security headers (via Nginx)
- ✅ Non-root Docker user

> ⚠️ **สำหรับ Production**: อย่าลืมเปลี่ยน `SECRET_KEY` และ `JWT_SECRET_KEY` ให้เป็นค่าที่ปลอดภัย!

---

## 🧪 การทดสอบ

```bash
# รัน tests (TODO: implement)
python -m pytest tests/ -v

# รัน tests with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

---

## 📊 Monitoring

- **Health Check**: `GET /api/v1/health`
- **Logs**: `docker compose logs -f`
- การใช้งาน MongoDB สามารถ monitor ผ่าน MongoDB Compass หรือ CLI

---

## 🤝 การมีส่วนร่วม

1. Fork repository
2. สร้าง feature branch (`git checkout -b feature/amazing-feature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. เปิด Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 ทีมพัฒนา

- **Developer**: SATI Team

---

## 📞 ติดต่อ

- 📧 Email: support@sati.app
- 🌐 Website: https://sati.app
- 📖 Docs: [API Documentation](http://localhost:3000/apidocs)

---

<p align="center">
  Made with ❤️ for a safer digital world
</p>
