import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from "../../services/filter.service";

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
    this.filter.editSelectedFilters({});
    this.filter.applyFilter({}).subscribe(data => {
        this.filter.displayFilteredNgoItems(data);
    });
  }
}
