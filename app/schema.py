"""API input contract matching training feature names and types."""

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FuelType(str, Enum):
    petrol = "Petrol"
    diesel = "Diesel"
    cng = "CNG"


class SellerType(str, Enum):
    dealer = "Dealer"
    individual = "Individual"


class TransmissionType(str, Enum):
    manual = "Manual"
    automatic = "Automatic"


class CarFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")
    Car_Name: str = Field(..., min_length=1, examples=["swift"])
    Year: int = Field(..., ge=1990, le=2030, examples=[2014])
    Present_Price: float = Field(..., gt=0, examples=[5.59], description="Present_Price field from the dataset, in INR lakhs")
    Kms_Driven: int = Field(..., ge=0, examples=[27000])
    Fuel_Type: FuelType
    Seller_Type: SellerType
    Transmission: TransmissionType
    Owner: Literal[0, 1, 3] = Field(..., examples=[0], description="Previous owner category in this dataset (0, 1 or 3)")


class PredictionResponse(BaseModel):
    prediction_price: float = Field(description="Predicted resale price in INR lakhs")
    unit: str = "INR lakh"
