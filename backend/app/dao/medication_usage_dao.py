"""Medication Usage Data Access Object."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.database import db


class MedicationUsageDAO:
    """Data access operations for medication usage logs."""
    
    @staticmethod
    def create_usage_log(family_member_id: int, medication_id: int, quantity_used: int, connection=None) -> Dict[str, Any]:
        """Create a new medication usage log."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                INSERT INTO medication_usage (family_member_id, medication_id, quantity_used)
                VALUES (%s, %s, %s)
                RETURNING id, family_member_id, medication_id, used_at, quantity_used, created_at, updated_at
            """, (family_member_id, medication_id, quantity_used))
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_usage_logs_by_user_id(user_id: int, connection=None) -> List[Dict[str, Any]]:
        """Get all usage logs for a user (via family members)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT mu.id, mu.family_member_id, mu.medication_id, mu.used_at, mu.quantity_used, mu.created_at, mu.updated_at,
                       fm.name as family_member_name, m.name as medication_name
                FROM medication_usage mu
                JOIN family_members fm ON mu.family_member_id = fm.id
                JOIN medications m ON mu.medication_id = m.id
                WHERE fm.user_id = %s
                ORDER BY mu.used_at DESC
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_usage_log_by_id(usage_id: int, user_id: int, connection=None) -> Optional[Dict[str, Any]]:
        """Get a usage log by ID (with user_id check for security)."""
        with db.get_cursor(connection=connection) as cursor:
            cursor.execute("""
                SELECT mu.id, mu.family_member_id, mu.medication_id, mu.used_at, mu.quantity_used, mu.created_at, mu.updated_at
                FROM medication_usage mu
                JOIN family_members fm ON mu.family_member_id = fm.id
                WHERE mu.id = %s AND fm.user_id = %s
            """, (usage_id, user_id))
            result = cursor.fetchone()
            return dict(result) if result else None

