import os
import schedule
import time
import mysql.connector

class BackupAutomation:
    def __init__(self):
        # Database configuration
        self.db_config = {
            "host": "localhost",
            "user": "root", 
            "password": "your_password"
        }
        
        # Backup paths
        self.locations = {
            "hongdae": "C:/backup/hongdae",
            "busan": "C:/backup/busan",
            "incheon": "C:/backup/incheon"
        }
    
    def run_sql_file(self, database, file_path):
        """Execute SQL file"""
        conn = mysql.connector.connect(database=database, **self.db_config)
        cursor = conn.cursor()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            sql = file.read()
            for command in sql.split(';'):
                if command.strip():
                    cursor.execute(command)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def process_backups(self):
        """Process backup files"""
        print(f"🔄 Backup started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for db_name, path in self.locations.items():
            if not os.path.exists(path):
                continue
                
            sql_files = [f for f in os.listdir(path) if f.endswith('.sql')]
            
            for file_name in sql_files:
                try:
                    self.run_sql_file(db_name, os.path.join(path, file_name))
                    print(f"✅ {db_name}/{file_name}")
                except Exception as e:
                    print(f"❌ {db_name}/{file_name}: {e}")
        
        print(f"✅ Backup completed: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def start_scheduler(self):
        """Auto-run daily at 9 AM"""
        schedule.every().day.at("09:00").do(self.process_backups)
        print("📅 Scheduler started - Auto-run daily at 09:00")
        
        while True:
            schedule.run_pending()
            time.sleep(60)

# Execute
if __name__ == "__main__":
    backup = BackupAutomation()
    
    print("1️⃣ Run now")
    print("2️⃣ Start scheduler")
    
    if input("Choose: ") == "1":
        backup.process_backups()
    else:
        backup.start_scheduler()