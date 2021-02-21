// add ngo interfaces here

export interface NgoDetailItem {
  id: number;
  name: string;
  acronym: string;
  metaData: any;
  description: NgoDetailItemDescription;
  fieldOfActivity: NgoDetailItemFieldOfActivity;
  stats: NgoDetailItemStats;
  contact: NgoDetailItemContact;
  rating: NgoDetailItemRating;
}

export interface NgoDetailItemRating {
  trustworthiness: { displayName: string, values: number };
  amount: { displayName: string, values: number };
}

export interface NgoDetailItemContact {
  address: { displayName: string, values: {
    street: string;
    postcode: string;
    city: string;
    country: string;
  }};
  ngoPhoneNumber: { displayName: string, values: string };
  ngoEmail: { displayName: string, values: string };
  representative?: { displayName: string, values: {
    representativeFirstName: string;
    representativeLastName: string;
    representativeEmail: string;
  }};
}

export interface NgoDetailItemStats {
  president?: { displayName: string, values: {
    presidentFirstName: string;
    presidentLastName: string;
  }};
  foundingYear: { displayName: string, values: number };
  staffNumber: { displayName: string, values: number };
  memberNumber: { displayName: string, values: number };
  yearlyIncome: { displayName: string, values: string };
  funding: { displayName: string, values: string };
  accreditations: { displayName: string, values: string[] };
}

export interface NgoDetailItemFieldOfActivity {
  topics: { displayName: string, values: string[] };
  activities: { displayName: string, values: string };
  branches: { displayName: string, values: string[] };
  workingLanguages: { displayName: string, values: string[] };
}

export interface NgoDetailItemDescription {
  aim: { displayName: string, values: string };
  typeOfOrganization: { displayName: string, values: string[] };
  website: { displayName: string, values: string };
}

export interface NgoOverviewItem {
  id: number;
  name: string;
  acronym: string;
  city: number;
  trustworthiness: number;
  amount: number;
}

export interface NgoOverviewItemPagination {
  count: number;
  next: string | null;
  previous: string | null;
  results: NgoOverviewItem[];
  total_pages: number;
  current_page: number;
}

export interface NgoFilterOptions {
  name: { values: string, displayName?: string, icon?: string };
  branches: { values: string[], displayName?: string, icon?: string };
  regions: { values: string[], displayName?: string, icon?: string };
  topics: { values: string[], displayName?: string, icon?: string };
  typeOfOrganization: { values: string[], displayName?: string, icon?: string };
  workingLanguages: { values: string[], displayName?: string, icon?: string };
  funding: { values: string[], displayName?: string, icon?: string };
  hasEcosoc: { values: boolean, displayName?: string, icon?: string };
  isCredible: { values: boolean, displayName?: string, icon?: string };
  trustworthiness: { values: number, displayName?: string, icon?: string };
  countries: { values: string[], displayName?: string, icon?: string };
  cities: { values: {[index: string]: string[]}, displayName?: string, icon?: string };
  contactOptionPresent: { values: boolean, displayName?: string, icon?: string };

  [key: string]: any;
}

export interface NgoFilterSelection {
  [keyOption: string]: any;
}

export interface NgoSortingSelection {
  keyToSort: string;
  orderToSort: string;
}

export interface Names {
  names: string[];
}

export interface NgoFavourite {
  ngoId: number;
  favourite: boolean;
}

export interface NgoConnection {
    connected_ngo_id: string;
}

export interface NgoShortItem {
  id: number;
  name: string;
}

export interface NgoEvent {
    id: number;
    name: string;
    start_date: Date;
    end_date: Date;
    organizer: NgoShortItem;
    description: string;
    tags: string;
}

export interface NewNgo {
  ngoName: string;
  ngoCountry: string;
  representativeFirstName: string;
  representativeLastName: string;
  representativeEmail: string;
}
