import {EventEmitter, Injectable} from '@angular/core';
import {NgoFilterOptions, NgoFilterSelection, NgoOverviewItemPagination} from '../models/ngo';
import {Observable} from 'rxjs';
import {ApiService} from './api.service';

@Injectable({
    providedIn: 'root'
})
export class FilterService {
    selectedFilters: NgoFilterSelection = {} as NgoFilterSelection;
    filteredNgoItems: NgoOverviewItemPagination = {} as NgoOverviewItemPagination;
    public selectedFiltersChanged: EventEmitter<NgoFilterSelection> = new EventEmitter<NgoFilterSelection>();
    public filteredNgoOverviewItemsChanged: EventEmitter<NgoOverviewItemPagination> = new EventEmitter<NgoOverviewItemPagination>();
    public loadingNgoOverviewItems: EventEmitter<boolean> = new EventEmitter<boolean>();

    constructor(public apiService: ApiService) {
    }

    getSelectedFilters(): NgoFilterSelection {
        return this.selectedFilters;
    }

    editSelectedFilters(selectedFilters: NgoFilterSelection): void {
        this.selectedFilters = selectedFilters;
        this.selectedFiltersChanged.emit(this.selectedFilters);
        this.loadingNgoOverviewItems.emit(true);
    }

    displayFilteredNgoItems(filteredNgoItems: NgoOverviewItemPagination): void {
        this.filteredNgoItems = filteredNgoItems;
        this.filteredNgoOverviewItemsChanged.emit(this.filteredNgoItems);
    }

    applyFilter(filterSelection: NgoFilterSelection, pageNumber: number = 0): Observable<NgoOverviewItemPagination> {
        if (pageNumber === 0) {
            return this.apiService.get('ngos/filter', {filter_selection: encodeURIComponent( JSON.stringify(filterSelection))});
        }
        return this.apiService.get('ngos/filter', {filter_selection: encodeURIComponent( JSON.stringify(filterSelection)), page: pageNumber});
    }
}
