// add ngo interfaces here

export interface NgoDetailItem {
  id: number;
  name: string;
  acronym: string;
  description: NgoDetailItemDescription;
  fieldOfActivity: NgoDetailItemFieldOfActivity;
  stats: NgoDetailItemStats;
  location: {address: {displayName: string, values: string}};
  contact: NgoDetailItemContact;
  rating: NgoDetailItemRating;
}

export interface NgoDetailItemRating {
  trustworthiness: {displayName: string, values: number};
  amount: {displayName: string, values: number};
}

export interface NgoDetailItemContact {
  ngoPhoneNumber: {displayName: string, values: string};
  ngoEmail: {displayName: string, values: string};
  representative?: {displayName: string, values: string};
}

export interface NgoDetailItemStats {
  president?: {displayName: string, values: string};
  foundingYear: {displayName: string, values: number};
  staffNumber: {displayName: string, values: number};
  memberNumber: {displayName: string, values: number};
  yearlyIncome: {displayName: string, values: string};
  funding: {displayName: string, values: string};
  accreditations: {displayName: string, values: string[]};
}

export interface NgoDetailItemFieldOfActivity {
  topics: {displayName: string, values: string[]};
  activities: {displayName: string, values: string};
  branches: {displayName: string, values: string[]};
  workingLanguages: {displayName: string, values: string[]};
}

export interface NgoDetailItemDescription {
  aim: {displayName: string, values: string};
  typeOfOrganization: {displayName: string, values: string[]};
  website: {displayName: string, values: string};
}

export interface NgoOverviewItem {
  id: number;
  name: string;
  acronym: string;
  city: number;
  trustworthiness: number;
  amount: number; //TODO
}

export interface NgoOverviewItemPagination {
  count: number;
  next: string | null;
  previous: string | null;
  results: NgoOverviewItem[];
  total_pages: number;
  current_page: number;
}

export interface Countries {
    countries: string[];
}

export interface Topics {
    topics: string[];
}
