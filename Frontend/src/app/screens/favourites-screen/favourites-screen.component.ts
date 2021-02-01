import { Component, OnDestroy, OnInit } from '@angular/core';
import { FilterService } from '../../services/filter.service';
import { NgoSortingSelection } from '../../models/ngo';
import { MatDialog } from '@angular/material/dialog';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-favourites-screen',
  templateUrl: './favourites-screen.component.html',
  styleUrls: ['./favourites-screen.component.scss']
})
export class FavouritesScreenComponent implements OnInit, OnDestroy {

  constructor(private filter: FilterService, public apiService: ApiService, public dialog: MatDialog) { }

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
