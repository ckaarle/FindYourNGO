import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from '../../services/filter.service';
import {NgoSortingSelection} from '../../models/ngo';

@Component({
  selector: 'app-map-screen',
  templateUrl: './map-screen.component.html',
  styleUrls: ['./map-screen.component.scss']
})
export class MapScreenComponent implements OnInit, OnDestroy {

  constructor(private filter: FilterService) { }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    const selectedSorting: NgoSortingSelection = {keyToSort: 'Name', orderToSort: 'asc'};
    this.filter.editSelectedFilters({}, selectedSorting);
    this.filter.applyFilter({}, selectedSorting).subscribe(data => {
        this.filter.displayFilteredNgoItems(data);
    });
  }
}
