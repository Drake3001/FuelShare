from pydantic import BaseModel


class VehicleCreateSchema(BaseModel):
    vin_number: str

class VehicleUpdateSchema(VehicleCreateSchema):
    pass

class VehicleSchema(BaseModel):
    id: int
    vin_number: str
