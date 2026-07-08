<div align="center">

# 🎓 School OS

### Multi-Tenant School Management Platform

[![Django](https://img.shields.io/badge/Django-4.x-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)](https://github.com/ashishkumarkasani21-create/school-os)

**A full-featured, SaaS-ready school ERP system built with Django.**

</div>

---

## 🌟 Overview

Multi-tenant school management platform for 3 schools with 21+ user accounts across Silver, Gold, and Platinum subscription tiers.

| Tier | School | Features |
|------|--------|----------|
| 🥈 **Silver** | Primary Stars School | Core academics, attendance, homework |
| 🥇 **Gold** | Beacon Academy | + Finance, exams, timetable, OCR |
| 💎 **Platinum** | Imperial Elite College | + Live GPS tracking, advanced OCR, analytics |

---

## ✨ Features

### 🔐 Authentication
- 6 roles: Admin, Principal, Teacher, Student, Parent, Accountant
- **Light animated aurora login page** with plan overview and demo accounts directory
- Country/currency selector (India ₹, USA $, UK £, Canada C$, Europe €)
- OCR hidden from Parent and Student roles

### 📚 Academics
- Classroom + Section creation with teacher assignment
- Named teachers: Olivia, Mokshith, Ashish, Swapna, John
- Subject, Timetable, Exam scheduling, Mark entry

### 🚌 Live GPS Bus Tracking *(Platinum)*
- Leaflet.js map with real-time vehicle positions
- Multi-country map support — map centers to selected region

### 📷 OCR Document Scanning *(Gold/Platinum staff only)*
- Upload admission forms, marksheets, fee receipts
- Automated data extraction and review UI

### 💰 Finance, 📢 Communication, 📝 Leave Requests
- Fee structures, payments, receipts
- Announcements broadcast by role
- Leave workflow with principal approval

---

## 🚀 Quick Start

```bash
git clone https://github.com/ashishkumarkasani21-create/school-os.git
cd school-os
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Open **http://localhost:8000**

---

## 🔑 Demo Accounts

Password for all: **`school123`**

### 🥈 Silver — Primary Stars School
| Role | Username |
|------|----------|
| Admin | `admin_silver_stars` |
| Principal | `principal_silver_stars` |
| Teacher | `teacher_silver_stars` |
| Student | `student_silver_stars` |
| Teacher (John) | `teacher_john` |

### 🥇 Gold — Beacon Academy
| Role | Username |
|------|----------|
| Admin | `admin_gold_beacon` |
| Principal | `principal_gold_beacon` |
| Teacher | `teacher_gold_beacon` |
| Accountant | `accountant_gold_beacon` |
| Teacher (Ashish) | `teacher_ashish` |
| Teacher (Swapna) | `teacher_swapna` |

### 💎 Platinum — Imperial Elite College
| Role | Username |
|------|----------|
| Admin | `admin_platinum_imperial` |
| Principal | `principal_platinum_imperial` |
| Teacher | `teacher_platinum_imperial` |
| Accountant | `accountant_platinum_imperial` |
| Student | `student_platinum_imperial` |
| Parent | `parent_platinum_imperial` |
| Teacher (Olivia) | `teacher_olivia` |
| Teacher (Mokshith) | `teacher_mokshith` |

---

## 💎 Subscription Plans

| Feature | 🥈 Silver | 🥇 Gold | 💎 Platinum |
|---------|-----------|---------|------------|
| Core Academics | ✅ | ✅ | ✅ |
| Finance & Fees | ❌ | ✅ | ✅ |
| Exam Scheduling | ❌ | ✅ | ✅ |
| Basic OCR | ❌ | ✅ | ✅ |
| Live Bus GPS Tracking | ❌ | ❌ | ✅ |
| Advanced Analytics | ❌ | ❌ | ✅ |
| India (₹) | ₹50,000/yr | ₹75,000/yr | ₹1,00,000/yr |
| USA ($) | $699/yr | $999/yr | $1,399/yr |

---

## 📝 Changelog

| Version | Change |
|---------|--------|
| v1.3 | Plans side panel freed — no height constraint |
| v1.3 | Demo accounts directory added to login |
| v1.3 | Silver/Gold/Platinum plan cards on login |
| v1.2 | Login redesigned to light aurora animated theme |
| v1.2 | 5 custom teachers: Olivia, Mokshith, Ashish, Swapna, John |
| v1.2 | OCR hidden from parent and student roles |
| v1.1 | GitHub repo created and code pushed |
| v1.0 | Initial commit |

---

## 🛠️ Tech Stack

Django · SQLite · Leaflet.js · Font Awesome · Google Fonts (Inter) · Vanilla CSS/JS

---

<div align="center">Built with ❤️ for schools across India and beyond — ⭐ Star this repo!</div>
