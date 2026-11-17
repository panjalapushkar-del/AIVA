import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from google import genai
import datetime
import os
import threading
import time
import re



BG = "#0B1120"
SIDEBAR = "#111A2E"
CARD = "#17233B"
INPUT = "#1E2D48"
PURPLE = "#8066F6"
BLUE = "#3987F5"
WHITE = "#F1F5F9"
MUTED = "#94A3B8"
GREEN = "#22C55E"


class StudyBuddy:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "AIVA | AI Student Virtual Assistant"
        )

        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.reminders = []
        self.chat_history = []

        # Gemini API connection

        api_key = os.environ.get("GEMINI_API_KEY")

        self.client = None

        if api_key:
            self.client = genai.Client(api_key=api_key)

        self.create_layout()

        self.update_clock()
        self.check_reminders()

    def create_layout(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=230
        )

        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="✦ AIVA",
            font=("Segoe UI", 19, "bold"),
            fg=WHITE,
            bg=SIDEBAR
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="YOUR PERSONAL AI ASSISTANT",
            font=("Segoe UI", 8, "bold"),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(pady=(0, 40))

        self.nav_button(
            "⌂   Dashboard",
            self.show_dashboard
        )

        self.nav_button(
            "✉   Chat Assistant",
            self.show_chat
        )

        self.nav_button(
            "▤   Academic Help",
            self.academic_help
        )

        self.nav_button(
            "▦   Study Planner",
            self.study_planner
        )

        self.nav_button(
            "◷   Reminders",
            self.view_reminders
        )

        self.nav_button(
            "✕   Clear Chat",
            self.clear_chat
        )

        tk.Frame(
            self.sidebar,
            bg="#263550",
            height=1
        ).pack(fill="x", padx=20, pady=30)

        tk.Label(
            self.sidebar,
            text="AIP203 | AI LAB PROJECT",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=SIDEBAR
        ).pack(side="bottom", pady=25)

        # MAIN CONTENT

        self.content = tk.Frame(
            self.root,
            bg=BG
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )


        header = tk.Frame(
            self.content,
            bg=BG,
            height=75
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(20, 10)
        )

        self.page_title = tk.Label(
            header,
            text="Dashboard",
            font=("Segoe UI", 23, "bold"),
            fg=WHITE,
            bg=BG
        )

        self.page_title.pack(side="left")

        self.clock = tk.Label(
            header,
            text="",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=BG
        )

        self.clock.pack(side="right", pady=10)


        self.page = tk.Frame(
            self.content,
            bg=BG
        )

        self.page.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        self.show_dashboard()

    def nav_button(self, text, command):

        tk.Button(
            self.sidebar,
            text=text,
            command=command,
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=SIDEBAR,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            anchor="w",
            padx=25,
            pady=14,
            cursor="hand2"
        ).pack(
            fill="x",
            padx=12,
            pady=3
        )


    def clear_page(self):

        for widget in self.page.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_page()

        self.page_title.config(text="Dashboard")

        welcome = tk.Frame(
            self.page,
            bg=CARD,
            padx=25,
            pady=25
        )

        welcome.pack(fill="x", pady=(5, 25))

        tk.Label(
            welcome,
            text="Welcome back, Student! 👋",
            font=("Segoe UI", 23, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            welcome,
            text="Your personal space for smarter learning and better productivity.",
            font=("Segoe UI", 11),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w", pady=(10, 0))

        tk.Button(
            welcome,
            text="Start Chat  →",
            command=self.show_chat,
            bg=PURPLE,
            fg=WHITE,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        ).pack(anchor="w", pady=(20, 0))

        tk.Label(
            self.page,
            text="QUICK ACCESS",
            font=("Segoe UI", 12, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(anchor="w", pady=(0, 15))

        cards = tk.Frame(
            self.page,
            bg=BG
        )

        cards.pack(fill="x")

        self.feature_card(
            cards,
            "✉",
            "AI Chat Assistant",
            "Ask anything using Gemini AI",
            self.show_chat,
            PURPLE,
            0,
            0
        )

        self.feature_card(
            cards,
            "▦",
            "Study Planner",
            "Create study schedules",
            self.study_planner,
            BLUE,
            0,
            1
        )

        self.feature_card(
            cards,
            "◷",
            "Reminders",
            "Manage study reminders",
            self.view_reminders,
            GREEN,
            1,
            0
        )

        self.feature_card(
            cards,
            "▤",
            "Academic Help",
            "Explore academic topics",
            self.academic_help,
            "#E69A42",
            1,
            1
        )

        tk.Label(
            self.page,
            text="STAY FOCUSED. KEEP LEARNING. KEEP GROWING.",
            font=("Segoe UI", 10, "bold"),
            fg=MUTED,
            bg=BG
        ).pack(pady=30)


    def feature_card(
        self,
        parent,
        icon,
        title,
        description,
        command,
        color,
        row,
        col
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            padx=20,
            pady=20
        )

        card.grid(
            row=row,
            column=col,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        tk.Label(
            card,
            text=icon,
            font=("Segoe UI", 25, "bold"),
            fg=color,
            bg=CARD
        ).pack(anchor="w")

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 14, "bold"),
            fg=WHITE,
            bg=CARD
        ).pack(anchor="w", pady=(10, 5))

        tk.Label(
            card,
            text=description,
            font=("Segoe UI", 10),
            fg=MUTED,
            bg=CARD
        ).pack(anchor="w")

        tk.Button(
            card,
            text="Open →",
            command=command,
            bg=INPUT,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=12,
            pady=7
        ).pack(anchor="w", pady=(15, 0))


    def show_chat(self):

        self.clear_page()

        self.page_title.config(text="Chat Assistant")

        tk.Label(
            self.page,
            text="Your AI Learning Partner",
            font=("Segoe UI", 19, "bold"),
            fg=WHITE,
            bg=BG
        ).pack(anchor="w", pady=(5, 5))

        tk.Label(
            self.page,
            text="Powered by Google Gemini AI",
            font=("Segoe UI", 10),
            fg=GREEN,
            bg=BG
        ).pack(anchor="w", pady=(0, 15))

        self.chat_area = scrolledtext.ScrolledText(
            self.page,
            font=("Segoe UI", 11),
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            wrap="word",
            padx=15,
            pady=15,
            state="disabled"
        )

        self.chat_area.pack(
            fill="both",
            expand=True,
            pady=5
        )

        self.chat_area.tag_config(
            "user",
            foreground="#A78BFA",
            font=("Segoe UI", 11, "bold")
        )

        self.chat_area.tag_config(
            "assistant",
            foreground="#60A5FA",
            font=("Segoe UI", 11, "bold")
        )

        self.chat_area.tag_config(
            "message",
            foreground=WHITE,
            font=("Segoe UI", 11)
        )
        
        if self.chat_history:

            for sender, message in self.chat_history:

                self.add_message(sender, message)

        else:

            self.add_message(
                "AIVA",
                "Hello! I am your AI-powered AIVA. "
                "Ask me anything about your studies!"
            )

        input_frame = tk.Frame(
            self.page,
            bg=BG
        )

        input_frame.pack(
            fill="x",
            pady=15
        )

        self.user_input = tk.Entry(
            input_frame,
            font=("Segoe UI", 12),
            bg=INPUT,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )

        self.user_input.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=14,
            padx=(0, 10)
        )

        self.user_input.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        self.send_button = tk.Button(
            input_frame,
            text="SEND  ➤",
            command=self.send_message,
            bg=PURPLE,
            fg=WHITE,
            activebackground=BLUE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=22,
            pady=12,
            cursor="hand2"
        )

        self.send_button.pack(side="right")

        self.status_label = tk.Label(
            self.page,
            text="",
            font=("Segoe UI", 9),
            fg=GREEN,
            bg=BG
        )

        self.status_label.pack(anchor="w")

        self.user_input.focus_set()


    def add_message(self, sender, message):

        self.chat_area.config(state="normal")

        if sender == "You":

            self.chat_area.insert(
                tk.END,
                "\nYou\n",
                "user"
            )

        else:

            self.chat_area.insert(
                tk.END,
                "\n✦ AIVA\n",
                "assistant"
            )

        self.insert_markdown(message)
        self.chat_area.config(state="disabled")
        self.chat_area.see(tk.END)

    def insert_markdown(self, text):
        """Render common Markdown formatting inside the chat Text widget."""
        widget = self.chat_area
        widget.config(state="normal")

        widget.tag_config("heading1", foreground="#F8FAFC",
                          font=("Segoe UI", 16, "bold"), spacing1=10, spacing3=7)
        widget.tag_config("heading2", foreground="#C4B5FD",
                          font=("Segoe UI", 13, "bold"), spacing1=8, spacing3=5)
        widget.tag_config("bold", font=("Segoe UI", 11, "bold"))
        widget.tag_config("italic", font=("Segoe UI", 11, "italic"))
        widget.tag_config("inline_code", foreground="#F9A8D4",
                          background="#263650", font=("Consolas", 10))
        widget.tag_config("code", foreground="#D1FAE5",
                          background="#101827", font=("Consolas", 10),
                          lmargin1=14, lmargin2=14, spacing1=3, spacing3=3)
        widget.tag_config("bullet", foreground="#93C5FD",
                          font=("Segoe UI", 11, "bold"))
        widget.tag_config("quote", foreground="#CBD5E1",
                          lmargin1=14, lmargin2=14)
        widget.tag_config("separator", foreground="#64748B")

        def insert_inline(line, base_tag="message"):
            """Apply bold, italic and inline-code styles within one line."""
            pattern = re.compile(r"(\*\*.+?\*\*|`[^`]+`|\*[^*]+\*)")
            pos = 0
            for match in pattern.finditer(line):
                if match.start() > pos:
                    widget.insert(tk.END, line[pos:match.start()], base_tag)

                token = match.group(0)
                if token.startswith("**"):
                    widget.insert(tk.END, token[2:-2], ("bold",))
                elif token.startswith("`"):
                    widget.insert(tk.END, token[1:-1], ("inline_code",))
                else:
                    widget.insert(tk.END, token[1:-1], ("italic",))
                pos = match.end()

            if pos < len(line):
                widget.insert(tk.END, line[pos:], base_tag)

        in_code = False
        code_lines = []

        for raw_line in text.splitlines():
            line = raw_line.rstrip()

            if line.strip().startswith("```"):
                if not in_code:
                    in_code = True
                    code_lines = []
                else:
                    widget.insert(tk.END, "\n".join(code_lines) + "\n", "code")
                    in_code = False
                continue

            if in_code:
                code_lines.append(line)
                continue

            stripped = line.strip()

            if not stripped:
                widget.insert(tk.END, "\n")
                continue

            if stripped in ("---", "***", "___"):
                widget.insert(tk.END, "────────────────────────────────────\n",
                              "separator")
                continue

            if stripped.startswith("### "):
                insert_inline(stripped[4:], "heading2")
                widget.insert(tk.END, "\n")
                continue

            if stripped.startswith("## "):
                insert_inline(stripped[3:], "heading1")
                widget.insert(tk.END, "\n")
                continue

            if stripped.startswith("# "):
                insert_inline(stripped[2:], "heading1")
                widget.insert(tk.END, "\n")
                continue

            bullet_match = re.match(r"^\s*[-*•]\s+(.*)$", line)
            numbered_match = re.match(r"^\s*(\d+[.)])\s+(.*)$", line)

            if bullet_match:
                widget.insert(tk.END, "  •  ", "bullet")
                insert_inline(bullet_match.group(1))
                widget.insert(tk.END, "\n")
            elif numbered_match:
                widget.insert(tk.END, f"  {numbered_match.group(1)}  ", "bullet")
                insert_inline(numbered_match.group(2))
                widget.insert(tk.END, "\n")
            elif stripped.startswith(">"):
                widget.insert(tk.END, "  " + stripped.lstrip("> ").strip() + "\n",
                              "quote")
            else:
                insert_inline(line)
                widget.insert(tk.END, "\n")

        if in_code and code_lines:
            widget.insert(tk.END, "\n".join(code_lines) + "\n", "code")

        widget.config(state="disabled")
        widget.see(tk.END)

    def send_message(self):

        question = self.user_input.get().strip()

        if not question:
            return

        if self.client is None:

            messagebox.showerror(
                "API Error",
                "Gemini API key not found.\n\n"
                "Please configure GEMINI_API_KEY "
                "in PowerShell."
            )

            return

        self.add_message("You", question)

        self.chat_history.append(
            ("You", question)
        )

        self.user_input.delete(0, tk.END)

        self.send_button.config(state="disabled")

        self.status_label.config(
            text="✦ AIVA is thinking..."
        )

        threading.Thread(
            target=self.get_ai_response,
            args=(question,),
            daemon=True
        ).start()

    def get_ai_response(self, question):

        answer = None
        last_error = None


        prompt = """
You are AIVA, an AI-powered student virtual assistant.

Your main purpose is to help students with academics.

You can help with:

1. Python Programming
2. Mathematics
3. Artificial Intelligence
4. Machine Learning
5. Deep Learning
6. Data Structures and Algorithms
7. Exam Preparation
8. Study Planning

Instructions:

- Answer the student's exact question first; do not give unrelated introductions.
- Keep normal answers concise (usually 5-10 lines). Give detail when the student asks for it.
- Explain concepts in simple language and use a small practical example when useful.
- Explain programming code step by step when code is requested.
- Provide accurate academic information. If unsure, say so instead of guessing.
- Be friendly and supportive, but avoid repeatedly asking generic follow-up questions.
- Use Markdown headings, **bold** for key terms, bullet points for lists, and fenced code blocks for code.
- Do not use Markdown tables unless a comparison genuinely needs one.

"""

        for sender, message in self.chat_history[-12:]:

            prompt += f"\n{sender}: {message}\n"

        prompt += f"\nStudent: {question}\nAIVA:"

        for attempt in range(3):

            try:

                response = self.client.models.generate_content(
                   model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                answer = response.text

                if answer:
                    break

                last_error = "Gemini returned an empty response."

            except Exception as error:

                last_error = error

                error_text = str(error).upper()

                temporary_error = (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "429" in error_text
                    or "RESOURCE_EXHAUSTED" in error_text
                    or "500" in error_text
                    or "INTERNAL" in error_text
                )

                if temporary_error and attempt < 2:

                    time.sleep(2 ** (attempt + 1))
                    continue

                break

        if not answer:

            answer = (
                "Sorry! Gemini AI is temporarily unavailable.\n\n"
                "Please try again after some time.\n\n"
                "Error details: "
                + str(last_error)
            )

        self.root.after(
            0,
            lambda: self.finish_response(question, answer)
        )

    def finish_response(self, question, answer):

        if not hasattr(self, "chat_area"):
            return

        if not self.chat_area.winfo_exists():
            return

        self.add_message(
            "AIVA",
            answer
        )

        self.chat_history.append(
            ("AIVA", answer)
        )

        self.status_label.config(text="")

        self.send_button.config(state="normal")

        self.user_input.focus_set()

    def academic_help(self):

        self.show_chat()

        self.user_input.insert(
            0,
            "Explain the important concepts of Artificial Intelligence with examples."
        )

        self.user_input.focus_set()

    def study_planner(self):

        subjects = simpledialog.askstring(
            "Study Planner",
            "Enter subjects separated by commas:"
        )

        if not subjects:
            return

        subject_list = [
            s.strip()
            for s in subjects.split(",")
            if s.strip()
        ]

        if not subject_list:

            messagebox.showwarning(
                "Warning",
                "Please enter at least one subject."
            )

            return

        hours = simpledialog.askinteger(
            "Study Planner",
            "Enter total study hours:",
            minvalue=1,
            maxvalue=24
        )

        if not hours:
            return

        start = datetime.datetime.now().replace(
            hour=18,
            minute=0,
            second=0,
            microsecond=0
        )

        result = "YOUR STUDY TIMETABLE\n\n"

        for i in range(hours):

            end = start + datetime.timedelta(hours=1)

            subject = subject_list[
                i % len(subject_list)
            ]

            result += (
                start.strftime("%I:%M %p")
                + " - "
                + end.strftime("%I:%M %p")
                + "     "
                + subject
                + "\n\n"
            )

            start = end

        result += "\nHappy Learning! Keep Growing!"

        messagebox.showinfo(
            "Your Study Timetable",
            result
        )

    def add_reminder(self):

        task = simpledialog.askstring(
            "Set Reminder",
            "Enter your study task:"
        )

        if not task:
            return

        minutes = simpledialog.askinteger(
            "Set Reminder",
            "Remind me after how many minutes?",
            minvalue=1
        )

        if not minutes:
            return

        reminder_time = (
            datetime.datetime.now()
            + datetime.timedelta(minutes=minutes)
        )

        self.reminders.append({
            "task": task,
            "time": reminder_time
        })

        messagebox.showinfo(
            "Reminder Set",
            f"Task: {task}\n"
            f"Reminder: {reminder_time.strftime('%I:%M %p')}"
        )

    def view_reminders(self):

        if not self.reminders:

            messagebox.showinfo(
                "Reminders",
                "No pending reminders."
            )

            return

        details = ""

        for reminder in self.reminders:

            details += (
                reminder["task"]
                + " - "
                + reminder["time"].strftime("%I:%M %p")
                + "\n\n"
            )

        messagebox.showinfo(
            "Your Reminders",
            details
        )

    def check_reminders(self):

        now = datetime.datetime.now()

        for reminder in self.reminders[:]:

            if now >= reminder["time"]:

                messagebox.showinfo(
                    "Study Reminder",
                    "Time to study!\n\n"
                    + reminder["task"]
                )

                self.reminders.remove(reminder)

        self.root.after(
            1000,
            self.check_reminders
        )
        
    def clear_chat(self):

        self.chat_history.clear()

        if hasattr(self, "chat_area"):

            if self.chat_area.winfo_exists():

                self.chat_area.config(state="normal")

                self.chat_area.delete(
                    "1.0",
                    tk.END
                )

                self.chat_area.config(state="disabled")

                self.add_message(
                    "AIVA",
                    "Chat cleared! How can I help you?"
                )

                return

        self.show_chat()

    def update_clock(self):

        now = datetime.datetime.now()

        self.clock.config(
            text=now.strftime(
                "%d %b %Y  |  %I:%M:%S %p"
            )
        )

        self.root.after(
            1000,
            self.update_clock
        )   

if __name__ == "__main__":

    root = tk.Tk()

    app = StudyBuddy(root)

    root.mainloop()