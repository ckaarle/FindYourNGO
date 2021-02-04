import { Component, EventEmitter, Input, Output } from '@angular/core';
import {NgoFilterOptions, NgoFilterSelection, NgoSortingSelection} from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';

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
  @Output() closeFilterSelectionDrawer: EventEmitter<boolean> = new EventEmitter<boolean>();

  credibility: string[] = ['trustworthiness', 'isCredible', 'hasEcosoc'];
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

  closeFilterSelection(): void {
    this.closeFilterSelectionDrawer.emit(true);
  }

  applyFilter(): void {
    this.filter.editSelectedFilters(this.filterSelection, this.sortingSelection);
    this.closeFilterSelection();
    this.filter.applyFilter(this.filterSelection, this.sortingSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
    });
  }

  getAvailableCities(): string[] {
    let result: string[] = [];
    const cities = this.filterOptions.cities.values;
    if (this.filterSelection.hasOwnProperty('countries')) {
      for (const country of this.filterSelection.countries) {
        for (const key in cities) {
          if (cities[key][country]) {
            result = result.concat(cities[key][country]);
            break;
          }
        }
      }
    }
    if (this.filterSelection.hasOwnProperty('cities')) {
      for (const prevCity of this.filterSelection.cities) {
        if (!result.includes(prevCity)) {
          this.filterSelection.cities.pop(prevCity);
        }
      }
    }
    return result.filter(str => str != null && str.length !== 0);
  }
}
