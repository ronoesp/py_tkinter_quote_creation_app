# -*- coding: utf-8 -*-
"""
Estimation App Prototype (Draft)
- GUI Framework: CustomTkinter
- Database & ORM: Peewee & SQLite
- Pattern: Model-View-Controller (MVC) Structure

This sample demonstrates how to structure a Python desktop app using CustomTkinter
for a modern UI and Peewee for effortless database persistence.
"""

import os
from datetime import datetime
import customtkinter as ctk
from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField, DoubleField

# ==========================================
# 1. DATABASE & MODELS (Model Layer)
# ==========================================

# Initialize SQLite database (will be created in the current working directory)
DB_NAME = "estimation_app.db"
db = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db

class Estimate(BaseModel):
    """
    Estimate Model representing the estimation table in SQLite
    """
    client_name = CharField(max_length=100, verbose_name="宛先 / クライアント名")
    subject = CharField(max_length=200, verbose_name="件名")
    quantity = IntegerField(default=1, verbose_name="数量")
    unit_price = DoubleField(default=0.0, verbose_name="単価")
    created_at = DateTimeField(default=datetime.now, verbose_name="作成日時")

    @property
    def total_amount(self):
        """Business Logic: Calculate total before tax"""
        return self.quantity * self.unit_price

    @property
    def tax_amount(self):
        """Business Logic: 10% tax calculation (truncated)"""
        return int(self.total_amount * 0.10)

    @property
    def grand_total(self):
        """Business Logic: Total with tax"""
        return int(self.total_amount + self.tax_amount)


def init_db():
    """Create database tables if they do not exist"""
    db.connect()
    db.create_tables([Estimate])
    db.close()


# ==========================================
# 2. APPLICATION VIEW (View Layer)
# ==========================================

