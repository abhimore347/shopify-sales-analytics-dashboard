Sales Dashboard (Python + Tkinter)
Overview
A desktop-based Sales Analytics Dashboard built with Python, Tkinter, Pandas, and Matplotlib. Upload a CSV file and generate interactive visual insights instantly.
Features
• Upload CSV sales data
• KPI Metrics: Total Orders, Total Revenue, Unique Products
• Visual Reports: Orders by Date, Top Products, Top Locations, Payment Method Distribution, Discount Usage, Vendor Sales
• Export charts as PNG and PDF
• Clean and scrollable UI dashboard
Tech Stack
• Python 3.8+
• Tkinter (GUI)
• Pandas (data processing)
• Matplotlib (visualization)
Installation
1. Clone the repository:
git clone <your-repo-url>
cd <project-folder>
2. Create virtual environment:
python -m venv venv
3. Activate environment:
Windows:
venv\Scripts\activate

Linux/macOS:
source venv/bin/activate
4. Install dependencies:
pip install -r requirements.txt
Run the Application
python main.py
Project Structure
project/
│── main.py
│── gui.py
│── analyzer.py
│── file_handler.py
│── requirements.txt
│── setup.sh
│── setup.bat
How to Use
• Launch the app
• Click "Upload CSV"
• Select dataset
• View KPI metrics
• Explore charts
• Export charts as PNG or PDF
Expected CSV Columns
• Name (Order ID)
• Created at (Order Date)
• Lineitem name (Product Name)
• Lineitem quantity (Quantity)
• Lineitem price (Price)
• Shipping City
• Payment Method
• Discount Code
• Vendor
Requirements
pandas>=1.5.0
matplotlib>=3.7.0
Setup Scripts
setup.sh:
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
setup.bat:
@echo off
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
pause
Troubleshooting
• Install tkinter if missing (Linux: sudo apt-get install python3-tk)
• Ensure CSV column names match expected format
• Large datasets may take time to render charts
License
This project is open-source and free to use.
