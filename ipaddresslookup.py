import socket
import os
import json
import tkinter as tk
from tkinter import ttk
import webbrowser

def open_discord_link():
    webbrowser.open("https://discord.gg/MDMyPDsszU")

def get_ip_info(ip):
    try:
        response = os.popen(f"curl -s ipinfo.io/{ip}").read()
        data = json.loads(response)
        return (
            data.get('country', 'N/A'),
            data.get('timezone', 'N/A'),
            data.get('region', 'N/A'),
            data.get('loc', 'N/A').split(',')
        )
    except Exception as e:
        print(f"Error getting IP information: {e}")
        return 'N/A', 'N/A', 'N/A', ('N/A', 'N/A')

def is_valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def get_ip_addresses(hostname):
    try:
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        return [ip for ip in ip_addresses if is_valid_ip(ip)]
    except socket.gaierror as e:
        print(f"Error resolving hostname {hostname}: {e}")
        return []

def save_to_file(filename, data):
    with open(filename, 'a') as file:
        for item in data:
            file.write(f"{item}\n")


def process_hostname():
    hostname = entry_hostname.get()
    ip_addresses = get_ip_addresses(hostname)

    if ip_addresses:
        result_text.delete(1.0, tk.END)
        filename = "ip_info.txt"
        for ip in ip_addresses:
            country, timezone, region, loc = get_ip_info(ip)
            
            # Format the information for display
            result_info = f"IP: {ip}\nCountry: {country}\nTimezone: {timezone}\nRegion: {region}\nLoc: {loc}\n"
            
            # Display and save to file
            result_text.insert(tk.END, result_info + '\n')
            save_to_file(filename, [result_info])

        result_text.insert(tk.END, f"IP addresses saved to {filename}\n")
        result_text.tag_config("link", foreground="blue", underline=False)
        result_text.tag_bind("link", "<Button-1>", lambda e: open_discord_link())
        result_text.tag_bind("link", "<Enter>", lambda e: result_text.config(cursor="hand2"))
        result_text.tag_bind("link", "<Leave>", lambda e: result_text.config(cursor=""))
        result_text.insert(tk.END, "Visit our Discord server", "link")

        result_text.insert(tk.END, "\n\nBY:MGC\n\n")

    else:
        result_text.insert(tk.END, f"No valid IP addresses found for {hostname}\n")

root = tk.Tk()
root.title("IP ADDRESS INFO LOOKUP")

label_hostname = ttk.Label(root, text="Enter Ip Address:")
label_hostname.grid(row=0, column=0, padx=10, pady=10)

entry_hostname = ttk.Entry(root)
entry_hostname.grid(row=0, column=1, padx=10, pady=10)

button_process = ttk.Button(root, text="Look UP", command=process_hostname)
button_process.grid(row=1, column=0, columnspan=2, pady=10)

result_text = tk.Text(root, height=10, width=80)
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

result_text.tag_config("link", foreground="blue", underline=False)
result_text.tag_bind("link", "<Button-1>", lambda e: open_discord_link())
result_text.tag_bind("link", "<Enter>", lambda e: result_text.config(cursor="hand2"))
result_text.tag_bind("link", "<Leave>", lambda e: result_text.config(cursor=""))
result_text.insert(tk.END, "Visit our Discord server", "link")

result_text.insert(tk.END, "\n\nBY:MGC\n\n")

root.mainloop()

