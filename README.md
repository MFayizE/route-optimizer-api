# 🚀 Route Optimizer API

## 📌 Description
A Django-based API that calculates the most cost-effective fuel stops along a route in the USA. It utilizes **OpenRouteService** for routing and dynamically loads fuel prices from a CSV file, ensuring efficient trip planning with minimal API calls.

## 🌟 Features
- 📍 **Accepts Start & Finish Locations** (Within the USA).
- 🗺️ **Returns Route Map** using OpenRouteService.
- ⛽ **Finds Cheapest Fuel Stops** based on CSV fuel price data.
- 🚗 **Assumes Vehicle Range** of **500 miles per tank** and **10 MPG efficiency**.
- 💰 **Calculates Total Fuel Cost** for the journey.
- ⚡ **Optimized API Calls** (Minimal calls to routing API for efficiency).

---

## ⚙️ Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/MFayizE/route-optimizer-api.git
cd route-optimizer-api
```

### **2️⃣ Create a Virtual Environment & Install Dependencies**
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### **3️⃣ Set Up Environment Variables**
1. Create a `.env` file in the root directory.
2. Add your **OpenRouteService API Key**:

```sh
ROUTING_API_KEY=your_actual_api_key_here
```

### **4️⃣ Run Migrations & Load Fuel Data**
```sh
python manage.py migrate
```

### **5️⃣ Start the Server**
```sh
python manage.py runserver
```

---

## 🎯 API Usage (Postman / cURL)
### **Endpoint: Get Optimized Route & Fuel Stops**
```sh
GET http://127.0.0.1:8000/api/route/?start=Los+Angeles,CA&finish=New+York,NY
```

### **Sample Response:**
```json
{
    "start": "Los Angeles, CA",
    "finish": "New York, NY",
    "route_map": "geojson_data_here",
    "total_distance_miles": 2800.03,
    "fuel_stops": [
        { "name": "7-ELEVEN #218", "address": "I-44, EXIT 4", "city": "Harrold", "state": "TX", "price_per_gallon": 2.69 },
        { "name": "Chevron", "address": "I-10, EXIT 858", "city": "Vidor", "state": "TX", "price_per_gallon": 2.75 }
    ],
    "total_fuel_cost": 820.45
}
```

---

## 🛠 Tech Stack
- **Backend**: Django, Django REST Framework
- **Routing API**: OpenRouteService
- **Data Handling**: Pandas for CSV fuel price processing
- **Environment Variables**: Python dotenv

---

## 📌 GitHub Repository Setup & Deployment

### **1️⃣ Initialize a New Git Repository**
```sh
git init
git add .
git commit -m "Initial commit"
```

### **2️⃣ Add Remote Repository & Push**
```sh
git remote add origin https://github.com/MFayizE/route-optimizer-api.git
git branch -M main
git push -u origin main
```

