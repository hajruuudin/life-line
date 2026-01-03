"""Medication Data Access Object."""
from typing import List, Dict, Any, Optional
from datetime import date
from app.database import db


class MedicationDAO:
    """Data access operations for medications."""
    
    @staticmethod
    def create_medication(user_id: int, name: str, quantity: int, expiration_date: Optional[date] = None, connection=None) -> Dict[str, Any]:
        """Create a new medication."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                INSERT INTO medications (user_id, name, quantity, expiration_date)
                VALUES (%s, %s, %s, %s)
                RETURNING id, user_id, name, quantity, expiration_date, created_at, updated_at
            """, (user_id, name, quantity, expiration_date))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_medications_by_user_id(user_id: int, connection=None) -> List[Dict[str, Any]]:
        """Get all medications for a user."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, user_id, name, quantity, expiration_date, created_at, updated_at
                FROM medications
                WHERE user_id = %s
                ORDER BY name ASC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_medication_by_id(medication_id: int, user_id: int, connection=None) -> Optional[Dict[str, Any]]:
        """Get a medication by ID (with user_id check for security)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, user_id, name, quantity, expiration_date, created_at, updated_at
                FROM medications
                WHERE id = %s AND user_id = %s
            """, (medication_id, user_id))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_medication_by_name(user_id: int, name: str, connection=None) -> Optional[Dict[str, Any]]:
        """Get a medication by name for a user (for inventory update logic)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, user_id, name, quantity, expiration_date, created_at, updated_at
                FROM medications
                WHERE user_id = %s AND LOWER(name) = LOWER(%s)
            """, (user_id, name))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def update_medication(medication_id: int, user_id: int, name: Optional[str] = None,
                         quantity: Optional[int] = None, expiration_date: Optional[date] = None, connection=None) -> Optional[Dict[str, Any]]:
        """Update a medication."""
        updates = []
        values = []
        
        if name is not None:
            updates.append("name = %s")
            values.append(name)
        if quantity is not None:
            updates.append("quantity = %s")
            values.append(quantity)
        if expiration_date is not None:
            updates.append("expiration_date = %s")
            values.append(expiration_date)
        
        if not updates:
            return MedicationDAO.get_medication_by_id(medication_id, user_id, connection=connection)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.extend([medication_id, user_id])
        
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute(f"""
                UPDATE medications
                SET {', '.join(updates)}
                WHERE id = %s AND user_id = %s
                RETURNING id, user_id, name, quantity, expiration_date, created_at, updated_at
            """, values)
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def increment_medication_quantity(medication_id: int, user_id: int, quantity_to_add: int, connection=None) -> Optional[Dict[str, Any]]:
        """Increment medication quantity (for inventory updates)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                UPDATE medications
                SET quantity = quantity + %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s AND user_id = %s
                RETURNING id, user_id, name, quantity, expiration_date, created_at, updated_at
            """, (quantity_to_add, medication_id, user_id))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def delete_medication(medication_id: int, user_id: int, connection=None) -> bool:
        """Delete a medication."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                DELETE FROM medications
                WHERE id = %s AND user_id = %s
            """, (medication_id, user_id))
            return cursor.rowcount > 0

