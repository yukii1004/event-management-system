# Club Event Management System

## Overview
The **Club Event Management System** is designed to streamline event planning and management for clubs and organizations within the college. By integrating college email authentication, timetable analysis, venue allocation, and automated event tracking, this system ensures a seamless experience for both event organizers and attendees.

## Features

### 🔑 Authentication
- Users log in using their **college email ID** (students, staff, and clubs).
- Ensures only verified members of the college can access the platform.

### 📅 Free Slot Detection
- The system stores **timetables of all classes**.
- Helps clubs find **free slots** to schedule events efficiently without class conflicts.

### 🏫 OD Tracking
- If an event occurs during class hours, the system **tracks attendees**.
- Automatically **emails faculty members** for OD requests, ensuring transparency.

### 📍 Room Allotment & Capacity Management
- Events are assigned **venues based on fixed capacities**.
- Prevents overbooking by checking the **number of registrations**.
- If a venue clash occurs, the system suggests **alternative available rooms**.

### 💳 Razorpay Integration (Ticketing System)
- Supports **paid club and college events** via **Razorpay**.
- Option to **directly transfer funds to event creators** (TBD).

### 🔔 Push Notifications
- Notifies users when an event **they registered for is approaching**.
- Ensures attendees never miss out on important events.

### 📸 Instagram Auto-Event Creation
- Periodically **checks Instagram posts** from official club accounts.
- Uses **Ollama AI** to extract event details from images.
- Auto-creates events under the respective club’s ID and **sends a push notification** for final verification.

### ⭐ Event Ratings & Leaderboard
- Users can **rate past events**.
- Maintains an **event history** and **average ratings**.
- Every **6 months**, generates a **leaderboard ranking clubs** based on event frequency and quality.
- Encourages clubs to **organize high-quality events**.

## Tech Stack
- **Frontend:** React (TypeScript, Vite)
- **Backend:** `db.py` (SQLite)
- **Payment Gateway:** Razorpay
- **Notifications:** Push API
- **AI Processing:** Ollama (for Instagram post analysis)

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yukii1004/event-management-system.git
   cd event-management-system/
   ```
2. Install dependencies:
   ```bash
   cd frontend/
   npm install  # For frontend
   
   cd ..

   cd backend/
   pip install -r requirements.txt  # For backend
   ```
3. Run the project:
   ```bash
   npm run dev  # Start frontend
   python app.py  # Start backend
   ```

## Contributing
Feel free to contribute by submitting a pull request or reporting issues!

## License
MIT License © 2025 Daddy_B

