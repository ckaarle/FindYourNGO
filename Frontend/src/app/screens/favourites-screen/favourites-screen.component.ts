import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from "../../services/filter.service";

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
    this.filter.editSelectedFilters({});
    this.filter.applyFilter({}).subscribe(data => {
        this.filter.displayFilteredNgoItems(data);
    });
  }

}
