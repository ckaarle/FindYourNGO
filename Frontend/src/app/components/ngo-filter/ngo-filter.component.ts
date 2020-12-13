import { Component, OnInit } from '@angular/core';
import { NgoFilterOptions } from 'src/app/models/ngo';
import { FilterService } from 'src/app/services/filter.service';

export interface NgoFilterSelection {}

@Component({
  selector: 'ngo-filter',
  templateUrl: './ngo-filter.component.html',
  styleUrls: ['./ngo-filter.component.scss']
})
export class NgoFilterComponent implements OnInit {
  filtersAvailable: boolean = false;
  filterOptions: NgoFilterOptions = {} as NgoFilterOptions;
  filterSelection: NgoFilterSelection = {} as NgoFilterSelection;

  constructor(private filter: FilterService) { }

  ngOnInit(): void {
    this.getFilterOptions();
  }

  getFilterOptions() {
    this.filter.getNgoFilterOptions().subscribe(data => {
      this.filterOptions = data;
      this.filtersAvailable = true;
    })
  }

  isStringArray(value: any): boolean {
    return Array.isArray(value);
  }

  isBoolean(value: any): boolean {
    return typeof value === 'boolean';
  }

  addValue(keyOption: any, value: any, multiple: boolean = false) { //WiP
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

  applyFilter() { //WiP
    console.log("FilterSelection: ", this.filterSelection);
    this.filter.applyFilter(this.filterSelection).subscribe(data => {
      console.log("FilteredNgoItems: ", data); //TODO: display result
    });
  }

}
