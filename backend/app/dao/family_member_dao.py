"""Family Member Data Access Object."""
from typing import List, Dict, Any, Optional
from datetime import date
from app.database import db


class FamilyMemberDAO:
    """Data access operations for family members."""
    
    @staticmethod
    def create_family_member(user_id: int, name: str, date_of_birth: Optional[date] = None,
                            gender: Optional[str] = None, profession: Optional[str] = None,
                            health_notes: Optional[str] = None, connection=None) -> Dict[str, Any]:
        """Create a new family member."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                INSERT INTO family_members (user_id, name, date_of_birth, gender, profession, health_notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, user_id, name, date_of_birth, gender, profession, health_notes, created_at, updated_at
            """, (user_id, name, date_of_birth, gender, profession, health_notes))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_family_members_by_user_id(user_id: int, connection=None) -> List[Dict[str, Any]]:
        """Get all family members for a user."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, user_id, name, date_of_birth, gender, profession, health_notes, created_at, updated_at
                FROM family_members
                WHERE user_id = %s
                ORDER BY created_at DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_family_member_by_id(family_member_id: int, user_id: int, connection=None) -> Optional[Dict[str, Any]]:
        """Get a family member by ID (with user_id check for security)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT id, user_id, name, date_of_birth, gender, profession, health_notes, created_at, updated_at
                FROM family_members
                WHERE id = %s AND user_id = %s
            """, (family_member_id, user_id))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def update_family_member(family_member_id: int, user_id: int, name: Optional[str] = None,
                            date_of_birth: Optional[date] = None, gender: Optional[str] = None,
                            profession: Optional[str] = None, health_notes: Optional[str] = None,
                            connection=None) -> Optional[Dict[str, Any]]:
        """Update a family member."""
        updates = []
        values = []
        
        if name is not None:
            updates.append("name = %s")
            values.append(name)
        if date_of_birth is not None:
            updates.append("date_of_birth = %s")
            values.append(date_of_birth)
        if gender is not None:
            updates.append("gender = %s")
            values.append(gender)
        if profession is not None:
            updates.append("profession = %s")
            values.append(profession)
        if health_notes is not None:
            updates.append("health_notes = %s")
            values.append(health_notes)
        
        if not updates:
            return FamilyMemberDAO.get_family_member_by_id(family_member_id, user_id, connection=connection)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.extend([family_member_id, user_id])
        
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute(f"""
                UPDATE family_members
                SET {', '.join(updates)}
                WHERE id = %s AND user_id = %s
                RETURNING id, user_id, name, date_of_birth, gender, profession, health_notes, created_at, updated_at
            """, values)
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def delete_family_member(family_member_id: int, user_id: int, connection=None) -> bool:
        """Delete a family member."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                DELETE FROM family_members
                WHERE id = %s AND user_id = %s
            """, (family_member_id, user_id))
            return cursor.rowcount > 0

