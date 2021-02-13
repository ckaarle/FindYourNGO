import {Component, OnInit} from '@angular/core';
import {MapboxService} from '../../services/mapbox.service';
import * as mapboxgl from 'mapbox-gl';
import {environment} from '../../../environments/environment';
import * as turf from '@turf/turf';

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

  color = '#fffff';

  constructor(private mapboxService: MapboxService) {
    this.color = getComputedStyle(document.body).getPropertyValue('--secondary-color');

    // @ts-ignore
    mapboxgl.accessToken = environment.mapbox.accessToken;

    this.mapboxService.getNgoCoordinates().subscribe(data => {
      data.forEach((plot: any) => this.addMarker(plot.coordinates[1], plot.coordinates[0]));

      this.mapboxService.getNgoLinks().subscribe(linkData => {
        linkData.forEach((link: any) => {

          // TODO


          if (link.connected_ngo_id > link.reporter_id) {

            this.links[link.id] = {
              between: [String(link.connected_ngo_id), String(link.reporter_id)],
              tooltip: {content: link.id}
            };
          }
        });
      });
    });
  }

  ngOnInit(): void {
    this.buildMap();
    this.addLink(this.lng, this.lat, -73.935242, 40.730610);
  }

  buildMap(): void {
    this.map = new mapboxgl.Map({container: 'map', style: this.style, zoom: this.zoom, center: [this.lng, this.lat]});
    this.map.addControl(new mapboxgl.NavigationControl());
  }

  addMarker(longitude: number, latitude: number): void {
    new mapboxgl.Marker({
      color: this.color
    }).setLngLat([longitude, latitude]).addTo(this.map);
  }

  addLink(lng1: number, lat1: number, lng2: number, lat2: number): void {
    const origin = turf.point([lng1, lat1]);
    const destination = turf.point([lng2, lat2]);

    const curvedLine = turf.greatCircle(origin, destination, {properties: {name: 'Name of this line'}});

    // A simple line from origin to destination.
    const route = {
      type: 'FeatureCollection',
      features: [
        {
          type: 'Feature',
          geometry: {
            type: 'LineString',
            coordinates: [origin, destination]
          }
        }
      ]
    };

    // @ts-ignore
    route.features[0].geometry.coordinates = curvedLine.geometry.coordinates;


    this.map.on('load', () => {
      this.map.addSource('route', {
        type: 'geojson',
        // @ts-ignore
        data: route
      });

      this.map.addLayer({
        id: 'route',
        source: 'route',
        type: 'line',
        paint: {
          'line-width': 3,
          'line-color': this.color,
        }
      });

  });
  }
}
