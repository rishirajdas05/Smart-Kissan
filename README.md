<h1 align="center"> Smart-Kissan </h1>
<p align="center"> Transforming Agriculture through Intelligent Soil Analytics, Real-time Market Intelligence, and Predictive Climate Insights </p>

<p align="center">
  <img alt="Build" src="https://img.shields.io/badge/Build-Passing-brightgreen?style=for-the-badge">
  <img alt="Issues" src="https://img.shields.io/badge/Issues-0%20Open-blue?style=for-the-badge">
  <img alt="Contributions" src="https://img.shields.io/badge/Contributions-Welcome-orange?style=for-the-badge">
 
</p>
<!-- 
  **Note:** These are static placeholder badges. Replace them with your project's actual badges.
  You can generate your own at https://shields.io
-->

## 📑 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Tech Stack & Architecture](#-tech-stack--architecture)
- [Project Structure](#-project-structure)
- [Environment Variables](#-environment-variables)
- [API Keys Setup](#-api-keys-setup)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Contributing](#-contributing)

---

## 🌟 Overview

### Hook
Smart-Kissan is a comprehensive agricultural intelligence platform that empowers farmers with data-driven insights, ranging from machine-learning-based soil analysis to real-time market price tracking and hyper-local weather forecasting.

### The Problem
> Traditional farming often relies on historical intuition, which is increasingly challenged by climate volatility, soil degradation, and unpredictable market fluctuations. Small-scale farmers frequently lack access to scientific soil testing and real-time commodity pricing (Mandi prices), leading to suboptimal crop selection, reduced yields, and financial vulnerability during the selling season.

### The Solution
Smart-Kissan bridges the digital divide by providing a unified, multi-lingual ecosystem. By integrating Machine Learning for crop recommendation, Agmarknet APIs for live market data, and OpenWeatherMap for climate precision, the platform transforms raw agricultural data into actionable strategy. Whether it is estimating potential yield before a single seed is sown or locating the best market prices in nearby regions, Smart-Kissan serves as a digital co-pilot for the modern agriculturist.

### Architecture Overview
The system follows a robust **MVC (Model-View-Controller)** pattern implemented via the **Django** framework. The core logic is bifurcated into a high-performance **ML Engine** (using scikit-learn for predictive modeling) and a dynamic **Weather/Market Intelligence service**. Data flow is managed through structured Django models, with a sophisticated caching and translation layer ensuring accessibility across different linguistic demographics.

---

## ✨ Key Features

Smart-Kissan is designed around the core needs of a farmer's lifecycle, from preparation to profit.

- 🧪 **AI-Powered Soil Analyzer:** Users can input soil parameters including Nitrogen (N), Phosphorus (P), Potassium (K), and pH levels. The underlying ML engine processes these along with regional data to recommend the most suitable crops for that specific plot.
- 💰 **Live Mandi Price Locator:** Integrated with the Agmarknet API (data.gov.in), this feature allows farmers to track real-time commodity prices across various markets, ensuring they sell their produce at the most competitive rates.
- 🌤️ **Precision Weather Forecasting:** Provides a comprehensive 7-day weather forecast using the OpenWeatherMap API. This enables farmers to plan irrigation, pesticide application, and harvesting around predictable weather patterns.
- 📊 **Dynamic Yield & Income Estimator:** Before planting, users can estimate their potential productivity and revenue based on land area and selected crop types, allowing for better financial planning.
- 🌐 **Multi-Lingual Accessibility:** Utilizing a tiered translation system (Database Cache -> MyMemory API -> LibreTranslate), the platform ensures that complex agricultural insights are available in the user's preferred local language.
- 🤖 **Interactive AI Chat Support:** A dedicated agricultural chatbot interface to answer queries ranging from pest control to fertilizer recommendations in real-time.
- 📅 **Regional Crop Calendar:** Automatically adapts to the user's geographic location to suggest optimal sowing and harvesting windows.

---

## 🛠️ Tech Stack & Architecture

The project utilizes a curated selection of industry-standard technologies to ensure scalability, accuracy, and performance.

| Technology | Purpose | Why it was Chosen |
| :--- | :--- | :--- |
| **Django** | Primary Backend Framework | Offers a secure, "batteries-included" environment for rapid development and robust user management. |
| **Python** | Logic & ML Computation | The gold standard for data science and backend automation, enabling seamless integration with ML libraries. |
| **scikit-learn** | Machine Learning Engine | Provides efficient tools for predictive data analysis used in crop recommendation and yield estimation. |
| **OpenWeatherMap API** | Climate Data | Delivers reliable, hyper-local weather forecasts and current atmospheric conditions. |
| **Agmarknet API** | Market Intelligence | The authoritative source for live commodity prices across Indian markets (Mandi). |
| **MyMemory/LibreTranslate** | Translation Services | Ensures high availability for multi-lingual support through primary and fallback translation APIs. |

---

## 📁 Project Structure

```
rishirajdas05-Smart-Kissan-bd457b1/
├── 📁 core/                        # Core application logic
│   ├── 📄 ml_engine.py             # ML prediction logic (13-feature vector)
│   ├── 📄 weather.py               # Weather & Mandi API integrations
│   ├── 📄 translation.py           # Multi-language logic (MyMemory/LibreTranslate)
│   ├── 📄 models.py                # Database schemas for Soil Analysis & Translations
│   ├── 📄 views.py                 # Core functional views (Dashboard, Analyzer, etc.)
│   ├── 📁 ml_models/               # Model training scripts
│   │   └── 📄 train_model.py       # Script to train and save predictive models
│   ├── 📁 templatetags/            # Custom Django template filters
│   │   ├── 📄 i18n_tags.py         # Internationalization tags
│   │   └── 📄 custom_filters.py    # Utility filters for UI
│   └── 📄 context_processors.py    # Global language context injector
├── 📁 smart_kissan/                # Main project configuration
│   ├── 📄 settings.py              # Global project settings
│   ├── 📄 urls.py                  # Root URL routing
│   └── 📄 wsgi.py                  # Deployment entry point
├── 📁 accounts/                    # User authentication and profiles
│   ├── 📄 models.py                # UserProfile and avatar management
│   └── 📄 views.py                 # Signup/Login logic
├── 📁 templates/                   # HTML Frontend layer
│   ├── 📁 core/                    # App-specific templates (Home, Soil, Prices)
│   ├── 📁 accounts/                # Auth templates
│   └── 📄 base.html                # Master layout template
├── 📁 static/                      # Static assets
│   ├── 📁 core/                    # CSS and specific UI images
│   └── 📁 recommender/             # Frontend JavaScript (app.js, ui.js)
├── 📄 manage.py                    # Django management script
├── 📄 requirements.txt             # Project dependencies
├── 📄 render.yaml                  # Deployment configuration
├── 📄 build.sh                     # Automated build script
├── 📄 .env.example                 # Environment variable template
└── 📄 .python-version              # Python version specification
```

---

## 🔐 Environment Variables

To run Smart-Kissan, you must configure the following environment variables. Use the provided `.env.example` as a template.

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `DJANGO_SECRET_KEY` | Secret key for cryptographic signing | `django-insecure-xxx...` |
| `DJANGO_DEBUG` | Toggle debug mode (Set to False in production) | `True` or `False` |
| `OPENWEATHER_API_KEY` | API key from OpenWeatherMap | `a1b2c3d4...` |
| `DEFAULT_WEATHER_CITY` | Default city for weather display | `Kolkata` |
| `DEFAULT_WEATHER_COUNTRY` | Default country code | `IN` |

---

## 🚀 Getting Started

### Prerequisites
*   **Python:** 3.9+ 
*   **Package Manager:** `pip`

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/rishirajdas05/Smart-Kissan.git
    cd rishirajdas05-Smart-Kissan-bd457b1
    ```

2.  **Initialize Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment:**
    ```bash
    cp .env.example .env
    # Edit .env and add your OPENWEATHER_API_KEY
    ```

5.  **Database Setup:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Train the ML Model:**
    ```bash
    python core/ml_models/train_model.py
    ```

7.  **Launch the Application:**
    ```bash
    python manage.py runserver
    ```

---

## 🔧 Usage

### 🗺️ Soil Analysis & Prediction
Navigate to the **Soil Analyzer** page. Input the values for Nitrogen, Phosphorus, Potassium, and pH levels. The ML Engine will process these inputs using a 13-feature vector (incorporating regional bias and seasonal data) to predict the crop that will yield the highest success rate.

### 💰 Tracking Market Prices
Access the **Crop Prices** or **Mandi Locator** section. The application fetches live data from the Agmarknet API. You can filter by region or commodity to see the latest minimum, maximum, and modal prices recorded at government-regulated markets.

### ☁️ Weather Monitoring
The **Weather Forecast** page provides a 7-day outlook. The system uses your profile's default city or your current IP location to fetch atmospheric data, including temperature, humidity, and rainfall probability, helping you stay ahead of climate risks.

### 📈 Yield Estimation
Enter your land area and target crop into the **Yield Estimator**. The system utilizes historical averages and regional parameters to provide a forecasted income statement for your next harvest.

---

## 🤝 Contributing

We welcome contributions to improve Smart-Kissan! Your input helps make this project better for farmers everywhere.

### How to Contribute

1. **Fork the repository** - Click the 'Fork' button at the top right of this page.
2. **Create a feature branch** 
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** - Improve code, documentation, or the ML models.
4. **Test thoroughly** - Ensure all functionality works as expected.
   ```bash
   python manage.py test
   ```
5. **Commit your changes** - Write clear, descriptive commit messages.
   ```bash
   git commit -m 'Add: ML model optimization for arid regions'
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** - Submit your changes for review.

### Development Guidelines

- ✅ Follow PEP 8 style guidelines for Python code.
- 📝 Add docstrings to all new functions in `ml_engine.py` or `weather.py`.
- 🧪 Ensure migrations are generated for any model changes.
- 🔄 Maintain backward compatibility with existing Soil Analysis data.

---

<p align="center">Made with ❤️ for the Global Farming Community</p>
<p align="center">
  <a href="#">⬆️ Back to Top</a>
</p>
