import { Component, EventEmitter, Input, Output} from '@angular/core';
import {NgoFilterOptions, NgoFilterSelection, NgoSortingSelection} from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';

@Component({
  selector: 'ngo-filter',
  templateUrl: './ngo-filter.component.html',
  styleUrls: ['./ngo-filter.component.scss']
})
export class NgoFilterComponent {
  @Input() filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  @Input() filterSelection: NgoFilterSelection = {} as NgoFilterSelection;
  @Input() sortingOptions: string[] = [];
  @Input() sortingSelection: NgoSortingSelection = {value: 'Name', order: 'asc'};
  @Output() openFilterSelectionDrawer: EventEmitter<boolean> = new EventEmitter<boolean>();
  filterUpdated: boolean = false;

  constructor(private filter: FilterService) { }

  checkIfFilterSet(key: string): boolean {
    return this.filterSelection.hasOwnProperty(key);
  }

  addValue(keyOption: any, value: any): void {
    this.filterSelection[keyOption] = value;
    this.filterUpdated = true;
  }

  changeSorting(sortingOption: any, sortingOrder?: string): void {
    this.sortingSelection.value = sortingOption;
    if (sortingOrder) {
      this.sortingSelection.order = sortingOrder;
    }
    this.applyFilter();
  }

  removeValue(keyOption: any): void {
    delete this.filterSelection[keyOption];
    this.applyFilter();
  }

  openFilterSelection(): void {
    this.openFilterSelectionDrawer.emit(true);
  }

  applyFilter(): void {
    this.filter.editSelectedFilters(this.filterSelection, this.sortingSelection);
    this.filter.applyFilter(this.filterSelection, this.sortingSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
      this.filterUpdated = false;
    });
  }
}
