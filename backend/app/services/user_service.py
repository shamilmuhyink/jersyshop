from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.user import User
from app.schemas import AddressSchema

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def update_profile(self, user_id: str, profile_data: dict) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update fields
        for field, value in profile_data.items():
            if value is not None:
                setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    async def add_address(self, user_id: str, address_data: AddressSchema) -> dict:
        # In a real implementation, you'd have a separate addresses table
        # For now, return the address data as confirmation
        return address_data.dict()

    async def get_addresses(self, user_id: str) -> List[dict]:
        # In a real implementation, you'd fetch from addresses table
        # For now, return empty list
        return []

    async def update_address(self, user_id: str, address_id: str, address_data: AddressSchema) -> dict:
        # In a real implementation, you'd update the address in the database
        return address_data.dict()

    async def delete_address(self, user_id: str, address_id: str) -> bool:
        # In a real implementation, you'd delete the address from the database
        return True