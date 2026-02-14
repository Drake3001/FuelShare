from typing import Optional, List

from pydantic import BaseModel, model_validator, Field, field_validator
from datetime import datetime
from .user_schema import UserSchema
from .vehicle_schema import VehicleSchema


class TripCreateSchema(BaseModel):
    start_lat: float
    start_lon: float
    end_lat: float
    end_lon: float
    start_time: datetime
    end_time: datetime
    duration: int
    distance: float
    ev_duration: int | None
    ev_distance: float | None

    fuel_consumed: float
    average_fuel_consumed: float

class TripSchema(TripCreateSchema):
    id: int
    refuel: bool | None
    driver: UserSchema | None
    vehicle: VehicleSchema | None
    period: int | None
    start_address: str | None = None
    end_address: str | None = None
    payer_ids: List[int] = Field(default=[], validation_alias="payers")
    class Config:
        from_attributes = True
    @field_validator("payer_ids", mode="before")
    @classmethod
    def extract_ids_from_users(cls, v):
        if not v:
            return []

        if hasattr(v[0], "id"):
            return [user.id for user in v]

        return v

class TripUpdateSchema(BaseModel):
    id: int
    refuel: bool | None = None
    driver_id: int | None = None
    payer_ids: Optional[List[int]] = None
    vehicle_id: int | None = None
    period: int | None = None
    start_address: str | None = None
    end_address: str | None = None


    @model_validator(mode="after")
    def ensure_has_id(self):
        if not self.id:
            raise ValueError("id is required for update")
        return self

