import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {NgoFilterOptions, NgoFilterSelection, NgoOverviewItemPagination} from '../models/ngo';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FilterService {
  selectedFilters: NgoFilterSelection = {} as NgoFilterSelection;
  filteredNgoItems: NgoOverviewItemPagination = {} as NgoOverviewItemPagination;
  public selectedFiltersChanged: EventEmitter<NgoFilterSelection> = new EventEmitter<NgoFilterSelection>();
  public filteredNgoOverviewItemsChanged: EventEmitter<NgoOverviewItemPagination> = new EventEmitter<NgoOverviewItemPagination>();
  public loadingNgoOverviewItems: EventEmitter<boolean> = new EventEmitter<boolean>();


  baseUrlGet = 'http://localhost:8000/ngos/filter';
  baseUrlPost = this.baseUrlGet + '/';
  pageSignifier = '?page=';

  constructor(private http: HttpClient) {
  }

  getSelectedFilters(): NgoFilterSelection {
    return this.selectedFilters;
  };

  editSelectedFilters(selectedFilters: NgoFilterSelection): void {
    this.selectedFilters = selectedFilters;
    console.log("Selected Filters: ", this.selectedFilters)
    this.selectedFiltersChanged.emit(this.selectedFilters);
    this.loadingNgoOverviewItems.emit(true);
  };

  getFilteredNgoItems(): NgoOverviewItemPagination {
    return this.filteredNgoItems;
  }

  displayFilteredNgoItems(filteredNgoItems: NgoOverviewItemPagination): void {
    this.filteredNgoItems = filteredNgoItems;
    this.filteredNgoOverviewItemsChanged.emit(this.filteredNgoItems);
  }

  getNgoFilterOptions(): Observable<any> {
    let endpoint = 'http://localhost:8000/ngos/filteroptions';
    return this.http.get<any>(endpoint); //TODO: move this to request service
  }


  getFilterSelection(filterSelection: NgoFilterSelection): Observable<NgoOverviewItemPagination> {
    return this.http.post<NgoOverviewItemPagination>(this.baseUrlPost, filterSelection); //TODO: move this to request service
  }

  applyFilter(filterSelection: NgoFilterSelection, pageNumber: number = 0): Observable<NgoOverviewItemPagination> {
    if (pageNumber === 0) {
      return this.getFilterSelection(filterSelection);
    } else {
      const url = this.baseUrlGet + this.pageSignifier + pageNumber.toString();
      return this.http.get<NgoOverviewItemPagination>(url, filterSelection);
    }
  }
}
