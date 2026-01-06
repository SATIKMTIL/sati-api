# 🚀 วิธีรัน SATI API แบบปกติ (python app.py)

## ขั้นตอนการติดตั้งและรัน

### 1️⃣ ติดตั้ง MongoDB (ถ้ายังไม่มี)

#### วิธีที่ 1: ใช้ MongoDB Community Edition

ดาวน์โหลดและติดตั้งจาก: https://www.mongodb.com/try/download/community

#### วิธีที่ 2: ใช้ Docker (แนะนำ - ง่ายกว่า)

```bash
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

### 2️⃣ ตรวจสอบว่า MongoDB กำลังรันอยู่

```bash
# ตรวจสอบว่า MongoDB รันอยู่หรือไม่
# Windows (PowerShell)
Get-Process -Name mongod -ErrorAction SilentlyContinue

# หรือลองเชื่อมต่อทดสอบ
mongosh mongodb://localhost:27017
```

### 3️⃣ ตั้งค่า Google Gemini API Key

1. ไปที่ https://makersuite.google.com/app/apikey
2. สร้าง API Key
3. เปิดไฟล์ `.env` และใส่ API Key ของคุณ:

```env
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

⚠️ **สำคัญ:** ต้องมี API Key จริง ไม่เช่นนั้นจะรันไม่ได้!

### 4️⃣ ติดตั้ง Python Dependencies

```bash
# ติดตั้ง dependencies ทั้งหมด
pip install -r requirements.txt
```

หรือถ้าใช้ virtual environment (แนะนำ):

```bash
# สร้าง virtual environment
python -m venv venv

# เปิดใช้งาน virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (CMD)
.\venv\Scripts\activate.bat

# ติดตั้ง dependencies
pip install -r requirements.txt
```

### 5️⃣ รัน Application 🎉

```bash
python app.py
```

### 6️⃣ ทดสอบว่ารันสำเร็จ

เปิดเบราว์เซอร์และไปที่:

- **API Health Check**: http://localhost:5000/
- **API Documentation (Swagger)**: http://localhost:5000/api/docs
- **API Health Endpoint**: http://localhost:5000/api/v1/health

---

## 📋 Checklist ก่อนรัน

- [ ] ติดตั้ง Python 3.11+ แล้ว
- [ ] ติดตั้ง MongoDB และรันอยู่ที่ localhost:27017
- [ ] ใส่ Google Gemini API Key ในไฟล์ `.env` แล้ว
- [ ] ติดตั้ง dependencies จาก `requirements.txt` แล้ว
- [ ] ไฟล์ `.env` มีการตั้งค่าถูกต้อง

---

## 🐛 แก้ปัญหาที่พบบ่อย

### ปัญหา: "Configuration Error: GOOGLE_API_KEY environment variable is required"

**วิธีแก้:**

1. เปิดไฟล์ `.env`
2. ใส่ Google API Key จริง (ไม่ใช่ `your-google-api-key-here`)
3. บันทึกไฟล์และรันใหม่

### ปัญหา: "Failed to connect to MongoDB"

**วิธีแก้:**

1. ตรวจสอบว่า MongoDB รันอยู่:
   ```bash
   # Windows (PowerShell)
   Get-Process -Name mongod
   ```
2. ถ้าไม่รัน ให้เริ่ม MongoDB:

   ```bash
   # ถ้าใช้ Docker
   docker start mongodb

   # ถ้าติดตั้งแบบปกติ
   net start MongoDB
   ```

### ปัญหา: "Port 5000 is already in use"

**วิธีแก้:**

1. เปลี่ยน PORT ในไฟล์ `.env`:
   ```env
   PORT=8000
   ```
2. รันใหม่

---

## 🧪 ทดสอบ API

### 1. ลงทะเบียนผู้ใช้ใหม่

```bash
curl -X POST http://localhost:5000/api/v1/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\",\"name\":\"Test User\"}"
```

### 2. Login

```bash
curl -X POST http://localhost:5000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

คัดลอก `access_token` ที่ได้

### 3. วิเคราะห์บทสนทนา

```bash
curl -X POST http://localhost:5000/api/v1/scam/analyze ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer <your-access-token>" ^
  -d "{\"conversation_text\":\"สวัสดีครับ ผมเป็นเจ้าหน้าที่ธนาคาร บัญชีของคุณมีปัญหาต้องโอนเงินมาตรวจสอบด่วน\"}"
```

---

## 🌐 ใช้ Swagger UI (แนะนำสำหรับมือใหม่)

1. เปิดเบราว์เซอร์ไปที่: http://localhost:5000/api/docs
2. จะเห็น UI สวยงามสำหรับทดสอบ API
3. ไม่ต้องใช้ curl หรือ Postman
4. มี documentation ครบทุก endpoint

---

## 📁 โครงสร้าง Logs

เมื่อรัน application จะสร้างโฟลเดอร์ `logs/` และมี log files:

- การเชื่อมต่อ database
- ข้อมูล request/response
- ข้อผิดพลาด (ถ้ามี)

---

## ⚡ Quick Start (รันด่วน 3 คำสั่ง)

```bash
# 1. รัน MongoDB (ถ้าใช้ Docker)
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# 2. ติดตั้ง dependencies (ถ้ายังไม่ได้ติดตั้ง)
pip install -r requirements.txt

# 3. รัน application (ต้องใส่ GOOGLE_API_KEY ในไฟล์ .env ก่อน!)
python app.py
```

**เสร็จแล้ว!** 🎉 ไปที่ http://localhost:5000/api/docs เพื่อเริ่มใช้งาน

---

## 🔒 สำหรับ Production

ถ้าต้องการนำไปใช้จริง (production) ให้ดูไฟล์ `BUG_FIXES_SUMMARY.md`
มี Production Checklist อยู่ครับ
