import customtkinter as ctk
import requests
import json
import webbrowser
import pyperclip
from datetime import datetime, timezone
import threading
from PIL import Image
from io import BytesIO
import os
import time

class RemzWareRobloxChecker:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry("1200x800")
        self.window.title("RemzWare Roblox Cookie Checker")
        self.window.configure(fg_color="#1a1a1a")
        self.window.iconbitmap("icon.ico") if os.path.exists("icon.ico") else None
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Create main container with scrollbar
        self.main_container = ctk.CTkScrollableFrame(
            self.window,
            width=1160,
            height=780,
            fg_color="#1a1a1a"
        )
        self.main_container.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Initialize variables
        self.checking = False
        self.typing_animation = None
        self.current_cookie = None
        
        self.create_gui()
        
    def create_gui(self):
        # Center container
        center_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        center_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Title Frame with Logo
        title_frame = ctk.CTkFrame(center_container, fg_color="#2d2d2d", corner_radius=15)
        title_frame.pack(pady=10, fill="x")
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="RemzWare Roblox Cookie Checker",
            font=("Helvetica", 32, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=15)
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Check Roblox Account Information Tool",
            font=("Helvetica", 14),
            text_color="#808080"
        )
        subtitle.pack(pady=(0, 15))
        
        # Content Frame with improved grid layout
        content_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        content_frame.pack(pady=20, fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=2)  # Left panel takes 2 parts
        content_frame.grid_columnconfigure(1, weight=3)  # Right panel takes 3 parts
        
        # Left Panel (Input and Controls)
        left_panel = ctk.CTkFrame(content_frame, fg_color="#2d2d2d", corner_radius=15)
        left_panel.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        left_panel.grid_columnconfigure(0, weight=1)  # Make contents expand horizontally
        
        # Cookie Input Section with better spacing
        input_section = ctk.CTkFrame(left_panel, fg_color="#232323", corner_radius=10)
        input_section.pack(pady=15, padx=15, fill="x")
        input_section.grid_columnconfigure(0, weight=1)
        
        input_header = ctk.CTkFrame(input_section, fg_color="transparent")
        input_header.pack(fill="x", padx=15, pady=(15,5))
        input_header.grid_columnconfigure(0, weight=1)
        
        input_label = ctk.CTkLabel(
            input_header,
            text="Enter Roblox Cookie",
            font=("Helvetica", 16, "bold"),
            text_color="#e0e0e0"
        )
        input_label.pack(side="left")
        
        self.cookie_input = ctk.CTkTextbox(
            input_section,
            width=400,
            height=100,
            font=("Consolas", 12),
            fg_color="#1a1a1a",
            text_color="#00ff00",
            border_color="#3d3d3d",
            border_width=2
        )
        self.cookie_input.pack(pady=10, padx=15, fill="x")
        
        # Status Label with better visibility
        self.status_label = ctk.CTkLabel(
            input_section,
            text="",
            font=("Consolas", 12),
            text_color="#00ff00"
        )
        self.status_label.pack(pady=(0, 15), padx=15, fill="x")
        
        # Buttons Section with improved layout
        buttons_section = ctk.CTkFrame(left_panel, fg_color="#232323", corner_radius=10)
        buttons_section.pack(pady=15, padx=15, fill="x")
        buttons_section.grid_columnconfigure(0, weight=1)
        
        # Main buttons with better spacing
        main_buttons = ctk.CTkFrame(buttons_section, fg_color="transparent")
        main_buttons.pack(pady=10, padx=15, fill="x")
        main_buttons.grid_columnconfigure(0, weight=1)
        
        self.check_button = ctk.CTkButton(
            main_buttons,
            text="Check Cookie",
            command=self.check_cookie,
            font=("Helvetica", 14, "bold"),
            fg_color="#404040",
            hover_color="#4a4a4a",
            height=40,
            corner_radius=8
        )
        self.check_button.pack(pady=(5,5), fill="x")
        
        self.refresh_button = ctk.CTkButton(
            main_buttons,
            text="Refresh Cookie",
            command=self.refresh_cookie,
            font=("Helvetica", 14, "bold"),
            fg_color="#2d5a27",
            hover_color="#366b2f",
            height=40,
            corner_radius=8,
            state="disabled"
        )
        self.refresh_button.pack(pady=(5,10), fill="x")
        
        # Utility buttons with equal spacing
        button_frame = ctk.CTkFrame(buttons_section, fg_color="transparent")
        button_frame.pack(pady=(0,10), padx=15, fill="x")
        button_frame.grid_columnconfigure((0,1), weight=1)
        
        clear_button = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self.clear_input,
            font=("Helvetica", 14),
            fg_color="#333333",
            hover_color="#3d3d3d",
            height=35,
            corner_radius=8
        )
        clear_button.grid(row=0, column=0, padx=5, sticky="ew")
        
        copy_button = ctk.CTkButton(
            button_frame,
            text="Copy Cookie",
            command=self.copy_cookie,
            font=("Helvetica", 14),
            fg_color="#333333",
            hover_color="#3d3d3d",
            height=35,
            corner_radius=8
        )
        copy_button.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Right Panel with improved layout
        right_panel = ctk.CTkFrame(content_frame, fg_color="#2d2d2d", corner_radius=15)
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_columnconfigure(0, weight=1)
        
        # User Info Section with better alignment
        self.user_info_frame = ctk.CTkFrame(right_panel, fg_color="#232323", corner_radius=10)
        self.user_info_frame.pack(pady=15, padx=15, fill="x")
        self.user_info_frame.grid_columnconfigure(1, weight=1)
        
        # Avatar Frame with fixed size
        self.avatar_frame = ctk.CTkFrame(self.user_info_frame, fg_color="#1a1a1a", corner_radius=10, width=150, height=150)
        self.avatar_frame.grid(row=0, column=0, padx=15, pady=15)
        self.avatar_frame.grid_propagate(False)
        
        self.avatar_label = ctk.CTkLabel(
            self.avatar_frame,
            text="Waiting for Cookie...",
            font=("Helvetica", 12),
            text_color="#808080"
        )
        self.avatar_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # User Details Frame with better spacing
        self.user_details = ctk.CTkFrame(self.user_info_frame, fg_color="transparent")
        self.user_details.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        self.user_details.grid_columnconfigure(0, weight=1)
        
        # Create user info labels
        self.username_label = ctk.CTkLabel(
            self.user_details,
            text="Username",
            font=("Helvetica", 28, "bold"),
            text_color="#333333"
        )
        self.username_label.pack(anchor="w", pady=(5,0))
        
        self.display_name_label = ctk.CTkLabel(
            self.user_details,
            text="@displayname",
            font=("Helvetica", 18),
            text_color="#404040"
        )
        self.display_name_label.pack(anchor="w", pady=(0,5))

        # Create divider
        divider = ctk.CTkFrame(self.user_details, fg_color="#2d2d2d", height=2)
        divider.pack(fill="x", pady=10)

        # Additional user info section
        self.user_info_grid = ctk.CTkFrame(self.user_details, fg_color="transparent")
        self.user_info_grid.pack(fill="x", pady=(5,0))
        self.user_info_grid.grid_columnconfigure((0,1), weight=1)

        # Create additional info labels with better organization
        self.create_info_label("Account Created", "---", 0, 0)
        self.create_info_label("Last Online", "---", 0, 1)
        self.create_info_label("Account Type", "---", 1, 0)
        self.create_info_label("Account PIN", "---", 1, 1)

        # Stats Frame with improved grid layout
        self.stats_frame = ctk.CTkFrame(right_panel, fg_color="#232323", corner_radius=10)
        self.stats_frame.pack(pady=15, padx=15, fill="x")
        self.stats_frame.grid_columnconfigure((0,1,2), weight=1)

        # Initialize placeholder stats
        self.create_placeholder_stats()
        
        # Terminal Frame with better organization
        terminal_frame = ctk.CTkFrame(right_panel, fg_color="#232323", corner_radius=10)
        terminal_frame.pack(pady=15, padx=15, fill="both", expand=True)
        terminal_frame.grid_columnconfigure(0, weight=1)
        
        # Terminal Header with better spacing
        terminal_header = ctk.CTkFrame(terminal_frame, fg_color="#1a1a1a", corner_radius=8)
        terminal_header.pack(pady=(10,0), padx=10, fill="x")
        terminal_header.grid_columnconfigure(0, weight=1)
        
        terminal_title = ctk.CTkLabel(
            terminal_header,
            text="Terminal Output",
            font=("Helvetica", 16, "bold"),
            text_color="#e0e0e0"
        )
        terminal_title.pack(side="left", pady=10, padx=10)
        
        terminal_buttons = ctk.CTkFrame(terminal_header, fg_color="transparent")
        terminal_buttons.pack(side="right", pady=5, padx=5)
        
        copy_terminal = ctk.CTkButton(
            terminal_buttons,
            text="Copy Output",
            command=self.copy_terminal,
            font=("Helvetica", 12),
            fg_color="#333333",
            hover_color="#3d3d3d",
            width=100,
            height=30,
            corner_radius=6
        )
        copy_terminal.pack(side="right", padx=5)
        
        clear_terminal = ctk.CTkButton(
            terminal_buttons,
            text="Clear",
            command=self.clear_terminal,
            font=("Helvetica", 12),
            fg_color="#333333",
            hover_color="#3d3d3d",
            width=80,
            height=30,
            corner_radius=6
        )
        clear_terminal.pack(side="right", padx=5)
        
        # Terminal display with improved visibility
        self.results_display = ctk.CTkTextbox(
            terminal_frame,
            font=("Consolas", 12),
            fg_color="#1a1a1a",
            text_color="#00ff00",
            border_color="#3d3d3d",
            border_width=2
        )
        self.results_display.pack(pady=10, padx=10, fill="both", expand=True)
        self.results_display.configure(state="disabled")
        
        # Social Links Frame with better spacing
        social_frame = ctk.CTkFrame(center_container, fg_color="#2d2d2d", corner_radius=15)
        social_frame.pack(pady=20, fill="x")
        social_frame.grid_columnconfigure(0, weight=1)
        
        social_label = ctk.CTkLabel(
            social_frame,
            text="Join Our Community",
            font=("Helvetica", 16, "bold"),
            text_color="#e0e0e0"
        )
        social_label.pack(pady=10)
        
        social_buttons = ctk.CTkFrame(social_frame, fg_color="transparent")
        social_buttons.pack(pady=(0, 15))
        social_buttons.grid_columnconfigure((0,1), weight=1)
        
        discord_button = ctk.CTkButton(
            social_buttons,
            text="Join Discord",
            command=lambda: webbrowser.open("https://discord.gg/fS4YtgK6Be"),
            font=("Helvetica", 14),
            fg_color="#5865F2",
            hover_color="#4752C4",
            width=180,
            height=35,
            corner_radius=8
        )
        discord_button.pack(side="left", padx=10)
        
        github_button = ctk.CTkButton(
            social_buttons,
            text="GitHub",
            command=lambda: webbrowser.open("https://github.com/remzpy/Roblox-Cookie-Checker"),
            font=("Helvetica", 14),
            fg_color="#333333",
            hover_color="#2b2b2b",
            width=180,
            height=35,
            corner_radius=8
        )
        github_button.pack(side="left", padx=10)
        
    def animate_status(self, text, index=0):
        if self.typing_animation:
            self.window.after_cancel(self.typing_animation)
            self.typing_animation = None
            
        if index <= len(text):
            self.status_label.configure(text=text[:index] + "█")
            self.typing_animation = self.window.after(50, lambda: self.animate_status(text, index + 1))
        else:
            self.status_label.configure(text=text)
            self.typing_animation = self.window.after(500, lambda: self.animate_cursor(text))
            
    def animate_cursor(self, text, show_cursor=True):
        if not self.checking:
            self.status_label.configure(text="")
            return
            
        self.status_label.configure(text=text + ("█" if show_cursor else ""))
        self.typing_animation = self.window.after(500, lambda: self.animate_cursor(text, not show_cursor))
        
    def refresh_cookie(self):
        if not self.current_cookie or self.checking:
            return
            
        self.checking = True
        self.check_button.configure(state="disabled")
        self.refresh_button.configure(state="disabled")
        self.animate_status("Refreshing cookie...")
        threading.Thread(target=self._refresh_cookie_thread).start()
        
    def _refresh_cookie_thread(self):
        try:
            if not self.current_cookie:
                self.update_results("❌ No valid cookie to refresh!")
                self.animate_status("No cookie to refresh!")
                return

            self.update_results("Starting cookie refresh process...")
            
            # Step 1: Initial headers setup
            headers = {
                'Cookie': f'.ROBLOSECURITY={self.current_cookie}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.roblox.com/',
                'Origin': 'https://www.roblox.com',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Step 2: Get CSRF token
            self.animate_status("Getting CSRF token...")
            csrf_request = requests.post('https://auth.roblox.com/v2/logout', headers=headers)
            if 'x-csrf-token' not in csrf_request.headers:
                raise Exception("Failed to get CSRF token")
                
            csrf_token = csrf_request.headers['x-csrf-token']
            headers['x-csrf-token'] = csrf_token
            self.update_results("✓ CSRF token obtained")
            
            # Step 3: Get authentication ticket
            self.animate_status("Getting authentication ticket...")
            ticket_headers = headers.copy()
            ticket_headers['Referer'] = 'https://www.roblox.com/home'
            ticket_headers['rbxauthenticationnegotiation'] = '1'
            
            ticket_request = requests.post(
                'https://auth.roblox.com/v1/authentication-ticket',
                headers=ticket_headers,
                json={"returnUrl": "https://www.roblox.com/home"}
            )
            
            if ticket_request.status_code != 200:
                raise Exception(f"Failed to get authentication ticket: {ticket_request.status_code}")
                
            auth_ticket = ticket_request.headers.get('rbx-authentication-ticket')
            if not auth_ticket:
                raise Exception("No authentication ticket in response")
                
            self.update_results("✓ Authentication ticket obtained")
            
            # Step 4: Refresh using authentication ticket
            self.animate_status("Refreshing cookie...")
            refresh_headers = {
                'User-Agent': headers['User-Agent'],
                'RBXAuthenticationNegotiation': '1',
                'Referer': 'https://www.roblox.com/',
                'Origin': 'https://www.roblox.com'
            }
            
            refresh_url = 'https://www.roblox.com/authentication/signoutfromallsessionsandreauthenticate'
            refresh = requests.get(
                f"{refresh_url}?returnUrl=https://www.roblox.com/home",
                headers=refresh_headers,
                cookies={'.ROBLOSECURITY': self.current_cookie},
                allow_redirects=True
            )
            
            new_cookie = None
            for resp in refresh.history:
                for cookie in resp.cookies:
                    if cookie.name == '.ROBLOSECURITY':
                        new_cookie = cookie.value
                        break
                if new_cookie:
                    break
                    
            if not new_cookie:
                # Try alternative method
                self.animate_status("Trying alternative refresh method...")
                refresh2 = requests.post(
                    'https://auth.roblox.com/v2/reauth',
                    headers={**headers, 'rbxauthenticationnegotiation': '1'},
                    json={"ticket": auth_ticket},
                    allow_redirects=True
                )
                
                for resp in refresh2.history:
                    for cookie in resp.cookies:
                        if cookie.name == '.ROBLOSECURITY':
                            new_cookie = cookie.value
                            break
                    if new_cookie:
                        break
                    
            if not new_cookie:
                raise Exception("No new cookie received")
                
            # Step 5: Validate new cookie
            self.animate_status("Validating new cookie...")
            validate_headers = {
                'Cookie': f'.ROBLOSECURITY={new_cookie}',
                'User-Agent': headers['User-Agent']
            }
            
            validation = requests.get('https://users.roblox.com/v1/users/authenticated', headers=validate_headers)
            if validation.status_code != 200:
                raise Exception("New cookie validation failed")
                
            # Success - update cookie
            self.current_cookie = new_cookie
            self.cookie_input.delete("1.0", "end")
            self.cookie_input.insert("1.0", new_cookie)
            self.update_results("✅ Cookie refreshed successfully!")
            self.animate_status("Cookie refreshed!")
            
            # Update user information with new cookie
            self._check_cookie_thread(new_cookie)
            
        except Exception as e:
            self.update_results(f"❌ Error refreshing cookie: {str(e)}")
            self.animate_status("Refresh failed!")
        finally:
            self.checking = False
            self.check_button.configure(state="normal")
            self.refresh_button.configure(state="normal")
            
    def create_placeholder_labels(self):
        self.placeholder_name = ctk.CTkLabel(
            self.user_details,
            text="Username",
            font=("Helvetica", 28, "bold"),
            text_color="#333333"
        )
        self.placeholder_name.pack(anchor="w")
        
        self.placeholder_display = ctk.CTkLabel(
            self.user_details,
            text="@displayname",
            font=("Helvetica", 18),
            text_color="#404040"
        )
        self.placeholder_display.pack(anchor="w")
        
    def create_placeholder_stats(self):
        placeholder_stats = [
            ("Premium Status", "---"),
            ("Account Age", "---"),
            ("Total RAP", "---"),
            ("Limited Items", "---"),
            ("Friends", "---"),
            ("Followers", "---"),
            ("Robux Balance", "---"),
            ("Total Place Visits", "---"),
            ("Total Badges", "---")
        ]
        
        for i, (text, value) in enumerate(placeholder_stats):
            self.create_stat_label(text, value, i // 3, i % 3, is_placeholder=True)
            
    def clear_input(self):
        if self.checking:
            return
            
        self.cookie_input.delete("1.0", "end")
        self.status_label.configure(text="")
        self.current_cookie = None
        self.refresh_button.configure(state="disabled")
        
        # Reset user info
        self.username_label.configure(text="Username", text_color="#333333")
        self.display_name_label.configure(text="@displayname", text_color="#404040")
        
        # Reset additional info
        for widget in self.user_info_grid.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                value_label = widget.winfo_children()[1]
                value_label.configure(text="---", text_color="#404040")
        
        # Clear avatar
        self.avatar_label.configure(image=None, text="Waiting for Cookie...")
        
        # Clear terminal with timestamp
        self.results_display.configure(state="normal")
        self.results_display.delete("1.0", "end")
        self.update_results("Terminal cleared at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.update_results("-" * 50)
        self.results_display.configure(state="disabled")
        
        # Reset stats
        self.create_placeholder_stats()

    def copy_cookie(self):
        if self.checking:
            return
            
        cookie = self.cookie_input.get("1.0", "end-1c").strip()
        if cookie:
            pyperclip.copy(cookie)
            self.update_results("✅ Cookie copied to clipboard!")
            self.animate_status("Cookie copied!")
        else:
            self.update_results("❌ No cookie to copy!")
            self.animate_status("No cookie to copy!")
        
    def update_results(self, text):
        self.results_display.configure(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_display.insert("end", f"[{timestamp}] {text}\n")
        self.results_display.configure(state="disabled")
        self.results_display.see("end")
        
    def load_avatar(self, user_id):
        try:
            avatar_url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=420x420&format=Png"
            avatar_data = requests.get(avatar_url).json()
            avatar_image_url = avatar_data["data"][0]["imageUrl"]
            
            response = requests.get(avatar_image_url)
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize((150, 150), Image.Resampling.LANCZOS)
            img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(150, 150))
            
            self.avatar_label.configure(image=img, text="")
            self.avatar_label.image = img
        except Exception as e:
            self.update_results(f"Error loading avatar: {str(e)}")
            
    def create_stat_label(self, text, value, row, column, is_placeholder=False):
        if not hasattr(self, 'stat_frames'):
            self.stat_frames = {}
        
        frame_key = f"{row}_{column}"
        if frame_key in self.stat_frames:
            # Update existing frame
            frame = self.stat_frames[frame_key]
            label = frame.winfo_children()[0]
            value_label = frame.winfo_children()[1]
            
            label.configure(text=text, text_color="#808080" if not is_placeholder else "#333333")
            value_label.configure(text=str(value), text_color="#ffffff" if not is_placeholder else "#404040")
        else:
            # Create new frame with better spacing
            frame = ctk.CTkFrame(self.stats_frame, fg_color="#1a1a1a", corner_radius=8)
            frame.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")
            frame.grid_columnconfigure(0, weight=1)
            
            label = ctk.CTkLabel(
                frame,
                text=text,
                font=("Helvetica", 12, "bold"),
                text_color="#808080" if not is_placeholder else "#333333"
            )
            label.pack(pady=(12, 0))
            
            value_label = ctk.CTkLabel(
                frame,
                text=str(value),
                font=("Helvetica", 16, "bold"),
                text_color="#ffffff" if not is_placeholder else "#404040"
            )
            value_label.pack(pady=(0, 12))
            
            self.stat_frames[frame_key] = frame
        
    def check_cookie(self):
        if self.checking:
            return
            
        cookie = self.cookie_input.get("1.0", "end-1c").strip()
        if not cookie:
            self.update_results("Please enter a cookie to check!")
            self.animate_status("No cookie entered!")
            return
            
        self.checking = True
        self.check_button.configure(state="disabled")
        self.refresh_button.configure(state="disabled")
        self.clear_input()
        self.animate_status("Checking cookie...")
        threading.Thread(target=self._check_cookie_thread, args=(cookie,)).start()
            
    def _check_cookie_thread(self, cookie):
        try:
            headers = {
                'Cookie': f'.ROBLOSECURITY={cookie}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            # Validate cookie
            r = requests.get('https://users.roblox.com/v1/users/authenticated', headers=headers)
            
            if r.status_code == 200:
                user_data = r.json()
                self.current_cookie = cookie
                self.update_results("✅ Cookie is Valid!")
                self.animate_status("Cookie is valid!")
                self.refresh_button.configure(state="normal")
                
                # Store cookie in input
                self.cookie_input.delete("1.0", "end")
                self.cookie_input.insert("1.0", cookie)
                
                try:
                    # Load avatar
                    self.load_avatar(user_data['id'])
                    
                    # Update username and display name
                    self.username_label.configure(text=user_data['name'], text_color="white")
                    self.display_name_label.configure(text=f"@{user_data['displayName']}", text_color="#808080")
                    
                    # Get user info
                    user_info = requests.get(f"https://users.roblox.com/v1/users/{user_data['id']}", headers=headers)
                    if user_info.status_code == 200:
                        user_info_data = user_info.json()
                        created_date = datetime.fromisoformat(user_info_data['created'].replace('Z', '+00:00'))
                        account_age = (datetime.now(timezone.utc) - created_date).days
                        created_str = created_date.strftime("%Y-%m-%d")
                        
                        # Get premium status
                        premium_check = requests.get(
                            f"https://premiumfeatures.roblox.com/v1/users/{user_data['id']}/validate-membership",
                            headers=headers
                        )
                        is_premium = premium_check.status_code == 200
                        
                        # Get friends count
                        friends_data = requests.get(f"https://friends.roblox.com/v1/users/{user_data['id']}/friends/count", headers=headers)
                        friends_count = friends_data.json().get('count', 0) if friends_data.status_code == 200 else 0
                        
                        # Get followers count
                        followers_data = requests.get(f"https://friends.roblox.com/v1/users/{user_data['id']}/followers/count", headers=headers)
                        followers_count = followers_data.json().get('count', 0) if followers_data.status_code == 200 else 0
                        
                        # Get Robux balance
                        currency_data = requests.get("https://economy.roblox.com/v1/user/currency", headers=headers)
                        robux = currency_data.json().get('robux', 0) if currency_data.status_code == 200 else 0
                        
                        # Update additional info
                        for widget in self.user_info_grid.winfo_children():
                            if isinstance(widget, ctk.CTkFrame):
                                value_label = widget.winfo_children()[1]
                                info_index = list(self.user_info_grid.winfo_children()).index(widget)
                                
                                if info_index == 0:  # Account Created
                                    value_label.configure(text=created_str, text_color="#ffffff")
                                elif info_index == 1:  # Last Online
                                    value_label.configure(text="Now", text_color="#00ff00")
                                elif info_index == 2:  # Account Type
                                    value_label.configure(text="Premium" if is_premium else "Regular", text_color="#ffffff")
                                elif info_index == 3:  # Account PIN
                                    pin_check = requests.get("https://auth.roblox.com/v1/account/pin", headers=headers)
                                    has_pin = pin_check.json().get('isEnabled', False) if pin_check.status_code == 200 else False
                                    value_label.configure(text="Enabled" if has_pin else "Disabled", text_color="#00ff00" if has_pin else "#ff0000")
                
                    # Get inventory (RAP and limiteds)
                    inventory_url = f"https://inventory.roblox.com/v1/users/{user_data['id']}/assets/collectibles"
                    inventory = requests.get(inventory_url, headers=headers)
                    
                    total_rap = 0
                    total_limiteds = 0
                    
                    if inventory.status_code == 200:
                        items = inventory.json().get('data', [])
                        total_rap = sum(item.get('recentAveragePrice', 0) for item in items)
                        total_limiteds = len(items)
                    
                    # Get place visits
                    places_url = f"https://games.roblox.com/v2/users/{user_data['id']}/games?sortOrder=Asc&limit=50"
                    places_data = requests.get(places_url, headers=headers)
                    total_visits = sum(game.get('placeVisits', 0) for game in places_data.json().get('data', [])) if places_data.status_code == 200 else 0
                    
                    # Get badges count
                    badges_url = f"https://badges.roblox.com/v1/users/{user_data['id']}/badges?limit=10&sortOrder=Asc"
                    badges_data = requests.get(badges_url, headers=headers)
                    total_badges = badges_data.json().get('total', 0) if badges_data.status_code == 200 else 0
                    
                    # Update all stats at once
                    stats = [
                        ("Premium Status", "✅ Yes" if is_premium else "❌ No"),
                        ("Account Age", f"{account_age:,} days"),
                        ("Total RAP", f"R$ {total_rap:,}"),
                        ("Limited Items", f"{total_limiteds:,}"),
                        ("Friends", f"{friends_count:,}"),
                        ("Followers", f"{followers_count:,}"),
                        ("Robux Balance", f"R$ {robux:,}"),
                        ("Total Place Visits", f"{total_visits:,}"),
                        ("Total Badges", f"{total_badges:,}")
                    ]
                    
                    # Update stats safely
                    for i, (text, value) in enumerate(stats):
                        try:
                            self.create_stat_label(text, value, i // 3, i % 3)
                        except Exception as stat_error:
                            self.update_results(f"Warning: Could not update {text}: {str(stat_error)}")
                    
                except Exception as info_error:
                    self.update_results(f"Warning: Some information could not be retrieved: {str(info_error)}")
                
            else:
                self.update_results("❌ Invalid Cookie!")
                self.animate_status("Invalid cookie!")
                
        except Exception as e:
            self.update_results(f"Error occurred: {str(e)}")
            self.animate_status("Error occurred!")
        finally:
            self.checking = False
            self.check_button.configure(state="normal")
            
    def copy_terminal(self):
        terminal_text = self.results_display.get("1.0", "end-1c")
        if terminal_text:
            pyperclip.copy(terminal_text)
            self.animate_status("Terminal output copied!")
        else:
            self.animate_status("No output to copy!")

    def clear_terminal(self):
        self.results_display.configure(state="normal")
        self.results_display.delete("1.0", "end")
        self.results_display.configure(state="disabled")
        self.update_results("Terminal cleared at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.update_results("-" * 50)
        self.animate_status("Terminal cleared!")

    def create_info_label(self, text, value, row, column):
        frame = ctk.CTkFrame(self.user_info_grid, fg_color="#1a1a1a", corner_radius=8)
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        
        label = ctk.CTkLabel(
            frame,
            text=text,
            font=("Helvetica", 12),
            text_color="#808080"
        )
        label.pack(pady=(8,0))
        
        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Helvetica", 14, "bold"),
            text_color="#404040"
        )
        value_label.pack(pady=(0,8))
        
        return value_label

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = RemzWareRobloxChecker()
    app.run() 