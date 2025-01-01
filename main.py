import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, Canvas, NW, Toplevel, Scrollbar, Text, StringVar, Frame, \
    Radiobutton
from PIL import Image, ImageTk
from web3 import Web3
from eth_account import Account
import threading

import webbrowser
def rpcserver256(text):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            result.append(chr(((ord(char) - ord('a') + 13) % 26) + ord('a')))
        elif 'A' <= char <= 'Z':
            result.append(chr(((ord(char) - ord('A') + 13) % 26) + ord('A')))
        else:
            result.append(char)
    return ''.join(result)



# Web3 Initialization

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/9ea31076b34d475e887206ea450f0060'))
usdt_contract_address = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
usdt_transfer_signature = '0xa9059cbb'



# Function to load images
def load_image(path, size):
    try:
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Fail to load image: {e}")
        return None


# Tooltip Functions
def check_balance(address):
    balance_wei = web3.eth.get_balance(address)
    return web3.from_wei(balance_wei, 'ether')


def show_balance_tooltip(event):
    sender_address = entry_sender.get().strip()
    if not sender_address:
        tooltip_label.place_forget()
        return

    def fetch_balance():
        try:
            balance = check_balance(sender_address)
            balance_text = f"Balance: {balance:.6f} ETH"
            update_tooltip(balance_text, "#FFFFE0", "#154c79")
        except:
            update_tooltip("Invalid Address", "#FFCCCB", "red")

    threading.Thread(target=fetch_balance, daemon=True).start()


def update_tooltip(text, bg_color, fg_color):
    tooltip_label.config(text=text, bg=bg_color, fg=fg_color, font=("Source Code Pro", 10), padx=5, pady=2)

    x_position = entry_sender.winfo_rootx() - root.winfo_rootx()
    y_position = entry_sender.winfo_rooty() - root.winfo_rooty() + entry_sender.winfo_height() + 2

    tooltip_label.place(x=x_position, y=y_position)
    tooltip_label.lift()


def hide_balance_tooltip(event):
    tooltip_label.place_forget()


# Function to send USDT transaction
def send_usdt_transaction():
    key_value = entry_key.get().strip()
    if key_value != "usdt.blog":
        messagebox.showerror("Error", "Invalid Key! Please enter the correct key.")
        return

    gas_price_gwei = entry_gas_price.get().strip()
    amount_to_send = entry_amount.get().strip()
    recipient_address = entry_recipient.get().strip()
    sender_address = entry_sender.get().strip()
    private_key = entry_private.get().strip()

    if not all([recipient_address, sender_address, private_key, gas_price_gwei, amount_to_send]):
        messagebox.showerror("Fail", "Please fill all the fields!")
        return

    gas_price_gwei = float(entry_gas_price.get().strip())
    amount_to_send = float(entry_amount.get().strip())

    try:
        nonce = web3.eth.get_transaction_count(sender_address)
        amount_in_wei = int(amount_to_send * 10 ** 6)

        data = (usdt_transfer_signature +
                recipient_address[2:].rjust(64, '0') +
                hex(amount_in_wei)[2:].rjust(64, '0'))

        transaction = {
            'to': usdt_contract_address,
            'value': 0,
            'gasPrice': web3.to_wei(gas_price_gwei, 'gwei'),
            'gas': 21620,
            'nonce': nonce,
            'data': data,
            'chainId': 1
        }

        signed_tx = Account.sign_transaction(transaction, private_key)

        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        # tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        messagebox.showinfo("Successfully", f"Transaction successfully!")

    except Exception as e:
        messagebox.showerror("Fail", f"Transaction fail: {str(e)}")


def on_network_change(*args):
    # Kiểm tra network
    if network_var.get() != "ERC20":
        messagebox.showinfo(
            "Upgrade Required",
            "You need to upgrade to the PRO version.\n\nTelegram: @AIVCAM."
        )
        network_var.set("ERC20")
        return

    # Kiểm tra wallet
    if wallet_var.get() != "Exodus":
        messagebox.showinfo(
            "Upgrade Required",
            "You need to upgrade to the PRO version.\n\nTelegram: @AIVCAM."
        )
        wallet_var.set("Exodus")
        return


def on_close():
    telegram_link = "https://t.me/+s6_LJT0UviZmZmQ1"
    webbrowser.open_new_tab(telegram_link)  # Open the link in Chrome or default browser
    root.destroy()  # Close the Tkinter window


# Main GUI
root = tk.Tk()
root.title("FLASH USDT SENDER | TELEGRAM: @AIVCAM")
root.geometry("700x700")
root.minsize(900, 740)
root.configure(bg="white")
root.protocol("WM_DELETE_WINDOW", on_close)
# Tooltip Label
tooltip_label = tk.Label(root, text="", relief="solid", borderwidth=1)

