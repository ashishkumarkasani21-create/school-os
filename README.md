<div align="center">

<img src="https://img.shields.io/badge/School%20OS-Management%20Platform-6366f1?style=for-the-badge&logo=graduation-cap&logoColor=white" alt="School OS"/>

# 🎓 School OS

### Multi-Tenant School Management Platform

[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/ashishkumarkasani21-create/school-os?style=flat-square&color=gold)](https://github.com/ashishkumarkasani21-create/school-os)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)](https://github.com/ashishkumarkasani21-create/school-os)

**A full-featured, SaaS-ready school ERP system built with Django.**  
Manage academics, finance, transport, attendance, and more — across multiple schools with subscription-based access control.

[🌐 Live Demo](#demo) • [✨ Features](#features) • [🚀 Quick Start](#quick-start) • [📸 Screenshots](#screenshots)

</div>

---

## 🌟 Overview

**School OS** is a production-ready, multi-tenant school management platform designed for institutions of all sizes. It supports **3 schools simultaneously** with **21 user accounts** out of the box via seed data — each school on a different subscription tier.

| Tier | School | Features |
|------|--------|----------|
| 🥈 **Silver** | Primary Stars School | Core academics, attendance, homework |
| 🥇 **Gold** | Beacon Academy | + Finance, exam scheduling, timetable |
| 💎 **Platinum** | Imperial Elite College | + Live GPS tracking, OCR scanning, analytics |

---

## ✨ Features

### 🔐 Authentication & Role-Based Access
- 6 distinct roles: **Admin, Principal, Teacher, Student, Parent, Accountant**
- Session-based login with animated aurora login page
- Auto-redirect to role-specific dashboards

### 🏫 Multi-School SaaS Architecture
- Each school is fully isolated with its own data
- Subscription plans gate access to premium features
- Dynamic **Silver → Gold → Platinum** plan switching

### 📚 Academics Management
- ClassRoom and Section creation with teacher assignment
- Subject and Timetable management
- Exam scheduling with mark entry

### 📊 Role-Specific Dashboards
| Role | Dashboard Features |
|------|--------------------|
| **Admin** | School config, user management, class creation, teacher assignment |
| **Principal** | School-wide analytics, staff overview, announcements |
| **Teacher** | Attendance, homework, grade entry, timetable |
| **Student** | Timetable, attendance, marks, homework, fee status |
| **Parent** | Child progress, attendance, fees, bus tracking |
| **Accountant** | Fee structures, payment collection, receipts |

### 💰 Finance Module
- Fee structure templates per class
- Payment collection and receipt generation
- Outstanding dues tracking

### 🚌 Live GPS Bus Tracking
- Interactive **Leaflet.js** map with real-time vehicle positions
- Route stop management with live coordinate polling
- **Multi-country map support** — map dynamically shifts to the selected region

### 📷 OCR Document Scanning *(Platinum)*
- Upload admission forms, marksheets, fee receipts
- Automated data extraction and review UI
- One-click approve and integrate into the system

### 📢 Communication
- School-wide announcement broadcasts
- Role-targeted notifications (All / Teachers / Students / Parents)
- Unique announcement IDs per board

### 🌍 Multi-Country & Currency Support
- India (₹ / GST), USA ($), UK (£), Canada (C$), Europe (€)
- Live price localization on the subscription plans page
- Session-based country selector on login page

### 📱 Mobile Responsive
- Hamburger sidebar toggle on mobile
- Stacked card layouts for small viewports
- Touch-friendly UI components

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/ashishkumarkasani21-create/school-os.git
cd school-os

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Seed demo data (3 schools, 21 users)
python manage.py seed_data

# 6. Start the server
python manage.py runserver
```

Open **http://localhost:8000** in your browser.

---

## 🔑 Demo Accounts

All accounts use password: **`school123`**

### 🥈 Silver — Primary Stars School
| Role | Username |
|------|----------|
| Admin | `admin_silver_stars` |
| Principal | `principal_silver_stars` |
| Teacher | `teacher_silver_stars` |
| Student | `student_silver_stars` |

### 🥇 Gold — Beacon Academy
| Role | Username |
|------|----------|
| Admin | `admin_gold_beacon` |
| Principal | `principal_gold_beacon` |
| Teacher | `teacher_gold_beacon` |
| Accountant | `accountant_gold_beacon` |

### 💎 Platinum — Imperial Elite College
| Role | Username |
|------|----------|
| Admin | `admin_platinum_imperial` |
| Principal | `principal_platinum_imperial` |
| Teacher | `teacher_platinum_imperial` |
| Accountant | `accountant_platinum_imperial` |
| Student | `student_platinum_imperial` |
| Parent | `parent_platinum_imperial` |

---

## 🏗️ Project Structure

```
school-os/
├── accounts/          # Custom User model, auth views
├── academics/         # ClassRoom, Subject, Timetable
├── attendance_app/    # Daily attendance tracking
├── communication/     # Announcements, broadcasts
├── finance/           # Fees, payments, receipts
├── homework_app/      # Assignment management
├── leave_app/         # Leave requests workflow
├── marks_app/         # Exam marks and grades
├── ocr_app/           # OCR document scanning
├── parents_portal/    # Parent-specific views
├── reports/           # Dashboards and analytics
├── schools/           # School and subscription models
├── transport/         # GPS bus tracking
├── templates/         # All HTML templates
│   ├── accounts/      # Login page
│   ├── reports/       # All dashboards
│   └── transport/     # Bus tracking map
├── school_os/         # Django project settings
├── manage.py
└── requirements.txt
```

---

## 💎 Subscription Plans

| Feature | 🥈 Silver | 🥇 Gold | 💎 Platinum |
|---------|-----------|---------|------------|
| Core Academics | ✅ | ✅ | ✅ |
| Attendance Tracking | ✅ | ✅ | ✅ |
| Homework Management | ✅ | ✅ | ✅ |
| Finance & Fees | ❌ | ✅ | ✅ |
| Exam Scheduling | ❌ | ✅ | ✅ |
| Leave Management | ❌ | ✅ | ✅ |
| Live Bus GPS Tracking | ❌ | ❌ | ✅ |
| OCR Document Scanning | ❌ | ❌ | ✅ |
| Advanced Analytics | ❌ | ❌ | ✅ |
| India (₹) | ₹50,000/yr | ₹75,000/yr | ₹1,00,000/yr |
| USA ($) | $699/yr | $999/yr | $1,399/yr |
| UK (£) | £599/yr | £849/yr | £1,199/yr |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.x (Python) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Frontend** | Vanilla HTML/CSS/JS |
| **Maps** | Leaflet.js |
| **Icons** | Font Awesome 6 |
| **Fonts** | Google Fonts (Inter) |
| **Auth** | Django session auth |
| **OCR** | Custom OCR service layer |

---

## 📝 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ for schools across India and beyond**

⭐ Star this repo if you find it useful!

</div>
