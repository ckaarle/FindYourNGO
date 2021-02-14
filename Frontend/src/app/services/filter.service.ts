import {EventEmitter, Injectable} from '@angular/core';
import {NgoFilterOptions, NgoFilterSelection, NgoOverviewItemPagination, NgoSortingSelection} from '../models/ngo';
import {Observable} from 'rxjs';
import {ApiService} from './api.service';
import {Utils} from './utils';
import {Router} from '@angular/router';

@Injectable({
    providedIn: 'root'
})
export class FilterService {
    filterActive: boolean = false;
    selectedFilters: NgoFilterSelection = {} as NgoFilterSelection;
    selectedSorting: NgoSortingSelection = {} as NgoSortingSelection;
    filteredNgoItems: NgoOverviewItemPagination = {} as NgoOverviewItemPagination;
    public selectedFiltersChanged: EventEmitter<NgoFilterSelection> = new EventEmitter<NgoFilterSelection>();
    public selectedSortingChanged: EventEmitter<NgoSortingSelection> = new EventEmitter<NgoSortingSelection>();
    public filteredNgoOverviewItemsChanged: EventEmitter<NgoOverviewItemPagination> = new EventEmitter<NgoOverviewItemPagination>();
    public loadingNgoOverviewItems: EventEmitter<boolean> = new EventEmitter<boolean>();

    constructor(public apiService: ApiService, private router: Router) {
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
            keyToSort: Utils.retrieveObjectKeyFromDisplayName(sortingSelection.keyToSort),
            orderToSort: sortingSelection.orderToSort,
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

    public getAvailableCities(cities: {[index: string]: string[]}, filterSelection: NgoFilterSelection ): string[] {
    let result: string[] = [];
    if (filterSelection.hasOwnProperty('countries')) {
      for (const country of filterSelection.countries) {
        for (const key in cities) {
          if (cities[key][country]) {
            result = result.concat(cities[key][country]);
            break;
          }
        }
      }
    }
    if (filterSelection.hasOwnProperty('cities')) {
      const prevCities = filterSelection.cities;
      for (const prevCity of prevCities) {
        if (!result.includes(prevCity)) {
          const index = prevCities.indexOf(prevCity, 0);
          if (index > -1) {
             prevCities.splice(index, 1);
          }
        }
      }
    }
    return result.filter(str => str != null && str.length !== 0);
  }

  showDetails(ngoId: number): void {
    this.router.navigate(['/detailView', ngoId, {
      currentPage: 1,
      filter: this.filterActive,
      filterSelection: JSON.stringify(this.selectedFilters),
      sortingSelection: JSON.stringify(this.selectedSorting),
    }]);
  }
}
