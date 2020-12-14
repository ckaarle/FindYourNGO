import { EventEmitter, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { NgoFilterOptions, NgoFilterSelection, NgoOverviewItem } from '../models/ngo';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FilterService {
  selectedFilters: NgoFilterSelection = {} as NgoFilterSelection;
  filteredNgoItems: NgoOverviewItem[] = {} as NgoOverviewItem[];
  public selectedFiltersChanged: EventEmitter<NgoFilterSelection> = new EventEmitter<NgoFilterSelection>();
  public filteredNgoOverviewItemsChanged: EventEmitter<NgoOverviewItem[]> = new EventEmitter<NgoOverviewItem[]>();

  constructor(private http: HttpClient) { }

  getSelectedFilters(): NgoFilterSelection {
    return this.selectedFilters;
  };

  editSelectedFilters(selectedFilters: NgoFilterSelection): void {
    this.selectedFilters = selectedFilters;
    this.selectedFiltersChanged.emit(this.selectedFilters);
  };

  getFilteredNgoItems(): NgoOverviewItem[] {
    return this.filteredNgoItems;
  }

  displayFilteredNgoItems(filteredNgoItems: NgoOverviewItem[]): void {
    this.filteredNgoItems = filteredNgoItems;
    this.filteredNgoOverviewItemsChanged.emit(this.filteredNgoItems);
  }

  getNgoFilterOptions(): Observable<NgoFilterOptions> {
    let endpoint = 'http://localhost:8000/ngos/filter';
    return this.http.get<NgoFilterOptions>(endpoint); //TODO: move this to request service
  }

  applyFilter(filterSelection: NgoFilterSelection): Observable<NgoOverviewItem[]> {
    let endpoint = 'http://localhost:8000/ngos/filter/';
    return this.http.post<NgoOverviewItem[]>(endpoint, filterSelection); //TODO: move this to request service
  }
}
