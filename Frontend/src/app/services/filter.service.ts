import {EventEmitter, Injectable} from '@angular/core';
import {NgoFilterSelection, NgoOverviewItemPagination, NgoSortingSelection} from '../models/ngo';
import {Observable} from 'rxjs';
import {ApiService} from './api.service';
import {Utils} from './utils';

@Injectable({
    providedIn: 'root'
})
export class FilterService {
    selectedFilters: NgoFilterSelection = {} as NgoFilterSelection;
    selectedSorting: NgoSortingSelection = {} as NgoSortingSelection;
    filteredNgoItems: NgoOverviewItemPagination = {} as NgoOverviewItemPagination;
    public selectedFiltersChanged: EventEmitter<NgoFilterSelection> = new EventEmitter<NgoFilterSelection>();
    public selectedSortingChanged: EventEmitter<NgoSortingSelection> = new EventEmitter<NgoSortingSelection>();
    public filteredNgoOverviewItemsChanged: EventEmitter<NgoOverviewItemPagination> = new EventEmitter<NgoOverviewItemPagination>();
    public loadingNgoOverviewItems: EventEmitter<boolean> = new EventEmitter<boolean>();

    constructor(public apiService: ApiService) {
    }

    getSelectedFilters(): NgoFilterSelection {
        return this.selectedFilters;
    }

    editSelectedFilters(selectedFilters: NgoFilterSelection, selectedSorting: NgoSortingSelection): void {
        this.selectedFilters = selectedFilters;
        this.selectedFiltersChanged.emit(this.selectedFilters);
        this.selectedSorting = selectedSorting;
        this.selectedSortingChanged.emit(this.selectedSorting);
        this.loadingNgoOverviewItems.emit(true);
    }

    displayFilteredNgoItems(filteredNgoItems: NgoOverviewItemPagination): void {
        this.filteredNgoItems = filteredNgoItems;
        this.filteredNgoOverviewItemsChanged.emit(this.filteredNgoItems);
    }

    applyFilter(filterSelection: NgoFilterSelection, sortingSelection: NgoSortingSelection, pageNumber: number = 0): Observable<NgoOverviewItemPagination> {
        // deep copy needed
        const tempSortingSelection: NgoSortingSelection = {
            value: Utils.retrieveObjectKeyFromDisplayName(sortingSelection.value),
            order: sortingSelection.order,
        };

        if (pageNumber === 0) {
            return this.apiService.get('ngos/filter',
                {filter_selection: encodeURIComponent(JSON.stringify(filterSelection)),
                sorting_selection: encodeURIComponent(JSON.stringify(tempSortingSelection))});
        }
        return this.apiService.get('ngos/filter',
            {filter_selection: encodeURIComponent(JSON.stringify(filterSelection)),
                sorting_selection: encodeURIComponent(JSON.stringify(tempSortingSelection)),
                page: pageNumber});
    }
}
