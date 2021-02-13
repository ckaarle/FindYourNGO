import {Injectable} from '@angular/core';
import {environment} from '../../environments/environment';
import * as mapboxgl from 'mapbox-gl';

@Injectable({
  providedIn: 'root'
})
export class MapboxService {

  // @ts-ignore
  map: mapboxgl.Map;
  style = 'mapbox://styles/mapbox/streets-v11';
  lat = 48.137154;
  lng = 11.576124;
  zoom = 1.5;

  constructor() {
    // @ts-ignore
    mapboxgl.accessToken = environment.mapbox.accessToken;
  }

  buildMap(): void {
    this.map = new mapboxgl.Map({container: 'map', style: this.style, zoom: this.zoom, center: [this.lng, this.lat]});
    this.map.addControl(new mapboxgl.NavigationControl());
  }
}
