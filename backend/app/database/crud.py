from typing import List, Optional
from sqlmodel import Session, select
from app.database.models import User, Prediction
import logging

logger = logging.getLogger(__name__)

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_prediction(session: Session, prediction: Prediction) -> Prediction:
    """Create a new prediction in the database"""
    try:
        session.add(prediction)
        session.commit()
        session.refresh(prediction)
        return prediction
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating prediction: {e}")
        raise

def list_predictions(session: Session, user_id: int, limit: int = 20) -> List[Prediction]:
    """List predictions for a user"""
    try:
        statement = select(Prediction).where(Prediction.user_id == user_id).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"Error listing predictions: {e}")
        raise

def get_all_users(session: Session, limit: int = 100) -> List[User]:
    """Get all users (admin only)"""
    try:
        statement = select(User).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"Error getting all users: {e}")
        raise

def get_all_predictions(session: Session, limit: int = 100) -> List[Prediction]:
    """Get all predictions (admin only)"""
    try:
        statement = select(Prediction).limit(limit)
        return session.exec(statement).all()
    except Exception as e:
        logger.error(f"Error getting all predictions: {e}")
        raise

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    try:
        return session.get(User, user_id)
    except Exception as e:
        logger.error(f"Error getting user by ID: {e}")
        raise

def get_prediction_by_id(session: Session, prediction_id: int) -> Optional[Prediction]:
    """Get prediction by ID"""
    try:
        return session.get(Prediction, prediction_id)
    except Exception as e:
        logger.error(f"Error getting prediction by ID: {e}")
        raise

def delete_user(session: Session, user_id: int) -> bool:
    """Delete a user"""
    try:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting user: {e}")
        raise

def delete_prediction(session: Session, prediction_id: int) -> bool:
    """Delete a prediction"""
    try:
        prediction = session.get(Prediction, prediction_id)
        if prediction:
            session.delete(prediction)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting prediction: {e}")
        raise

def update_user(session: Session, user_id: int, full_name: str = None, email: str = None) -> Optional[User]:
    """Update a user"""
    try:
        user = session.get(User, user_id)
        if not user:
            return None
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating user: {e}")
        raise