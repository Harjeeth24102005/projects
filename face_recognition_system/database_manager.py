import sqlite3
import os
import pickle
import cv2

class DatabaseManager:
    def __init__(self, db_name="face_database.db"):
        self.db_name = db_name
    
    def view_database(self):
        """View all entries in the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, image_path, created_at FROM faces")
        rows = cursor.fetchall()
        
        print("\n=== Face Database ===")
        print(f"{'ID':<3} {'Name':<15} {'Image Path':<30} {'Created At'}")
        print("-" * 70)
        
        for row in rows:
            print(f"{row[0]:<3} {row[1]:<15} {row[2]:<30} {row[3]}")
        
        conn.close()
        return rows
    
    def delete_face(self, name):
        """Delete a face from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT image_path FROM faces WHERE name = ?", (name,))
        result = cursor.fetchone()
        
        if result:
            # Delete image file
            image_path = result[0]
            if os.path.exists(image_path):
                os.remove(image_path)
            
            # Delete database entry
            cursor.execute("DELETE FROM faces WHERE name = ?", (name,))
            conn.commit()
            print(f"Deleted face: {name}")
        else:
            print(f"Face '{name}' not found")
        
        conn.close()
    
    def clear_database(self):
        """Clear entire database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Get all image paths
        cursor.execute("SELECT image_path FROM faces")
        rows = cursor.fetchall()
        
        # Delete image files
        for row in rows:
            if os.path.exists(row[0]):
                os.remove(row[0])
        
        # Clear database
        cursor.execute("DELETE FROM faces")
        conn.commit()
        conn.close()
        
        # Delete encodings cache
        if os.path.exists("face_encodings.pkl"):
            os.remove("face_encodings.pkl")
        
        print("Database cleared successfully")

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.view_database()
    