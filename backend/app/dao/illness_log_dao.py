"""Illness Log Data Access Object."""
from typing import List, Dict, Any, Optional
from datetime import date
from app.database import db


class IllnessLogDAO:
    """Data access operations for illness logs."""
    
    @staticmethod
    def create_illness_log(
        family_member_id: int,
        illness_name: str,
        start_date: date,
        end_date: Optional[date] = None,
        notes: Optional[str] = None,
        ai_suggestion: Optional[str] = None,
        connection=None
    ) -> Dict[str, Any]:
        """Create a new illness log."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                INSERT INTO illness_logs (family_member_id, illness_name, start_date, end_date, notes, ai_suggestion)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, family_member_id, illness_name, start_date, end_date, notes, ai_suggestion, created_at, updated_at
            """, (family_member_id, illness_name, start_date, end_date, notes, ai_suggestion))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_illness_logs_by_user_id(user_id: int, family_member_id: Optional[int] = None, connection=None) -> List[Dict[str, Any]]:
        """Get all illness logs for a user's family members, optionally filtered by family member."""
        with db.get_cursor(connection=connection) as cursor:
            if family_member_id:
                cursor.execute("""
                    SELECT il.id, il.family_member_id, fm.name as family_member_name,
                           il.illness_name, il.start_date, il.end_date, il.notes, il.ai_suggestion,
                           il.created_at, il.updated_at
                    FROM illness_logs il
                    JOIN family_members fm ON il.family_member_id = fm.id
                    WHERE fm.user_id = %s AND il.family_member_id = %s
                    ORDER BY il.start_date DESC
                """, (user_id, family_member_id))
            else:
                cursor.execute("""
                    SELECT il.id, il.family_member_id, fm.name as family_member_name,
                           il.illness_name, il.start_date, il.end_date, il.notes, il.ai_suggestion,
                           il.created_at, il.updated_at
                    FROM illness_logs il
                    JOIN family_members fm ON il.family_member_id = fm.id
                    WHERE fm.user_id = %s
                    ORDER BY il.start_date DESC
                """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_illness_log_by_id(illness_log_id: int, user_id: int, connection=None) -> Optional[Dict[str, Any]]:
        """Get an illness log by ID (with user_id check for security)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT il.id, il.family_member_id, fm.name as family_member_name,
                       il.illness_name, il.start_date, il.end_date, il.notes, il.ai_suggestion,
                       il.created_at, il.updated_at
                FROM illness_logs il
                JOIN family_members fm ON il.family_member_id = fm.id
                WHERE il.id = %s AND fm.user_id = %s
            """, (illness_log_id, user_id))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def update_illness_log(
        illness_log_id: int,
        user_id: int,
        illness_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        notes: Optional[str] = None,
        ai_suggestion: Optional[str] = None,
        connection=None
    ) -> Optional[Dict[str, Any]]:
        """Update an illness log."""
        updates = []
        values = []
        
        if illness_name is not None:
            updates.append("illness_name = %s")
            values.append(illness_name)
        if start_date is not None:
            updates.append("start_date = %s")
            values.append(start_date)
        if end_date is not None:
            updates.append("end_date = %s")
            values.append(end_date)
        if notes is not None:
            updates.append("notes = %s")
            values.append(notes)
        if ai_suggestion is not None:
            updates.append("ai_suggestion = %s")
            values.append(ai_suggestion)
        
        if not updates:
            return IllnessLogDAO.get_illness_log_by_id(illness_log_id, user_id, connection=connection)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.extend([illness_log_id, user_id])
        
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute(f"""
                UPDATE illness_logs il
                SET {', '.join(updates)}
                FROM family_members fm
                WHERE il.id = %s AND il.family_member_id = fm.id AND fm.user_id = %s
                RETURNING il.id, il.family_member_id, il.illness_name, il.start_date, 
                          il.end_date, il.notes, il.created_at, il.updated_at
            """, values)
            result = cursor.fetchone()
            if result:
                # Fetch with family member name
                return IllnessLogDAO.get_illness_log_by_id(illness_log_id, user_id, connection=connection)
            return None
    
    @staticmethod
    def delete_illness_log(illness_log_id: int, user_id: int, connection=None) -> bool:
        """Delete an illness log."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                DELETE FROM illness_logs il
                USING family_members fm
                WHERE il.id = %s AND il.family_member_id = fm.id AND fm.user_id = %s
            """, (illness_log_id, user_id))
            return cursor.rowcount > 0
