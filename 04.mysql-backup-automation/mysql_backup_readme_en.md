# 🚀 MySQL Backup Automation

> **Automatically apply daily SQL backup files to local database**

## ✨ Key Features

- **Auto Scheduling**: Automatic execution daily at 9 AM
- **Multi-DB Support**: Simultaneous processing of multiple branch databases  
- **Error Handling**: Individual file processing ensures stability
- **Immediate Execution**: Manual execution available for testing

## 🚀 Usage

### 1. Installation
```bash
pip install mysql-connector-python schedule
```

### 2. Configuration Changes
```python
# Modify in code
self.db_config = {
    "host": "localhost",
    "user": "root", 
    "password": "actual_password"  # Change this
}

self.locations = {
    "hongdae": "C:/backup/hongdae",    # Change to actual path
    "busan": "C:/backup/busan",
    "incheon": "C:/backup/incheon"
}
```

### 3. Execution
```bash
python backup.py
```

## 📊 Execution Results
```
🔄 Backup started: 2024-01-15 09:00:01
✅ hongdae/backup_20240115.sql
✅ busan/data_backup.sql  
❌ incheon/corrupt_file.sql: Syntax error
✅ Backup completed: 2024-01-15 09:03:22
```

## 🎯 Core Code

### Auto Scheduling
```python
schedule.every().day.at("09:00").do(self.process_backups)
while True:
    schedule.run_pending()
    time.sleep(60)
```

### SQL File Execution
```python
with open(file_path, 'r', encoding='utf-8') as file:
    sql = file.read()
    for command in sql.split(';'):
        if command.strip():
            cursor.execute(command)
```

### Error Handling
```python
try:
    self.run_sql_file(db_name, file_path)
    print(f"✅ {db_name}/{file_name}")
except Exception as e:
    print(f"❌ {db_name}/{file_name}: {e}")
```

## 💡 Practical Impact

| Category | Before | After Automation |
|----------|--------|------------------|
| **Time** | 30 min/day | 2 min/day |
| **Errors** | Occasional | None |
| **Monitoring** | Manual | Automatic |

## 🔧 Extension Methods

**Adding New Branch**
```python
self.locations["gangnam"] = "C:/backup/gangnam"
```

**Different Time Settings**  
```python
schedule.every().day.at("21:00").do(self.process_backups)  # 9 PM
schedule.every().monday.do(self.process_backups)           # Every Monday
```

---

> **Development Period**: 1 day | **Code Lines**: 50 lines | **Automation Effect**: 93% time savings