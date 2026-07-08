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
| 🥈 **Silver** | Silver | Core academics, attendance, homework |
| 🥇 **Gold** | Gold | + Finance, exams, timetable, OCR |
| 💎 **Platinum** | Platinum | + Live GPS tracking, advanced OCR, analytics |

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

### 🥈 Silver
| Role | Username |
|------|----------|
| Admin | `admin_silver` |
| Principal | `principal_silver` |
| Teacher | `teacher_silver` |
| Student | `student_silver` |
| Teacher (John) | `teacher_john` |
| Teacher (Lucas) | `teacher_lucas` |
| Teacher (Isabella) | `teacher_isabella` |

### 🥇 Gold
| Role | Username |
|------|----------|
| Admin | `admin_gold` |
| Principal | `principal_gold` |
| Teacher | `teacher_gold` |
| Accountant | `accountant_gold` |
| Teacher (Ashish) | `teacher_ashish` |
| Teacher (Swapna) | `teacher_swapna` |
| Teacher (Noah) | `teacher_noah` |
| Teacher (Emma) | `teacher_emma` |

### 💎 Platinum
| Role | Username |
|------|----------|
| Admin | `admin_platinum` |
| Principal | `principal_platinum` |
| Teacher | `teacher_platinum` |
| Accountant | `accountant_platinum` |
| Student | `student_platinum` |
| Parent | `parent_platinum` |
| Teacher (Olivia) | `teacher_olivia` |
| Teacher (Mokshith) | `teacher_mokshith` |
| Teacher (Sophia) | `teacher_sophia` |
| Teacher (Liam) | `teacher_liam` |

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
