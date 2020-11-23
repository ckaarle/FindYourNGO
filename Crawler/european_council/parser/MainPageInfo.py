from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Name:
    name: str
    acronym: str
    funding: Optional[str]


@dataclass
class Address:
    street: Optional[str]
    postcode: Optional[str]
    city: Optional[str]
    country: Optional[str]


@dataclass
class ContactInfo:
    phone_number: Optional[str]
    email: Optional[str]


@dataclass
class Representative:
    representative_lastname: Optional[str]
    representative_firstname: Optional[str]
    representative_email: Optional[str]


@dataclass
class MainPageInfo:
    idx: int
    name: Name
    address: Address
    contact: ContactInfo
    representative: Representative


@dataclass
class HardFacts:
    website: Optional[str]
    president_firstname: Optional[str]
    president_lastname: Optional[str]
    founding_year: Optional[int]
    staff_number: Optional[int]
    members: Optional[int]
    working_languages: Optional[str]


@dataclass
class SoftFacts:
    aims: Optional[str]
    activities: Optional[str]
    accreditations: Optional[str]
    areas_of_competence: Optional[List[str]]
    greographical_representation: Optional[List[str]]


@dataclass
class DetailPageInfo:
    idx: int
    last_updated: str
    hard_facts: HardFacts
    soft_facts: SoftFacts


@dataclass
class Info:
    main_info: MainPageInfo
    detail_info: DetailPageInfo