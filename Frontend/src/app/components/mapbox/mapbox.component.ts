import { Component, OnInit } from '@angular/core';
import {MapboxService} from '../../services/mapbox.service';

@Component({
  selector: 'app-mapbox',
  templateUrl: './mapbox.component.html',
  styleUrls: ['./mapbox.component.scss']
})
export class MapboxComponent implements OnInit {

  constructor(private mapboxService: MapboxService) { }

  ngOnInit(): void {
    this.mapboxService.buildMap();
  }

}
