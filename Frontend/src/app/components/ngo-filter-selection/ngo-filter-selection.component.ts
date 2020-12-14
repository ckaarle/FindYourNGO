import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { NgoFilterOptions, NgoOverviewItem, NgoFilterSelection } from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';

@Component({
  selector: 'ngo-filter-selection',
  templateUrl: './ngo-filter-selection.component.html',
  styleUrls: ['./ngo-filter-selection.component.scss']
})
export class NgoFilterSelectionComponent implements OnInit {
  @Input() filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  @Output() closeFilterSelectionDrawer: EventEmitter<boolean> = new EventEmitter<boolean>();

  filterSelection: NgoFilterSelection = {} as NgoFilterSelection;
  filterOptionsLoaded = false;
  credibility: string[] = ['trustworthiness', 'isCredible', 'hasEcosoc'];
  hqDetails: string[] = ['cities', 'countries', 'workingLanguages', 'contactOptionPresent'];
  ngoDetails: string[] = ['branches', 'topics', 'typeOfOrganization', 'funding'];

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

  getFilterOption(key: string): any {
    return this.filterOptions[key];
  }

  addValue(keyOption: any, value: any, multiple: boolean = false): void {
    if (this.filterSelection[keyOption] && multiple) {
      this.filterSelection[keyOption].push(value);
    } else {
      if (multiple) {
        this.filterSelection[keyOption] = [value];
      } else {
        this.filterSelection[keyOption] = value;
      }
    }
  }

  closeFilterSelection(): void {
    this.closeFilterSelectionDrawer.emit(true);
  }

  applyFilter(): void {
    this.filter.applyFilter(this.filterSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
      this.filter.editSelectedFilters(this.filterSelection);
      this.closeFilterSelection();
    });
  }
}
