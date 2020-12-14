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

  subscribeFilterSelection(): void {
    this.filter
      .selectedFiltersChanged
      .subscribe((data: NgoFilterSelection) => {
        this.filterSelection = data;
      });
  }

  checkIfFilterSet(key: string): boolean {
    return key in this.filterSelection;
  }

  addValue(keyOption: any, value: any, multiple: boolean = false): void {
    if (this.filterSelection[keyOption] && multiple) {
      this.filterSelection[keyOption].push(value);
      this.filterUpdated = true;
    } else {
      if (multiple) {
        this.filterSelection[keyOption] = [value];
        this.filterUpdated = true;
      } else {
        this.filterSelection[keyOption] = value;
        this.filterUpdated = true;
      }
    }
  }

  removeValue(keyOption: any) {
    delete this.filterSelection[keyOption];
    this.applyFilter();
  }

  openFilterSelection(): void {
    this.openFilterSelectionDrawer.emit(true);
  }

  applyFilter(): void {
    this.filter.editSelectedFilters(this.filterSelection);
    this.filter.applyFilter(this.filterSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
      this.filterUpdated = false;
    });
  }
}
