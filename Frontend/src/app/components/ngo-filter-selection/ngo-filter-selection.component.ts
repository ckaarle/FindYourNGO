import { Component, EventEmitter, Input, Output } from '@angular/core';
import {NgoFilterOptions, NgoFilterSelection, NgoSortingSelection} from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';
import {MatMenu} from '@angular/material/menu';

@Component({
  selector: 'ngo-filter-selection',
  templateUrl: './ngo-filter-selection.component.html',
  styleUrls: ['./ngo-filter-selection.component.scss']
})
export class NgoFilterSelectionComponent {
  @Input() filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  @Input() filterSelection: NgoFilterSelection = {} as NgoFilterSelection;
  @Input() sortingOptions: string[] = [];
  @Input() sortingSelection: NgoSortingSelection = {} as NgoSortingSelection;

  credibility: string[] = ['trustworthiness', 'fromCredibleDataSource', 'hasAccreditations'];
  hqDetails: string[] = ['countries', 'cities', 'workingLanguages', 'contactOptionPresent'];
  ngoDetails: string[] = ['branches', 'topics', 'typeOfOrganization', 'funding'];

  constructor(private filter: FilterService) { }

  addValue(keyOption: any, value: any): void {
    this.filterSelection[keyOption] = value;
  }

  changeSorting(sortingOption: any, sortingOrder?: string): void {
    this.sortingSelection.keyToSort = sortingOption;
    if (sortingOrder) {
      this.sortingSelection.orderToSort = sortingOrder;
    }
  }

  applyFilter(): void {
    this.filter.editSelectedFilters(this.filterSelection, this.sortingSelection);
    this.filter.applyFilter(this.filterSelection, this.sortingSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
    });
  }

  getAvailableCities(): string[] {
    return this.filter.getAvailableCities(this.filterOptions.cities.values, this.filterSelection);
  }
}
