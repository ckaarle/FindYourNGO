import { Component, EventEmitter, Input, Output} from '@angular/core';
import {NgoFilterOptions, NgoFilterSelection, NgoSortingSelection} from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';
import {FilteredNgosCount} from '../../screens/overview-screen/overview-screen.component';

@Component({
  selector: 'ngo-filter',
  templateUrl: './ngo-filter.component.html',
  styleUrls: ['./ngo-filter.component.scss']
})
export class NgoFilterComponent {
  @Input() filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  @Input() filterSelection: NgoFilterSelection = {} as NgoFilterSelection;
  @Input() sortingOptions: string[] = [];
  @Input() sortingSelection: NgoSortingSelection = {} as NgoSortingSelection;
  @Input() totalAmountOfNgos: FilteredNgosCount = {} as FilteredNgosCount;
  @Output() openFilterSelectionDrawer: EventEmitter<boolean> = new EventEmitter<boolean>();
  filterUpdated: boolean = false;

  constructor(private filter: FilterService) {
  }

  checkIfFilterSet(key: string): boolean {
    return this.filterSelection.hasOwnProperty(key);
  }

  addValue(keyOption: any, value: any): void {
    this.filterSelection[keyOption] = value;
    this.filterUpdated = true;
  }

  changeSorting(sortingOption: any, sortingOrder?: string): void {
    this.sortingSelection.keyToSort = sortingOption;
    if (sortingOrder) {
      this.sortingSelection.orderToSort = sortingOrder;
    }
    this.applyFilter();
  }

  removeValue(keyOption: any): void {
    delete this.filterSelection[keyOption];
    this.applyFilter();
  }

  openFilterSelection(event: MouseEvent): void {
    if (event.buttons === 0 && event.clientX === 0 && event.clientY === 0) {
      // triggered by hitting enter key in the filter selection drawer ...
      return;
    }

    this.openFilterSelectionDrawer.emit(true);
  }

  applyFilter(): void {
    this.filter.editSelectedFilters(this.filterSelection, this.sortingSelection);
    this.filter.applyFilter(this.filterSelection, this.sortingSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
      this.filterUpdated = false;
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
      const prevCities = this.filterSelection.cities;
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
}
