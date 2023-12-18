# pylint: disable=too-few-public-methods
from pydantic import BaseModel
class User(BaseModel):
    """
    A Pydantic schema for a User
    """
    Username: str
    Email: str
    Password: str

class Shipment(BaseModel):
    """
    A Pydantic schema for a Shipment
    """
    ShipmentNumber: str
    ContainerNumber: int
    ShipmentDescription: str
    RouteDetails: str
    GoodsType: str
    Device: str
    PickupDate: str
    PONumber: int
    DeliveryNumber: int
    NDCNumber: int
    BatchId: int
    SerialNumber: int
    email: str