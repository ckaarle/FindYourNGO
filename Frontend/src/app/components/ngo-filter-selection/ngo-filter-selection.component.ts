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
  @Input() filterSelection: NgoFilterSelection = {} as NgoFilterSelection;
  @Output() closeFilterSelectionDrawer: EventEmitter<boolean> = new EventEmitter<boolean>();

  credibility: string[] = ['trustworthiness', 'isCredible', 'hasEcosoc'];
  hqDetails: string[] = ['cities', 'countries', 'workingLanguages', 'contactOptionPresent'];
  ngoDetails: string[] = ['branches', 'topics', 'typeOfOrganization', 'funding'];

  constructor(private filter: FilterService) { }

  ngOnInit(): void {
  }

  addValue(keyOption: any, value: any): void {
    this.filterSelection[keyOption] = value;
  }

  closeFilterSelection(): void {
    this.closeFilterSelectionDrawer.emit(true);
  }

  applyFilter(): void {
    this.filter.editSelectedFilters(this.filterSelection);
    this.closeFilterSelection();
    this.filter.applyFilter(this.filterSelection).subscribe(data => {
      this.filter.displayFilteredNgoItems(data);
    });
  }
}
