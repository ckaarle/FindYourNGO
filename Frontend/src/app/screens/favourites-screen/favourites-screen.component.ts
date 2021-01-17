import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from '../../services/filter.service';
import {NgoSortingSelection} from '../../models/ngo';

@Component({
  selector: 'app-favourites-screen',
  templateUrl: './favourites-screen.component.html',
  styleUrls: ['./favourites-screen.component.scss']
})
export class FavouritesScreenComponent implements OnInit, OnDestroy {

  constructor(private filter: FilterService) { }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    const selectedSorting: NgoSortingSelection = {value: 'Name', order: 'asc'};
    this.filter.editSelectedFilters({}, selectedSorting);
    this.filter.applyFilter({}, selectedSorting).subscribe(data => {
        this.filter.displayFilteredNgoItems(data);
    });
  }

}
