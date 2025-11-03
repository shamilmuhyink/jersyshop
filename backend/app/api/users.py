from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserResponse, AddressSchema
from app.services.user_service import UserService
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_profile(db: Session = Depends(get_db)):
    """Get current user profile"""
    current_user = await get_current_user(db)
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    first_name: str,
    last_name: str,
    phone: str = None,
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    current_user = await get_current_user(db)
    user_service = UserService(db)
    return await user_service.update_profile(current_user.id, {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone
    })

@router.post("/addresses")
async def add_address(address_data: AddressSchema, db: Session = Depends(get_db)):
    """Add new address to user's address book"""
    current_user = await get_current_user(db)
    user_service = UserService(db)
    return await user_service.add_address(current_user.id, address_data)

@router.get("/addresses")
async def get_addresses(db: Session = Depends(get_db)):
    """Get user's saved addresses"""
    current_user = await get_current_user(db)
    user_service = UserService(db)
    return await user_service.get_addresses(current_user.id)

@router.put("/addresses/{address_id}")
async def update_address(
    address_id: str,
    address_data: AddressSchema,
    db: Session = Depends(get_db)
):
    """Update saved address"""
    current_user = await get_current_user(db)
    user_service = UserService(db)
    return await user_service.update_address(current_user.id, address_id, address_data)

@router.delete("/addresses/{address_id}")
async def delete_address(address_id: str, db: Session = Depends(get_db)):
    """Delete saved address"""
    current_user = await get_current_user(db)
    user_service = UserService(db)
    success = await user_service.delete_address(current_user.id, address_id)
    if not success:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Address deleted successfully"}