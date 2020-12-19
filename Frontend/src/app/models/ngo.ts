// add ngo interfaces here

export interface NgoDetailItem {
  id: number;
  name: string;
  acronym: string;
  aim: string;
  activities: string;
  branches: string[];
  topics: string[];
  accreditations: string[];
  stats: NgoStats;
  contact: NgoContact;
  trustworthiness: number;
  amount: number; //TODO
}

export interface NgoStats {
  foundingYear: number;
  staffNumber: number;
  memberNumber: number;
  workingLanguages: string;
  funding: string;
  presidentFirstName: string;
  presidentLastName: string;
  yearlyIncome: string;
  typeOfOrganization: string[];
}

export interface NgoContact {
  ngoPhoneNumber: string;
  ngoEmail: string;
  website: string;
  representative: {
    representativeFirstName: string;
    representativeLastName: string;
    representativeEmail: string;
  };
  address: {
    street: string;
    postcode: string;
    city: string;
    country: string;
  }
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
