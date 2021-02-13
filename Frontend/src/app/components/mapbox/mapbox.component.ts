import {Component, OnInit} from '@angular/core';
import {MapboxService} from '../../services/mapbox.service';
import * as mapboxgl from 'mapbox-gl';
import {environment} from '../../../environments/environment';

@Component({
  selector: 'app-mapbox',
  templateUrl: './mapbox.component.html',
  styleUrls: ['./mapbox.component.scss']
})
export class MapboxComponent implements OnInit {

  // @ts-ignore
  map: mapboxgl.Map;
  style = 'mapbox://styles/mapbox/streets-v11';
  lat = 48.137154;
  lng = 11.576124;
  zoom = 1.5;

  constructor(private mapboxService: MapboxService) {
    // @ts-ignore
    mapboxgl.accessToken = environment.mapbox.accessToken;

    this.mapboxService.getNgoCoordinates().subscribe(data => {
      data.forEach((plot: any) => this.addMarker(plot.coordinates[1], plot.coordinates[0]));

      // this.mapboxService.get('map/links').subscribe(linkData => {
      //   linkData.forEach((link: any) => {
      //     if (link.connected_ngo_id > link.reporter_id) {
      //       this.links[link.id] = {
      //         between: [String(link.connected_ngo_id), String(link.reporter_id)],
      //         tooltip: {content: link.id}
      //       };
      //     }
      //   });
      //   console.log(this.links);
      //   $('.container').trigger('update', [{
      //     newPlots: this.plots,
      //     newLinks: this.links,
      //     animDuration: 1000}]);
      // });
    });
  }

  ngOnInit(): void {
    this.buildMap();
  }

  buildMap(): void {
    this.map = new mapboxgl.Map({container: 'map', style: this.style, zoom: this.zoom, center: [this.lng, this.lat]});
    this.map.addControl(new mapboxgl.NavigationControl());
  }

  addMarker(longitude: number, latitude: number): void {
    const newMarker = new mapboxgl.Marker({
      color: getComputedStyle(document.body).getPropertyValue('--secondary-color')
    }).setLngLat([longitude, latitude]).addTo(this.map);
  }

}
