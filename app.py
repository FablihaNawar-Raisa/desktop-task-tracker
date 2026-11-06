import sqlite3
import tkinter as tk


my_ds = sqlite3.connect("tasks.db")
cursor = my_ds.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    due_date TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)"""
)
my_ds.commit()
my_ds.close()


def show_task():
  task_list.delete(0, tk.END)
  conn = sqlite3.connect("tasks.db")
  cur = conn.cursor()
  cur.execute("SELECT id, title FROM tasks")
  rows = cur.fetchall()
  for i in rows:
    task_list.insert(tk.END, f"{i[0]}: {i[1]}")
  conn.close()


def add_task():
  task_title = task_entry.get()
  if task_title != "":
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, category, due_date) VALUES (?, ?, ?)",
        (task_title, "General", "Today"),
    )
    conn.commit()
    conn.close()

    task_entry.delete(0, tk.END)
    show_task()


def delete_task():
  selected = task_list.curselection()  
  if selected:
    selected_text = task_list.get(selected[0])  
    task_id = selected_text.split(":")[0]  

    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    show_task()  


window = tk.Tk()
window.title("Task Checker")
window.geometry("360x480")
window.attributes("-alpha", 0.88)  

title = tk.Label(window, text="My Daily Tasks", font=("Arial", 14, "bold"))
title.pack(pady=10)

task_entry = tk.Entry(window, width=28)
task_entry.pack(pady=5)

btn_add = tk.Button(
    window, text="Add Task", width=15, bg="#e0ebe6", command=add_task
)
btn_add.pack(pady=5)


task_list = tk.Listbox(window, width=35, height=10)
task_list.pack(pady=10)


btn_delete = tk.Button(
    window,
    text="Delete Selected Task",
    width=18,
    bg="#8d6f72",
    command=delete_task,
)
btn_delete.pack(pady=5)


show_task()

window.mainloop()