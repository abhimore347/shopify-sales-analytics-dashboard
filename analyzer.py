import pandas as pd

class SalesAnalyzer:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        self.df.columns = self.df.columns.str.strip()
        self.df.dropna(how='all', inplace=True)

    # ✅ FIXED (no datetime conversion here)
    def orders_by_date(self):
        return self.df.groupby('Created at')['Name'].count()

    def product_sales(self):
        return self.df.groupby('Lineitem name')['Lineitem quantity'].sum().sort_values(ascending=False)

    def location_sales(self):
        return self.df.groupby('Shipping City')['Lineitem quantity'].sum().sort_values(ascending=False)

    def payment_type(self):
        return self.df['Payment Method'].fillna('Unknown').value_counts()

    def discount_usage(self):
        return self.df['Discount Code'].fillna('No Discount').value_counts()

    def vendor_sales(self):
        return self.df.groupby('Vendor')['Lineitem quantity'].sum().sort_values(ascending=False)