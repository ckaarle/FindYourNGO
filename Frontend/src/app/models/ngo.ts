// add ngo interfaces here

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
    branches: {values: string[], displayName?: string, icon?: string};
    topics: {values: string[], displayName?: string, icon?: string};
    typeOfOrganization: {values: string[], displayName?: string, icon?: string};
    workingLanguages: {values: string[], displayName?: string, icon?: string};
    funding: {values: string[], displayName?: string, icon?: string};
    hasEcosoc: {values: boolean, displayName?: string, icon?: string};
    isCredible: {values: boolean, displayName?: string, icon?: string};
    trustworthiness: {values: number, displayName?: string, icon?: string};
    hqCountries: {values: string[], displayName?: string, icon?: string};
    hqCities: {values: string, displayName?: string, icon?: string};
    contactOptionPresent: {values: boolean, displayName?: string, icon?: string};
}
