import tkinter as tk

class ATM_GUI:
    def __init__(self, master):
        self.master = master
        master.title("ATM")

        # Welcome Label
        self.welcome_label = tk.Label(master, text="Bienvenido al cajero automático", font=("Arial", 14))
        self.welcome_label.pack()

        # Balance Label
        self.balance_label = tk.Label(master, text="Saldo disponible: $100.00", font=("Arial", 12))
        self.balance_label.pack()

        # Entry for amount
        self.amount_entry = tk.Entry(master, font=("Arial", 12))
        self.amount_entry.pack()

        # Withdraw button
        self.withdraw_button = tk.Button(master, text="Retirar", font=("Arial", 12), command=self.withdraw)
        self.withdraw_button.pack()

        # Deposit button
        self.deposit_button = tk.Button(master, text="Depositar", font=("Arial", 12), command=self.deposit)
        self.deposit_button.pack()

    def withdraw(self):
        # Get amount from Entry
        amount = self.amount_entry.get()

        # Update balance label
        self.balance_label.config(text=f"Saldo disponible: $90.00")

    def deposit(self):
        # Get amount from Entry
        amount = self.amount_entry.get()

        # Update balance label
        self.balance_label.config(text=f"Saldo disponible: $110.00")

root = tk.Tk()
atm_gui = ATM_GUI(root)
root.mainloop()
import tkinter as tk

class ATM_GUI:
    def __init__(self, master):
        self.master = master
        master.title("ATM")

        # Welcome Label
        self.welcome_label = tk.Label(master, text="Bienvenido al cajero automático", font=("Arial", 14))
        self.welcome_label.pack()

        # Balance Label
        self.balance_label = tk.Label(master, text="Saldo disponible: $100.00", font=("Arial", 12))
        self.balance_label.pack()

        # Entry for amount
        self.amount_entry = tk.Entry(master, font=("Arial", 12))
        self.amount_entry.pack()

        # Withdraw button
        self.withdraw_button = tk.Button(master, text="Retirar", font=("Arial", 12), command=self.withdraw)
        self.withdraw_button.pack()

        # Deposit button
        self.deposit_button = tk.Button(master, text="Depositar", font=("Arial", 12), command=self.deposit)
        self.deposit_button.pack()

    def withdraw(self):
        # Get amount from Entry
        amount = self.amount_entry.get()

        # Update balance label
        self.balance_label.config(text=f"Saldo disponible: $90.00")

    def deposit(self):
        # Get amount from Entry
        amount = self.amount_entry.get()

        # Update balance label
        self.balance_label.config(text=f"Saldo disponible: $110.00")

root = tk.Tk()
atm_gui = ATM_GUI(root)
root.mainloop()
