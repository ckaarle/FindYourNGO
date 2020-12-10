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

export interface Countries {
    countries: string[];
}

export interface Topics {
    topics: string[];
}
