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
}
