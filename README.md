# EconBank – Interactive Economics & Financial Literacy Platform

**EconBank** is an interactive, web-based economics education platform built with Python and Streamlit. Its purpose is to teach users essential economic and financial literacy concepts through hands-on money management, transaction tracking, and economic data visualization.

Rather than simply teaching economics through textbooks, EconBank allows users to experience financial decision-making firsthand by tracking money earned, spent, given, and received.

---

## Project Mission

EconBank aims to make economics accessible, engaging, and practical.

By providing users with a simulated financial management environment, the platform encourages users to:
- Understand how money flows through an economy.
- Develop responsible spending and saving habits.
- Recognize the relationship between income, expenses, and financial balance.
- Analyze personal and collective economic trends.
- Learn how individual financial decisions contribute to broader economic activity.

## Features

### User Accounts
- Individual account registration and login.
- Secure password hashing.
- Personalized financial dashboards.
- Private transaction histories for each user.

### Personal Dashboard

Users can access three main sections:

**1. Summary**
- Total money earned.
- Total money spent.
- Total money given.
- Total money received.
- Current account balance.

**2. Transactions**
- Record individual financial transactions.
- View transaction histories.
- Track transaction descriptions, amounts, and timestamps.
- Visualize spending and income by transaction type.

**3. Statistics**
- View financial trends over time.
- Analyze transaction patterns.
- Compare different categories of financial activity.

### Transaction Management

Users can record four types of transactions:

| Transaction | Description |
|---|---|
| Earned | Money received through work or other income sources. |
| Spent | Money used to purchase goods or services. |
| Given | Money transferred or gifted to another person. |
| Received | Money received from another person. |

Account balances are calculated using:

**Balance = Earned + Received − Spent − Given**

### Administrator Dashboard

Administrators have access to a centralized overview of platform activity.

Admin capabilities include:
- View transactions across all user accounts.
- Monitor total money earned, spent, given, and received.
- Analyze transaction activity across users.
- View aggregate economic trends.
- Compare financial activity between accounts.
- Monitor the overall flow of money through the platform.

### Economic Data Visualization

EconBank uses charts and financial metrics to help users understand economic activity.

Visualizations include:
- Transaction trends over time.
- Financial activity by transaction type.
- Total transaction amounts by user.
- Aggregate economic activity across the platform.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Interactive web application framework |
| Pandas | Financial data processing and analysis |
| SQLite / Cloud Database | Persistent data storage (planned or implemented depending on deployment) |
| JSON | Original local data storage |
| Hashlib | Password hashing |
| GitHub | Source code management |
| Streamlit Community Cloud | Web application deployment |

---

## Getting Started

### Prerequisites

Install the following:
- Python 3.9 or newer
- Git
- Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/felicia-guo/EconBank.git
```

### 2. Navigate to the Project Folder

```bash
cd EconBank
```

### 3. Install Dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Launch the Application

```bash
python3 -m streamlit run econApp.py
```

The application should automatically open in your browser.

If it doesn't, visit:

```text
http://localhost:8501
```

---

## Deployment

EconBank can be deployed using **Streamlit Community Cloud**.

1. Push the project to GitHub.
2. Visit https://share.streamlit.io/
3. Sign in using your GitHub account.
4. Select the EconBank repository.
5. Choose the `main` branch.
6. Set the main file path to `econApp.py`.
7. Click Deploy.

Once deployment is complete, the application will have a public URL that users can access from different devices.

---

## Data Storage & Persistence

EconBank requires centralized data storage to ensure that users and administrators access the same financial records across devices.

The original version uses a local JSON file (`economics_data.json`).

However, local files on Streamlit Community Cloud are not guaranteed to persist after application restarts or redeployments.

**Recommended future implementation:**
- Use a hosted PostgreSQL database or another managed cloud database.
- Store user accounts and transactions centrally.
- Ensure transaction records persist across deployments.
- Allow administrators to access updated platform-wide financial data.

---

## Future Development

Potential improvements include:

- [ ] Centralized cloud database integration.
- [ ] More advanced user authentication and account security.
- [ ] Transaction categories (food, entertainment, transportation, etc.).
- [ ] Monthly and yearly financial reports.
- [ ] Budget creation and tracking.
- [ ] Savings goals.
- [ ] Interactive economic simulations.
- [ ] Supply and demand simulations.
- [ ] Inflation and interest rate demonstrations.
- [ ] Economic indicators and aggregate statistics.
- [ ] Improved administrator analytics.
- [ ] Exportable financial reports.

---

## Educational Impact

EconBank is designed to bridge the gap between economic theory and real-world financial decision-making.

Through interactive financial tracking and economic visualization, users can explore concepts such as:
- Personal finance and budgeting.
- Income and expenditure.
- Financial responsibility.
- Money circulation.
- Supply and demand.
- Economic growth and trends.
- The relationship between individual and collective economic activity.

The ultimate goal is to transform economics from an abstract academic subject into an interactive learning experience.

---

## Project Information

**Project:** EconBank  
**Category:** Economics Education / Financial Literacy / Technology  
**Framework:** Python + Streamlit  
**Repository:** https://github.com/felicia-guo/EconBank

**Created to make economics more interactive, accessible, and practical.**
