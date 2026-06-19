from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.activity_log_schemas import (
    ActivityLogCreate,
    ActivityLogUpdate
)

from app.services.activity_log_service import (
    create_activity_log_service,
    get_activity_logs_service,
    get_activity_log_by_id_service,
    get_recent_activities_service,
    get_activities_by_type_service,
    get_activities_by_admin_service,
    get_activities_by_date_service,
    update_activity_log_service,
    delete_activity_log_service,
    get_activity_summary_service
)

router = APIRouter(
    prefix="/activity-logs",
    tags=["Activity Logs"]
)


#  CREATE ACTIVITY
@router.post("/")
def create_activity(payload: ActivityLogCreate, db: Session = Depends(get_db)):
    return create_activity_log_service(db, payload)


#  GET ALL ACTIVITIES
@router.get("/")
def get_all_activities(db: Session = Depends(get_db)):
    return get_activity_logs_service(db)


#  GET RECENT ACTIVITIES
@router.get("/recent/{limit}")
def get_recent_activities(limit: int, db: Session = Depends(get_db)):
    return get_recent_activities_service(db, limit)


#  GET ACTIVITIES BY TYPE
@router.get("/type/{activity_type}")
def get_activities_by_type(activity_type: str, db: Session = Depends(get_db)):
    return get_activities_by_type_service(db, activity_type)


#  GET ACTIVITIES BY ADMIN
@router.get("/admin/{admin_id}")
def get_activities_by_admin(admin_id: int, db: Session = Depends(get_db)):
    return get_activities_by_admin_service(db, admin_id)


#  GET ACTIVITIES BY DATE
@router.get("/date/{activity_date}")
def get_activities_by_date(activity_date: str, db: Session = Depends(get_db)):
    return get_activities_by_date_service(db, activity_date)


#  GET ACTIVITY SUMMARY
@router.get("/summary")
def get_activity_summary(db: Session = Depends(get_db)):
    return get_activity_summary_service(db)


#  UPDATE ACTIVITY
@router.put("/{activity_id}")
def update_activity(activity_id: int, payload: ActivityLogUpdate, db: Session = Depends(get_db)):
    return update_activity_log_service(db, activity_id, payload)

# DELETE ACTIVITY
@router.delete("/{activity_id}")
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    return delete_activity_log_service(db, activity_id)


#  GET ACTIVITY BY ID 
@router.get("/{activity_id}")
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)):
    return get_activity_log_by_id_service(db, activity_id)