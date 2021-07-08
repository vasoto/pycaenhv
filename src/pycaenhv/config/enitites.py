from enum import Enum

from typing import MutableMapping, Union, Any, Optional, Dict

from pydantic import BaseModel


class LinkEnum(str, Enum):
    TCPIP = 'TCPIP'
    RS232 = 'RS232'
    CAENET = 'CAENET'
    USB = 'USB'
    OPTLINK = 'OPTILINK'
    USB_VCP = 'USB_VCP'


class Channel(BaseModel):
    VSet: Optional[float] = None
    ISet: Optional[float] = None
    Trip: Optional[float] = None
    SVmax: Optional[float] = None
    RDown: Optional[float] = None
    RUp: Optional[float] = None


# class Channel(ChannelBase):
#     id: int


class Channels(BaseModel):
    default: Optional[Channel] = None
    channels: Optional[Dict[int, Channel]] = None


class HVBase(BaseModel):
    board: str
    link: LinkEnum
    slot: int = 0
    address: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    channels: Optional[Channels] = None


class Config(BaseModel):
    hv: Dict[str, HVBase]
