from dataclasses import dataclass

from selenium.webdriver.remote.webelement import WebElement


@dataclass
class Name:
    name: str
    acronym: str


@dataclass
class Address:
    detail_address: str
    city: str
    country: str
    unprocessed_address: str


@dataclass
class ContactInfo:
    phone_number: str
    email: str
    unprocessed_contact: str


@dataclass
class Representative:
    representative_name: str
    representative_email: str
    unprocessed_representative: str


@dataclass
class MainPageInfo:
    idx: int
    name: Name
    link: WebElement
    address: Address
    contact: ContactInfo
    representative: Representative
