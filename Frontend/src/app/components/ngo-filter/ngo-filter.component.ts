import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NgoFilterOptions, NgoOverviewItem, NgoFilterSelection } from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';

@Component({
  selector: 'ngo-filter',
  templateUrl: './ngo-filter.component.html',
  styleUrls: ['./ngo-filter.component.scss']
})
export class NgoFilterComponent implements OnInit {
  @Input() filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  @Output() openFilterSelectionDrawer: EventEmitter<boolean> = new EventEmitter<boolean>();

  filterUpdated: boolean = false;
  filterSelection: NgoFilterSelection = {} as NgoFilterSelection;

  constructor(private filter: FilterService) { }

  ngOnInit(): void {
    this.subscribeFilterSelection();
  }

  subscribeFilterSelection() {
    this.filter
      .selectedFiltersChanged
      .subscribe(data => {
        this.filterSelection = data;
      });
  }

  isStringArray(value: any): boolean {
    return Array.isArray(value);
  }

  isBoolean(value: any): boolean {
    return typeof value === 'boolean';
  }

  checkIfFilterSet(key: string) {
    return key in this.filterSelection;
  }

  addValue(keyOption: any, value: any, multiple: boolean = false) {
    if (this.filterSelection[keyOption] && multiple) {
      this.filterSelection[keyOption].push(value);
    } else {
      if (multiple) {
        this.filterSelection[keyOption] = [value];
      } else {
        this.filterSelection[keyOption] = value;
      }
    }
    this.filterUpdated = true;
  }

  openFilterSelection() {
    this.openFilterSelectionDrawer.emit(true)
  }

  applyFilter() {
    this.filter.applyFilter(this.filterSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
      this.filter.editSelectedFilters(this.filterSelection);
      this.filterUpdated = false;
    });
  }
}
