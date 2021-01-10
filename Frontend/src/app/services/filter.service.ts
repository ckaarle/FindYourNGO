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

    mapDataToObject(data: any): NgoFilterOptions {
        return {
            name: {values: data.name},
            branches: {displayName: 'Branches', values: data.branches, icon: 'account_tree'},
            regions: {values: data.regions},
            topics: {displayName: 'Topics', values: data.topics, icon: 'topic'},
            hasEcosoc: {displayName: 'Accreditations', values: data.hasEcosoc, icon: 'account_balance'},
            isCredible: {displayName: 'Credibility', values: data.isCredible, icon: 'loyalty'},
            countries: {displayName: 'Countries', values: data.countries, icon: 'flag'},
            cities: {displayName: 'Cities', values: data.cities, icon: 'location_on'},
            contactOptionPresent: {displayName: 'Contactable', values: data.contactOptionPresent, icon: 'how_to_reg'},
            typeOfOrganization: {
                displayName: 'Type of organization',
                values: data.typeOfOrganization,
                icon: 'corporate_fare'
            },
            workingLanguages: {displayName: 'Working languages', values: data.workingLanguages, icon: 'translate'},
            funding: {displayName: 'Funding', values: data.funding, icon: 'attach_money'},
            trustworthiness: {displayName: 'Trustworthiness', values: data.trustworthiness, icon: 'star'}
        };
    }

    applyFilter(filterSelection: NgoFilterSelection, pageNumber: number = 0): Observable<NgoOverviewItemPagination> {
        if (pageNumber === 0) {
            return this.apiService.get('ngos/filter', {filter_selection: encodeURIComponent( JSON.stringify(filterSelection))});
        }
        return this.apiService.get('ngos/filter', {filter_selection: encodeURIComponent( JSON.stringify(filterSelection)), page: pageNumber});
    }
}
