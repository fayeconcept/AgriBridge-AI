# AgriBridge AI - API Design

## Overview

The API (Application Programming Interface) is the communication layer of AgriBridge AI.

It connects the frontend, backend, database, Gemini AI, and external services.

Every request from a user passes through the API before reaching the database or AI.

---

# API Modules
## Module 1: Authentication API

This module manages user authentication and account security.

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/auth/register | Register a new user |
| POST | /api/v1/auth/login | Log in a user |
| POST | /api/v1/auth/logout | Log out the current user |
| POST | /api/v1/auth/forgot-password | Request a password reset |
| POST | /api/v1/auth/reset-password | Reset the user's password |
| GET | /api/v1/auth/profile | Get the logged-in user's profile |

---

### Why this module exists

The Authentication API ensures that:

- Only authorized users can access the platform.
- User accounts remain secure.
- Farmers, buyers, and administrators can safely sign in.
## Module 2: Farm Management API

This module allows farmers to manage their farms.

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/farms | Create a new farm |
| GET | /api/v1/farms | Get all farms for the logged-in user |
| GET | /api/v1/farms/{farm_id} | Get details of a specific farm |
| PUT | /api/v1/farms/{farm_id} | Update a farm |
| DELETE | /api/v1/farms/{farm_id} | Delete a farm |

---

### Why this module exists

The Farm Management API allows users to:

- Register one or more farms
- Update farm details
- View farm information
- Remove farms that are no longer active
## Module 3: AI Assistant API

This module connects AgriBridge AI to Google's Gemini AI.

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/ai/chat | Send a question to the AI assistant |
| POST | /api/v1/ai/diagnose | Analyze a crop image for disease detection |
| POST | /api/v1/ai/recommend | Get farming recommendations |
| GET | /api/v1/ai/history | Retrieve previous AI conversations |

---

### Why this module exists

The AI Assistant API enables farmers to:

- Ask agricultural questions
- Diagnose crop diseases from images
- Receive personalized farming advice
- View previous AI conversations## Module 4: Marketplace API

This module manages agricultural products listed for sale.

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /api/v1/marketplace/products | Create a product listing |
| GET | /api/v1/marketplace/products | Get all available products |
| GET | /api/v1/marketplace/products/{product_id} | Get product details |
| PUT | /api/v1/marketplace/products/{product_id} | Update a product listing |
| DELETE | /api/v1/marketplace/products/{product_id} | Remove a product listing |

---

### Why this module exists

The Marketplace API allows farmers to:

- Sell agricultural products
- Reach buyers across different locations
- Update product availability
- Manage product listings
## Module 5: Notifications API

This module manages notifications sent to users.

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | /api/v1/notifications | Get all notifications for the logged-in user |
| GET | /api/v1/notifications/{notification_id} | Get a specific notification |
| PUT | /api/v1/notifications/{notification_id}/read | Mark a notification as read |
| DELETE | /api/v1/notifications/{notification_id} | Delete a notification |

---

### Why this module exists

The Notifications API allows AgriBridge AI to:

- Deliver weather alerts
- Send AI recommendations
- Notify users about marketplace activities
- Remind farmers about important farming tasks
- Deliver important system announcements