class AppView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Configure Window
        self.title("見積作成システム - Prototype")
        self.geometry("850x600")
        ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue") # Options: "blue", "green", "dark-blue"

        # Configure Grid layout (2 Columns: Left for Input, Right for History List)
        self.grid_columnconfigure(0, weight=1, minsize=380)
        self.grid_columnconfigure(1, weight=1, minsize=420)
        self.grid_rowconfigure(0, weight=1)

        # Build UI Components
        self.create_input_panel()
        self.create_history_panel()

    def create_input_panel(self):
        """Left Side: Input Form"""
        self.input_frame = ctk.CTkFrame(self, corner_radius=12)
        self.input_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # Title Label
        title_label = ctk.CTkLabel(
            self.input_frame, 
            text="見積情報の新規登録", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(padx=20, pady=(20, 15), anchor="w")

        # 1. Client Name Input
        self.client_label = ctk.CTkLabel(self.input_frame, text="宛先 (会社名・個人名):", font=ctk.CTkFont(size=12))
        self.client_label.pack(padx=20, pady=(5, 2), anchor="w")
        self.client_entry = ctk.CTkEntry(self.input_frame, placeholder_text="例: 株式会社サンプル")
        self.client_entry.pack(padx=20, pady=(0, 10), fill="x")

        # 2. Subject Input
        self.subject_label = ctk.CTkLabel(self.input_frame, text="見積件名:", font=ctk.CTkFont(size=12))
        self.subject_label.pack(padx=20, pady=(5, 2), anchor="w")
        self.subject_entry = ctk.CTkEntry(self.input_frame, placeholder_text="例: システム開発費用")
        self.subject_entry.pack(padx=20, pady=(0, 10), fill="x")

        # 3. Quantity Input
        self.qty_label = ctk.CTkLabel(self.input_frame, text="数量:", font=ctk.CTkFont(size=12))
        self.qty_label.pack(padx=20, pady=(5, 2), anchor="w")
        self.qty_entry = ctk.CTkEntry(self.input_frame, placeholder_text="例: 1")
        self.qty_entry.pack(padx=20, pady=(0, 10), fill="x")
        self.qty_entry.insert(0, "1")  # Default value

        # 4. Unit Price Input
        self.price_label = ctk.CTkLabel(self.input_frame, text="単価 (円):", font=ctk.CTkFont(size=12))
        self.price_label.pack(padx=20, pady=(5, 2), anchor="w")
        self.price_entry = ctk.CTkEntry(self.input_frame, placeholder_text="例: 150000")
        self.price_entry.pack(padx=20, pady=(0, 20), fill="x")

        # Live Calculation Display Frame
        self.calc_frame = ctk.CTkFrame(self.input_frame, fg_color="transparent", border_width=1, border_color="gray30", corner_radius=8)
        self.calc_frame.pack(padx=20, pady=10, fill="x")

        self.subtotal_label = ctk.CTkLabel(self.calc_frame, text="小計: ¥ 0", font=ctk.CTkFont(size=13))
        self.subtotal_label.pack(padx=15, pady=(8, 2), anchor="w")

        self.tax_label = ctk.CTkLabel(self.calc_frame, text="消費税 (10%): ¥ 0", font=ctk.CTkFont(size=13))
        self.tax_label.pack(padx=15, pady=2, anchor="w")

        self.grand_total_label = ctk.CTkLabel(self.calc_frame, text="合計金額 (税込): ¥ 0", font=ctk.CTkFont(size=15, weight="bold"), text_color="#1f538d")
        self.grand_total_label.pack(padx=15, pady=(2, 8), anchor="w")

        # Bind validation and calculation on key release
        self.qty_entry.bind("<KeyRelease>", self.on_input_changed)
        self.price_entry.bind("<KeyRelease>", self.on_input_changed)

        # Error Message Label (Hidden by default)
        self.error_label = ctk.CTkLabel(self.input_frame, text="", text_color="red", font=ctk.CTkFont(size=11))
        self.error_label.pack(padx=20, pady=5)

        # Action Button (Save)
        self.save_btn = ctk.CTkButton(
            self.input_frame, 
            text="見積書を保存する", 
            command=self.controller.save_estimate,
            font=ctk.CTkFont(weight="bold")
        )
        self.save_btn.pack(padx=20, pady=(10, 20), fill="x")

    def create_history_panel(self):
        """Right Side: Saved Estimates History"""
        self.history_frame = ctk.CTkFrame(self, corner_radius=12)
        self.history_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        title_label = ctk.CTkLabel(
            self.history_frame, 
            text="見積書 履歴一覧", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(padx=20, pady=(20, 15), anchor="w")

        # Scrollable Frame to list estimates
        self.scroll_frame = ctk.CTkScrollableFrame(self.history_frame, label_text="保存履歴 (最新順)")
        self.scroll_frame.pack(padx=15, pady=10, fill="both", expand=True)

    def on_input_changed(self, event=None):
        """Handler to update the live tax and subtotal indicators"""
        try:
            qty = int(self.qty_entry.get().strip() or 0)
            price = float(self.price_entry.get().strip() or 0.0)
            
            subtotal = qty * price
            tax = int(subtotal * 0.10)
            grand_total = int(subtotal + tax)

            self.subtotal_label.configure(text=f"小計: ¥ {subtotal:,.0f}")
            self.tax_label.configure(text=f"消費税 (10%): ¥ {tax:,.0f}")
            self.grand_total_label.configure(text=f"合計金額 (税込): ¥ {grand_total:,.0f}")
            self.error_label.configure(text="")
        except ValueError:
            self.error_label.configure(text="数量は整数、単価は数値を入力してください。")

    def get_form_data(self):
        """Gather current UI field inputs"""
        return {
            "client_name": self.client_entry.get().strip(),
            "subject": self.subject_entry.get().strip(),
            "quantity_str": self.qty_entry.get().strip(),
            "unit_price_str": self.price_entry.get().strip()
        }

    def clear_form(self):
        """Reset text inputs to initial state"""
        self.client_entry.delete(0, 'end')
        self.subject_entry.delete(0, 'end')
        self.qty_entry.delete(0, 'end')
        self.qty_entry.insert(0, "1")
        self.price_entry.delete(0, 'end')
        self.on_input_changed()

    def update_history_list(self, estimates):
        """Re-render the history widget list from databases"""
        # Clear current list widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not estimates:
            no_data_lbl = ctk.CTkLabel(self.scroll_frame, text="保存された履歴はありません。", font=ctk.CTkFont(slant="italic"))
            no_data_lbl.pack(pady=20)
            return

        for est in estimates:
            # Card Container for each estimate
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=6, border_width=1, border_color="gray25")
            card.pack(fill="x", padx=5, pady=5)

            # Left/Main metadata block
            text_block = f"宛先: {est.client_name}\n件名: {est.subject}\n金額: ¥ {est.grand_total:,.0f} (内税 ¥ {est.tax_amount:,.0f})"
            lbl = ctk.CTkLabel(card, text=text_block, justify="left", font=ctk.CTkFont(size=12))
            lbl.pack(side="left", padx=10, pady=8, fill="both", expand=True)

            # Date stamp on right side
            date_str = est.created_at.strftime("%Y/%m/%d %H:%M")
            date_lbl = ctk.CTkLabel(card, text=date_str, font=ctk.CTkFont(size=10, slant="italic"), text_color="gray60")
            date_lbl.pack(side="right", padx=10, pady=8)


# ==========================================
# 3. APP CONTROLLER (Controller Layer)
# ==========================================

class AppController:
    def __init__(self):
        # Initialize database schemas
        init_db()
        
        # Connect View and Controller
        self.view = AppView(self)
        
        # Fetch initial dataset
        self.refresh_history()

    def run(self):
        self.view.mainloop()

    def fetch_all_estimates(self):
        """Query database for all estimates ordered by newest"""
        db.connect(reuse_if_open=True)
        query = Estimate.select().order_by(Estimate.created_at.desc())
        results = list(query)
        db.close()
        return results

    def refresh_history(self):
        """Retrieve records and tell View to redraw them"""
        estimates = self.fetch_all_estimates()
        self.view.update_history_list(estimates)

    def save_estimate(self):
        """Validates inputs, commits to SQLite, and updates UI"""
        data = self.view.get_form_data()
        
        # Validation
        if not data["client_name"] or not data["subject"]:
            self.view.error_label.configure(text="エラー: 宛先と件名は必須項目です。")
            return

        try:
            qty = int(data["quantity_str"])
            price = float(data["unit_price_str"])
            if qty <= 0 or price < 0:
                raise ValueError("Positive values required")
        except ValueError:
            self.view.error_label.configure(text="エラー: 数量・単価に正しい数値を入力してください。")
            return

        # Commit to DB
        db.connect(reuse_if_open=True)
        new_est = Estimate.create(
            client_name=data["client_name"],
            subject=data["subject"],
            quantity=qty,
            unit_price=price,
            created_at=datetime.now()
        )
        db.close()

        # Update visual states
        self.view.clear_form()
        self.refresh_history()


# ==========================================
# 4. ENTRY POINT
# ==========================================

if __name__ == "__main__":
    controller = AppController()
    controller.run()
