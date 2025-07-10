
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import json
import os
from typing import Dict, List, Any
import csv

class BusinessTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Business Financial Management System")
        self.root.geometry("1200x700")
        
        # Data storage
        self.data_file = "business_data.json"
        self.data = self.load_data()
        
        # Create main interface
        self.create_widgets()
        self.refresh_displays()
        
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file or create default structure"""
        default_data = {
            "income": [],
            "expenses": [],
            "sales": [],
            "stock": [],
            "settings": {
                "currency": "$",
                "business_name": "My Business"
            }
        }
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    # Ensure all required keys exist
                    for key in default_data:
                        if key not in data:
                            data[key] = default_data[key]
                    return data
            except:
                return default_data
        return default_data
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
            messagebox.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
    def create_widgets(self):
        """Create the main GUI interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_income_tab()
        self.create_expenses_tab()
        self.create_sales_tab()
        self.create_stock_tab()
        self.create_reports_tab()
        self.create_settings_tab()
        
        # Bottom frame for save/load buttons
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(bottom_frame, text="Save Data", command=self.save_data, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Export to CSV", command=self.export_to_csv,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Refresh", command=self.refresh_displays,
                 bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    
    def create_income_tab(self):
        """Create income tracking tab"""
        income_frame = ttk.Frame(self.notebook)
        self.notebook.add(income_frame, text="Income")
        
        # Input section
        input_frame = tk.LabelFrame(income_frame, text="Add Income", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.income_date = tk.Entry(input_frame, width=12)
        self.income_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.income_date.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Source:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.income_source = tk.Entry(input_frame, width=20)
        self.income_source.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(input_frame, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.income_amount = tk.Entry(input_frame, width=12)
        self.income_amount.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Description:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.income_desc = tk.Entry(input_frame, width=30)
        self.income_desc.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Button(input_frame, text="Add Income", command=self.add_income,
                 bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=4, pady=10)
        
        # Display section
        display_frame = tk.LabelFrame(income_frame, text="Income Records", padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Treeview for income records
        columns = ("Date", "Source", "Amount", "Description")
        self.income_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.income_tree.heading(col, text=col)
            self.income_tree.column(col, width=150)
        
        scrollbar_income = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.income_tree.yview)
        self.income_tree.configure(yscrollcommand=scrollbar_income.set)
        
        self.income_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_income.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        tk.Button(display_frame, text="Delete Selected", command=lambda: self.delete_record("income"),
                 bg="#f44336", fg="white").pack(pady=5)
    
    def create_expenses_tab(self):
        """Create expenses tracking tab"""
        expenses_frame = ttk.Frame(self.notebook)
        self.notebook.add(expenses_frame, text="Expenses")
        
        # Input section
        input_frame = tk.LabelFrame(expenses_frame, text="Add Expense", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.expense_date = tk.Entry(input_frame, width=12)
        self.expense_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.expense_date.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Category:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.expense_category = ttk.Combobox(input_frame, width=17, values=[
            "Office Supplies", "Marketing", "Utilities", "Rent", "Equipment", 
            "Travel", "Meals", "Professional Services", "Insurance", "Other"
        ])
        self.expense_category.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(input_frame, text="Amount:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.expense_amount = tk.Entry(input_frame, width=12)
        self.expense_amount.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Description:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.expense_desc = tk.Entry(input_frame, width=30)
        self.expense_desc.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Button(input_frame, text="Add Expense", command=self.add_expense,
                 bg="#f44336", fg="white").grid(row=2, column=0, columnspan=4, pady=10)
        
        # Display section
        display_frame = tk.LabelFrame(expenses_frame, text="Expense Records", padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Date", "Category", "Amount", "Description")
        self.expense_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.expense_tree.heading(col, text=col)
            self.expense_tree.column(col, width=150)
        
        scrollbar_expense = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        self.expense_tree.configure(yscrollcommand=scrollbar_expense.set)
        
        self.expense_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_expense.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(display_frame, text="Delete Selected", command=lambda: self.delete_record("expenses"),
                 bg="#f44336", fg="white").pack(pady=5)
    
    def create_sales_tab(self):
        """Create sales tracking tab"""
        sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="Sales")
        
        # Input section
        input_frame = tk.LabelFrame(sales_frame, text="Add Sale", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sale_date = tk.Entry(input_frame, width=12)
        self.sale_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.sale_date.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Product/Service:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.sale_product = tk.Entry(input_frame, width=20)
        self.sale_product.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(input_frame, text="Quantity:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.sale_quantity = tk.Entry(input_frame, width=12)
        self.sale_quantity.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Unit Price:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.sale_price = tk.Entry(input_frame, width=12)
        self.sale_price.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Label(input_frame, text="Customer:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sale_customer = tk.Entry(input_frame, width=20)
        self.sale_customer.grid(row=2, column=1, padx=5, pady=2)
        
        tk.Button(input_frame, text="Add Sale", command=self.add_sale,
                 bg="#2196F3", fg="white").grid(row=3, column=0, columnspan=4, pady=10)
        
        # Display section
        display_frame = tk.LabelFrame(sales_frame, text="Sales Records", padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Date", "Product", "Quantity", "Unit Price", "Total", "Customer")
        self.sales_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(col, width=120)
        
        scrollbar_sales = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=scrollbar_sales.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_sales.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(display_frame, text="Delete Selected", command=lambda: self.delete_record("sales"),
                 bg="#f44336", fg="white").pack(pady=5)
    
    def create_stock_tab(self):
        """Create stock management tab"""
        stock_frame = ttk.Frame(self.notebook)
        self.notebook.add(stock_frame, text="Stock")
        
        # Input section
        input_frame = tk.LabelFrame(stock_frame, text="Add/Update Stock", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Product Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.stock_product = tk.Entry(input_frame, width=20)
        self.stock_product.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Quantity:").grid(row=0, column=2, sticky=tk.W, pady=2)
        self.stock_quantity = tk.Entry(input_frame, width=12)
        self.stock_quantity.grid(row=0, column=3, padx=5, pady=2)
        
        tk.Label(input_frame, text="Unit Cost:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.stock_cost = tk.Entry(input_frame, width=12)
        self.stock_cost.grid(row=1, column=1, padx=5, pady=2)
        
        tk.Label(input_frame, text="Supplier:").grid(row=1, column=2, sticky=tk.W, pady=2)
        self.stock_supplier = tk.Entry(input_frame, width=20)
        self.stock_supplier.grid(row=1, column=3, padx=5, pady=2)
        
        tk.Button(input_frame, text="Add/Update Stock", command=self.add_stock,
                 bg="#9C27B0", fg="white").grid(row=2, column=0, columnspan=4, pady=10)
        
        # Display section
        display_frame = tk.LabelFrame(stock_frame, text="Stock Records", padx=10, pady=10)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Product", "Quantity", "Unit Cost", "Total Value", "Supplier")
        self.stock_tree = ttk.Treeview(display_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
            self.stock_tree.column(col, width=140)
        
        scrollbar_stock = ttk.Scrollbar(display_frame, orient=tk.VERTICAL, command=self.stock_tree.yview)
        self.stock_tree.configure(yscrollcommand=scrollbar_stock.set)
        
        self.stock_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_stock.pack(side=tk.RIGHT, fill=tk.Y)
        
        tk.Button(display_frame, text="Delete Selected", command=lambda: self.delete_record("stock"),
                 bg="#f44336", fg="white").pack(pady=5)
    
    def create_reports_tab(self):
        """Create reports and summary tab"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="Reports & Summary")
        
        # Summary section
        summary_frame = tk.LabelFrame(reports_frame, text="Financial Summary", padx=10, pady=10)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.summary_text = tk.Text(summary_frame, height=15, width=70)
        summary_scrollbar = ttk.Scrollbar(summary_frame, orient=tk.VERTICAL, command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=summary_scrollbar.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(reports_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(buttons_frame, text="Generate Monthly Report", command=self.generate_monthly_report,
                 bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Generate Profit Analysis", command=self.generate_profit_analysis,
                 bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Stock Valuation Report", command=self.generate_stock_report,
                 bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
    
    def create_settings_tab(self):
        """Create settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Settings input
        input_frame = tk.LabelFrame(settings_frame, text="Business Settings", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(input_frame, text="Business Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.business_name = tk.Entry(input_frame, width=30)
        self.business_name.insert(0, self.data["settings"]["business_name"])
        self.business_name.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(input_frame, text="Currency Symbol:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.currency_symbol = tk.Entry(input_frame, width=10)
        self.currency_symbol.insert(0, self.data["settings"]["currency"])
        self.currency_symbol.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(input_frame, text="Save Settings", command=self.save_settings,
                 bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)
    
    def add_income(self):
        """Add income record"""
        try:
            record = {
                "date": self.income_date.get(),
                "source": self.income_source.get(),
                "amount": float(self.income_amount.get()),
                "description": self.income_desc.get()
            }
            self.data["income"].append(record)
            self.refresh_income_display()
            self.clear_income_fields()
            messagebox.showinfo("Success", "Income added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amount")
    
    def add_expense(self):
        """Add expense record"""
        try:
            record = {
                "date": self.expense_date.get(),
                "category": self.expense_category.get(),
                "amount": float(self.expense_amount.get()),
                "description": self.expense_desc.get()
            }
            self.data["expenses"].append(record)
            self.refresh_expense_display()
            self.clear_expense_fields()
            messagebox.showinfo("Success", "Expense added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid amount")
    
    def add_sale(self):
        """Add sales record"""
        try:
            quantity = float(self.sale_quantity.get())
            unit_price = float(self.sale_price.get())
            total = quantity * unit_price
            
            record = {
                "date": self.sale_date.get(),
                "product": self.sale_product.get(),
                "quantity": quantity,
                "unit_price": unit_price,
                "total": total,
                "customer": self.sale_customer.get()
            }
            self.data["sales"].append(record)
            self.refresh_sales_display()
            self.clear_sales_fields()
            messagebox.showinfo("Success", "Sale added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and price")
    
    def add_stock(self):
        """Add or update stock record"""
        try:
            product = self.stock_product.get()
            quantity = float(self.stock_quantity.get())
            cost = float(self.stock_cost.get())
            supplier = self.stock_supplier.get()
            
            # Check if product already exists
            existing_index = None
            for i, stock in enumerate(self.data["stock"]):
                if stock["product"].lower() == product.lower():
                    existing_index = i
                    break
            
            record = {
                "product": product,
                "quantity": quantity,
                "unit_cost": cost,
                "total_value": quantity * cost,
                "supplier": supplier
            }
            
            if existing_index is not None:
                self.data["stock"][existing_index] = record
                messagebox.showinfo("Success", "Stock updated successfully!")
            else:
                self.data["stock"].append(record)
                messagebox.showinfo("Success", "Stock added successfully!")
            
            self.refresh_stock_display()
            self.clear_stock_fields()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid quantity and cost")
    
    def delete_record(self, record_type):
        """Delete selected record"""
        trees = {
            "income": self.income_tree,
            "expenses": self.expense_tree,
            "sales": self.sales_tree,
            "stock": self.stock_tree
        }
        
        tree = trees.get(record_type)
        if not tree:
            return
        
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            for item in selected:
                index = tree.index(item)
                del self.data[record_type][index]
            
            self.refresh_displays()
            messagebox.showinfo("Success", "Record deleted successfully!")
    
    def refresh_displays(self):
        """Refresh all displays"""
        self.refresh_income_display()
        self.refresh_expense_display()
        self.refresh_sales_display()
        self.refresh_stock_display()
    
    def refresh_income_display(self):
        """Refresh income treeview"""
        self.income_tree.delete(*self.income_tree.get_children())
        currency = self.data["settings"]["currency"]
        
        for record in self.data["income"]:
            self.income_tree.insert("", tk.END, values=(
                record["date"],
                record["source"],
                f"{currency}{record['amount']:.2f}",
                record["description"]
            ))
    
    def refresh_expense_display(self):
        """Refresh expense treeview"""
        self.expense_tree.delete(*self.expense_tree.get_children())
        currency = self.data["settings"]["currency"]
        
        for record in self.data["expenses"]:
            self.expense_tree.insert("", tk.END, values=(
                record["date"],
                record["category"],
                f"{currency}{record['amount']:.2f}",
                record["description"]
            ))
    
    def refresh_sales_display(self):
        """Refresh sales treeview"""
        self.sales_tree.delete(*self.sales_tree.get_children())
        currency = self.data["settings"]["currency"]
        
        for record in self.data["sales"]:
            self.sales_tree.insert("", tk.END, values=(
                record["date"],
                record["product"],
                record["quantity"],
                f"{currency}{record['unit_price']:.2f}",
                f"{currency}{record['total']:.2f}",
                record["customer"]
            ))
    
    def refresh_stock_display(self):
        """Refresh stock treeview"""
        self.stock_tree.delete(*self.stock_tree.get_children())
        currency = self.data["settings"]["currency"]
        
        for record in self.data["stock"]:
            self.stock_tree.insert("", tk.END, values=(
                record["product"],
                record["quantity"],
                f"{currency}{record['unit_cost']:.2f}",
                f"{currency}{record['total_value']:.2f}",
                record["supplier"]
            ))
    
    def clear_income_fields(self):
        """Clear income input fields"""
        self.income_date.delete(0, tk.END)
        self.income_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.income_source.delete(0, tk.END)
        self.income_amount.delete(0, tk.END)
        self.income_desc.delete(0, tk.END)
    
    def clear_expense_fields(self):
        """Clear expense input fields"""
        self.expense_date.delete(0, tk.END)
        self.expense_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.expense_category.set("")
        self.expense_amount.delete(0, tk.END)
        self.expense_desc.delete(0, tk.END)
    
    def clear_sales_fields(self):
        """Clear sales input fields"""
        self.sale_date.delete(0, tk.END)
        self.sale_date.insert(0, date.today().strftime("%Y-%m-%d"))
        self.sale_product.delete(0, tk.END)
        self.sale_quantity.delete(0, tk.END)
        self.sale_price.delete(0, tk.END)
        self.sale_customer.delete(0, tk.END)
    
    def clear_stock_fields(self):
        """Clear stock input fields"""
        self.stock_product.delete(0, tk.END)
        self.stock_quantity.delete(0, tk.END)
        self.stock_cost.delete(0, tk.END)
        self.stock_supplier.delete(0, tk.END)
    
    def save_settings(self):
        """Save application settings"""
        self.data["settings"]["business_name"] = self.business_name.get()
        self.data["settings"]["currency"] = self.currency_symbol.get()
        self.refresh_displays()
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def generate_monthly_report(self):
        """Generate monthly financial report"""
        current_month = date.today().strftime("%Y-%m")
        currency = self.data["settings"]["currency"]
        
        # Calculate monthly totals
        monthly_income = sum(record["amount"] for record in self.data["income"] 
                           if record["date"].startswith(current_month))
        monthly_expenses = sum(record["amount"] for record in self.data["expenses"] 
                             if record["date"].startswith(current_month))
        monthly_sales = sum(record["total"] for record in self.data["sales"] 
                          if record["date"].startswith(current_month))
        monthly_profit = monthly_income - monthly_expenses
        
        report = f"""
MONTHLY FINANCIAL REPORT - {current_month}
{'='*50}

INCOME:
Total Monthly Income: {currency}{monthly_income:.2f}

EXPENSES:
Total Monthly Expenses: {currency}{monthly_expenses:.2f}

SALES:
Total Monthly Sales: {currency}{monthly_sales:.2f}

PROFIT/LOSS:
Net Profit: {currency}{monthly_profit:.2f}

EXPENSE BREAKDOWN:
"""
        
        # Expense breakdown by category
        expense_categories = {}
        for record in self.data["expenses"]:
            if record["date"].startswith(current_month):
                category = record["category"]
                if category in expense_categories:
                    expense_categories[category] += record["amount"]
                else:
                    expense_categories[category] = record["amount"]
        
        for category, amount in expense_categories.items():
            report += f"  {category}: {currency}{amount:.2f}\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, report)
    
    def generate_profit_analysis(self):
        """Generate profit analysis report"""
        currency = self.data["settings"]["currency"]
        
        total_income = sum(record["amount"] for record in self.data["income"])
        total_expenses = sum(record["amount"] for record in self.data["expenses"])
        total_sales = sum(record["total"] for record in self.data["sales"])
        net_profit = total_income - total_expenses
        
        # Calculate stock value
        stock_value = sum(record["total_value"] for record in self.data["stock"])
        
        report = f"""
PROFIT ANALYSIS REPORT
{'='*50}

OVERALL FINANCIAL POSITION:
Total Income: {currency}{total_income:.2f}
Total Expenses: {currency}{total_expenses:.2f}
Total Sales Revenue: {currency}{total_sales:.2f}
Net Profit: {currency}{net_profit:.2f}

ASSET VALUATION:
Current Stock Value: {currency}{stock_value:.2f}

PERFORMANCE METRICS:
Profit Margin: {((net_profit / total_income) * 100) if total_income > 0 else 0:.1f}%
Expense Ratio: {((total_expenses / total_income) * 100) if total_income > 0 else 0:.1f}%

TOP PERFORMING PRODUCTS:
"""
        
        # Product performance analysis
        product_sales = {}
        for record in self.data["sales"]:
            product = record["product"]
            if product in product_sales:
                product_sales[product] += record["total"]
            else:
                product_sales[product] = record["total"]
        
        # Sort by revenue
        sorted_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)
        for product, revenue in sorted_products[:5]:  # Top 5 products
            report += f"  {product}: {currency}{revenue:.2f}\n"
        
        if not sorted_products:
            report += "  No sales data available\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, report)
    
    def generate_stock_report(self):
        """Generate stock valuation report"""
        currency = self.data["settings"]["currency"]
        
        total_stock_value = sum(record["total_value"] for record in self.data["stock"])
        total_items = len(self.data["stock"])
        
        report = f"""
STOCK VALUATION REPORT
{'='*50}

STOCK SUMMARY:
Total Stock Items: {total_items}
Total Stock Value: {currency}{total_stock_value:.2f}
Average Item Value: {currency}{(total_stock_value / total_items) if total_items > 0 else 0:.2f}

DETAILED STOCK BREAKDOWN:
"""
        
        # Sort stock by value
        sorted_stock = sorted(self.data["stock"], key=lambda x: x["total_value"], reverse=True)
        
        for record in sorted_stock:
            report += f"""
Product: {record['product']}
  Quantity: {record['quantity']}
  Unit Cost: {currency}{record['unit_cost']:.2f}
  Total Value: {currency}{record['total_value']:.2f}
  Supplier: {record['supplier']}
"""
        
        if not sorted_stock:
            report += "No stock records available\n"
        
        # Low stock alerts (items with quantity < 10)
        low_stock = [item for item in self.data["stock"] if item["quantity"] < 10]
        if low_stock:
            report += f"\nLOW STOCK ALERTS:\n"
            for item in low_stock:
                report += f"  {item['product']}: {item['quantity']} units remaining\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, report)
    
    def export_to_csv(self):
        """Export all data to CSV files"""
        try:
            # Create exports directory if it doesn't exist
            export_dir = "exports"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Export income data
            if self.data["income"]:
                with open(f"{export_dir}/income_{timestamp}.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "Source", "Amount", "Description"])
                    for record in self.data["income"]:
                        writer.writerow([record["date"], record["source"], 
                                       record["amount"], record["description"]])
            
            # Export expenses data
            if self.data["expenses"]:
                with open(f"{export_dir}/expenses_{timestamp}.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "Category", "Amount", "Description"])
                    for record in self.data["expenses"]:
                        writer.writerow([record["date"], record["category"], 
                                       record["amount"], record["description"]])
            
            # Export sales data
            if self.data["sales"]:
                with open(f"{export_dir}/sales_{timestamp}.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Date", "Product", "Quantity", "Unit Price", "Total", "Customer"])
                    for record in self.data["sales"]:
                        writer.writerow([record["date"], record["product"], record["quantity"],
                                       record["unit_price"], record["total"], record["customer"]])
            
            # Export stock data
            if self.data["stock"]:
                with open(f"{export_dir}/stock_{timestamp}.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Product", "Quantity", "Unit Cost", "Total Value", "Supplier"])
                    for record in self.data["stock"]:
                        writer.writerow([record["product"], record["quantity"], record["unit_cost"],
                                       record["total_value"], record["supplier"]])
            
            messagebox.showinfo("Success", f"Data exported successfully to {export_dir}/ folder!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = BusinessTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