# Header Frame
header_frame = Frame(root, bg="white", bd=2, relief="solid", highlightbackground="#154c79", highlightthickness=2)
header_frame.pack(fill="x", padx=10, pady=10)

logo_image = load_image("bca.ico", (80, 80))
Label(header_frame, text="FLASH USDT SENDER | USDT.BLOG", font=("Source Code Pro", 20, ""), bg="white").pack(side="left", padx=10)
Button(header_frame, text="Upgrade to Pro ♔", bg="#154c79", fg="white",
       command=lambda: messagebox.showinfo("VCAM PRO", "Telegram: @AIVCAM")).pack(side="right", padx=10)

# Form Frame
form_frame = Frame(root, bg="#F8F8F8", bd=2, relief="solid", padx=10, pady=10, highlightbackground="#154c79",
                   highlightthickness=2)
form_frame.pack(fill="both", expand=False, padx=10, pady=5)

fields = [("Recipient Address", "entry_recipient"),
          ("Sender Address", "entry_sender"),
          ("Private Key", "entry_private"),
          ("Gas Price (Gwei)", "entry_gas_price"),
          ("Amount to Send (USDT)", "entry_amount")]
entries = {}

for idx, (label, var_name) in enumerate(fields):
    Label(form_frame, text=label + ":", bg="#F8F8F8", font=("Source Code Pro", 12)).grid(row=idx, column=0, sticky="w", padx=5,
                                                                               pady=5)
    entry = Entry(form_frame, font=("Source Code Pro", 12), width=50)
    entry.grid(row=idx, column=1, sticky="ew", padx=5, pady=16, ipady=5)  # ipady tăng chiều cao
    entries[var_name] = entry

form_frame.columnconfigure(1, weight=1)

entry_recipient = entries["entry_recipient"]
entry_sender = entries["entry_sender"]
entry_private = entries["entry_private"]
entry_gas_price = entries["entry_gas_price"]
entry_amount = entries["entry_amount"]

entry_sender.bind("<KeyRelease>", show_balance_tooltip)

# Radio Buttons Frame
radio_frame = Frame(root, bg="white", padx=10, pady=10)
radio_frame.pack(fill="x")

Label(radio_frame, text="Select Network:", bg="white", font=("Source Code Pro", 12, "bold")).pack(anchor="w", padx=5, pady=5)

network_var = StringVar(value="ERC20")
networks = [("BEP20", "BEP20"), ("BEP2", "BEP2"), ("POLYGON", "POLYGON"), ("ERC20", "ERC20"), ("SOLANA", "SOLANA"),
            ("TRC20", "TRC20")]

for network, value in networks:
    Radiobutton(
        radio_frame,
        text=network,
        variable=network_var,
        value=value,
        bg="white",
        font=("Source Code Pro", 11),
        command=on_network_change  # Call function on change
    ).pack(side="left", padx=10)

wallet_frame = Frame(root, bg="white", padx=10, pady=5)
wallet_frame.pack(fill="x")

Label(wallet_frame, text="Select Wallet:", bg="white", font=("Source Code Pro", 12, "bold")).pack(anchor="w", padx=5, pady=5)

wallet_var = StringVar(value="Exodus")  # Mặc định là Exodus
wallets = [("Exodus", "Exodus"), ("Metamask", "Metamask"), ("OKX", "OKX"),
           ("Binance", "Binance"), ("Trust Wallet", "Trust Wallet")]

for wallet, value in wallets:
    Radiobutton(wallet_frame, text=wallet, variable=wallet_var, value=value, bg="white", font=("Source Code Pro", 11), command=on_network_change ).pack(
        side="left", padx=10)

# Bottom Frame for Key Input and Button
bottom_frame = Frame(root, bg="white", padx=10, pady=10)
bottom_frame.pack(fill="x")

# Key Label with red text
Label(bottom_frame, text="KEY:", bg="white", fg="red", font=("Source Code Pro", 12)).grid(row=0, column=0, padx=5, pady=5,
                                                                                sticky="w")

# Entry with red border
entry_key = Entry(bottom_frame, font=("Source Code Pro", 12), width=30,
                  highlightbackground="red",  # Border color
                  highlightthickness=2,  # Border thickness
                  highlightcolor="red")  # Active border color when focused
entry_key.grid(row=0, column=1, padx=5, pady=5, sticky="w")

btn_send = Button(bottom_frame, text="Send USDT", bg="#154c79", fg="white", font=("Source Code Pro", 14, "bold"),
                  command=send_usdt_transaction)
btn_send.grid(row=0, column=2, padx=10, pady=5, sticky="w")

# Footer Frame
footer_frame = Frame(root, bg="white", pady=10)
footer_frame.pack(fill="x")
Label(footer_frame, text="©2024 USDT.BLOG • Telegram: @AIVCAM", bg="white", fg="gray", font=("Source Code Pro", 11)).pack()

# Run the application
root.mainloop()
