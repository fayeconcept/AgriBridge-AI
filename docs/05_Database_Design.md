# AgriBridge AI - Database Design

## Overview

The database is the heart of AgriBridge AI. It stores information about users, farms, crops, AI conversations, marketplace products, weather data, and notifications.

A well-designed database ensures the platform is fast, secure, scalable, and reliable.

---

# Database Tables
## Table 1: Users

This table stores information about every person who uses AgriBridge AI.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique user ID |
| full_name | String | User's full name |
| email | String | Email address |
| phone | String | Mobile phone number |
| password_hash | String | Encrypted password |
| role | Enum | Farmer, Buyer, Admin, Extension Officer |
| country | String | User's country |
| state | String | User's state or region |
| preferred_language | String | User's preferred language |
| created_at | Timestamp | Account creation date |
| updated_at | Timestamp | Last update date |

---

### Why this table exists

Every feature in AgriBridge AI starts with a user account.

A user can:

- Register and log in.
- Own one or more farms.
- Chat with the AI assistant.
- Buy or sell products.
- Receive weather alerts and notifications.
## Table 2: Farms

This table stores information about farms owned by users.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique farm ID |
| user_id | UUID | Owner of the farm |
| farm_name | String | Name of the farm |
| location | String | Farm location |
| farm_size | Decimal | Size in hectares or acres |
| farm_type | Enum | Crop, Livestock, Mixed |
| latitude | Decimal | GPS latitude |
| longitude | Decimal | GPS longitude |
| created_at | Timestamp | Farm creation date |
| updated_at | Timestamp | Last update date |

---

### Relationship

One User can own many Farms.

The `user_id` field connects this table to the Users table.
## Table 3: Crops

This table stores all crops planted on a farm.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique crop ID |
| farm_id | UUID | References the farm that owns this crop |
| crop_name | String | Name of the crop |
| variety | String | Crop variety (optional) |
| planting_date | Date | Date planted |
| expected_harvest | Date | Expected harvest date |
| area_planted | Decimal | Size of land used |
| growth_stage | Enum | Seedling, Vegetative, Flowering, Harvest |
| health_status | Enum | Healthy, At Risk, Diseased |
| created_at | Timestamp | Record creation date |
| updated_at | Timestamp | Last update date |

---

### Why this table exists

Each farm can grow multiple crops.

This table allows AgriBridge AI to:

- Track planting schedules
- Predict harvest dates
- Monitor crop health
- Generate AI recommendations
- Estimate yields
## Table 4: AI Conversations

This table stores every conversation between a user and the AI assistant.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique conversation ID |
| user_id | UUID | References the user |
| question | Text | User's question |
| response | Text | AI's response |
| language | String | Language used in the conversation |
| created_at | Timestamp | Date and time of the conversation |

---

### Why this table exists

This table allows AgriBridge AI to:

- Save chat history
- Continue previous conversations
- Learn common farming challenges
- Provide personalized recommendations
## Table 5: Marketplace

This table stores products that farmers list for sale.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique product listing ID |
| seller_id | UUID | References the user selling the product |
| product_name | String | Name of the product |
| category | String | Product category (e.g., Grain, Vegetable, Fruit) |
| quantity | Decimal | Quantity available |
| unit | String | Unit of measurement (kg, bags, tonnes, etc.) |
| price | Decimal | Price per unit |
| location | String | Product location |
| status | Enum | Available, Reserved, Sold |
| created_at | Timestamp | Listing creation date |
| updated_at | Timestamp | Last update date |

---

### Why this table exists

This table allows farmers to:

- Sell produce online
- Reach more buyers
- Update product availability
- Manage sales listings
## Table 6: Notifications

This table stores notifications sent to users.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique notification ID |
| user_id | UUID | References the user |
| title | String | Notification title |
| message | Text | Notification message |
| notification_type | Enum | Weather, AI, Marketplace, Reminder, System |
| is_read | Boolean | Whether the user has read the notification |
| created_at | Timestamp | Date and time the notification was created |

---

### Why this table exists

This table allows AgriBridge AI to:

- Send weather alerts
- Notify farmers of AI recommendations
- Inform sellers when buyers are interested
- Remind farmers about important farming activities
- Send important system announcements