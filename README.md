# Hospital Bed Booking System

A desktop-based Hospital Bed Booking System built using **Python, Tkinter, and SQLite** as a learning project to explore SQL, database management, and GUI development.

## Overview

The application provides a graphical interface for managing hospital bed availability and bookings. Users can create profiles, log in, view their profile information, book beds, release their own bookings, and check bed availability.

SQLite is used to store user profiles and bed booking information locally.

## Features

- **User Registration and Login:** Create a user profile and authenticate using a username and password.
- **Bed Booking:** Book a bed by selecting its type, number, and booking duration.
- **Bed Availability:** View available and occupied beds through a graphical grid.
- **Release Bookings:** Release beds booked by the currently logged-in user.
- **Profile Information:** View registered user details.
- **Persistent Storage:** Store user and bed information in a local SQLite database.
- **Visual Status Indicators:** Use different colours to distinguish available beds, the current user's bookings, and beds booked by other users.

## Bed Categories

The application initializes 30 beds across three categories:

- Luxury Bed — 10 beds
- AC Bed — 10 beds
- Normal Bed — 10 beds

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Tkinter | Desktop graphical user interface |
| SQLite | Local relational database |
| SQL | Data creation, retrieval, and modification |

## Database Design

The application uses two primary tables:

### `users`

Stores user profile information, including:

- `username`
- `password`
- `gender`
- `age`
- `bed_type`

### `beds`

Stores bed availability and booking information, including:

- `bed_type`
- `bed_number`
- `status`
- `booked_by`
- `booking_time`
- `booking_duration`

The `beds` table uses a composite primary key consisting of `bed_type` and `bed_number`.

## SQL Concepts Practiced

This project helped explore:

- Creating tables using `CREATE TABLE IF NOT EXISTS`
- Retrieving records using `SELECT`
- Adding records using `INSERT`
- Updating booking information using `UPDATE`
- Primary keys and basic data integrity
- Parameterized SQL queries
- Database initialization and persistence
- Connecting a Python application to SQLite

## Requirements

- Python 3
- Tkinter, included with many standard Python installations
- SQLite, included through Python's `sqlite3` module

No external database server is required.

## How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/hospital-bed-booking-system.git
   ```

2. Navigate to the project directory:

   ```bash
   cd hospital-bed-booking-system
   ```

3. Run the application:

   ```bash
   python hosbed.py
   ```

The application initializes its local SQLite database when it starts.

## Learning Outcomes

Through this project, I explored how to:

- Integrate SQL queries with a Python application.
- Design basic relational tables.
- Perform database operations through a GUI.
- Manage booking state and availability.
- Connect user actions to database updates.
- Build a desktop application using Tkinter.

## Future Improvements

- Password hashing and stronger authentication.
- Improved input validation and error handling.
- Better separation of GUI, database, and application logic.
- Automated tests for booking and database operations.
- More robust booking-duration and expiry handling.
- Improved interface design and user experience.

## Project Status

This is an educational project created to practice Python, SQL, SQLite, and desktop application development. It is not intended for real-world hospital operations.

