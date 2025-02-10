## 📚 **Assistant Bot - Address Book**

This is a **command-line assistant bot** that helps you **store contacts, phone numbers, and birthdays**. You can **add, edit, delete, and search** contacts, as well as **check upcoming birthdays**. Your data is saved automatically using **Pickle**, so it persists between runs.

---

## 🛠 **Installation**

To use the assistant bot, follow these steps:

1. **Clone this repository**:

   ```
   git clone https://github.com/jamleston/address-book
   cd address-book
   ```

2. **Run the script**:

   ```
   python main.py
   ```

3. **Start interacting with the bot**! 🎉

---

## 📝 **Features & Commands**

This bot supports the following commands:

### 1️⃣ **Basic Commands**

| Command          | Description                               |
| ---------------- | ----------------------------------------- |
| `hello`          | Greets the user and asks how it can help. |
| `close` / `exit` | Exits the bot and saves all contacts.     |

### 2️⃣ **Adding & Managing Contacts**

| Command                     | Description                                    | Example                 |
| --------------------------- | ---------------------------------------------- | ----------------------- |
| `add <name> <phone>`        | Adds a new contact or updates an existing one. | `add Bob 1234567890`    |
| `change <name> <new_phone>` | Changes the first phone number of a contact.   | `change Bob 0987654321` |
| `phone <name>`              | Displays the phone number(s) of a contact.     | `phone Bob`             |
| `all`                       | Shows all saved contacts.                      | `all`                   |
| `delete <name>`             | Deletes a contact from the address book.       | `delete Bob`            |

### 3️⃣ **Managing Birthdays**

| Command                            | Description                                      | Example                       |
| ---------------------------------- | ------------------------------------------------ | ----------------------------- |
| `add-birthday <name> <DD.MM.YYYY>` | Adds a birthday to a contact.                    | `add-birthday Bob 15.06.1995` |
| `show-birthday <name>`             | Displays the birthday of a contact.              | `show-birthday Bob`           |
| `birthdays`                        | Shows upcoming birthdays within the next 7 days. | `birthdays`                   |

---

## 💾 **Data Persistence**

- All data is **automatically saved** in `addressbook.pkl` when the bot exits.
- On the next run, the bot will **load previous contacts and birthdays**.

---

## ⚠ **Error Handling**

The bot includes built-in **error handling** with helpful messages:

| Issue                    | Response                                 |
| ------------------------ | ---------------------------------------- |
| **Missing phone number** | `"Enter name and phone for the command"` |
| **Invalid date format**  | `"Invalid date format. Use DD.MM.YYYY"`  |
| **Nonexistent contact**  | `"We don't have this contact"`           |

---

Happy coding and using! 🚀

