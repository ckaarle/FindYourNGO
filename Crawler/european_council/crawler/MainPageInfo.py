from dataclasses import dataclass
from typing import List, Optional


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
    idx: int # as displayed on the website
    name: Name
    address: Address
    contact: ContactInfo
    representative: Representative


@dataclass
class HardFacts:
    website: str
    president: str
    founding_year: Optional[int]
    staff_number: Optional[int]
    members: Optional[int]
    working_languages: List[str]


@dataclass
class SoftFacts:
    aims: str
    activities: str
    accreditations: str
    areas_of_competence: List[str]
    greographical_representation: List[str]


@dataclass
class DetailPageInfo:
    idx: int # as displayed on the website
    hard_facts: HardFacts
    soft_facts: SoftFacts