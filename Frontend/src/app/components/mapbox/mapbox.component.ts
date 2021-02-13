import {Component, OnInit} from '@angular/core';
import {MapboxService} from '../../services/mapbox.service';
import * as mapboxgl from 'mapbox-gl';
import {environment} from '../../../environments/environment';
import * as turf from '@turf/turf';
import {NgoCoordinates} from '../../models/ngo';

@Component({
  selector: 'app-mapbox',
  templateUrl: './mapbox.component.html',
  styleUrls: ['./mapbox.component.scss']
})
export class MapboxComponent {

  // TODO cluster instead of marker?
  // TODO only one layer for links (speedup?)

  // @ts-ignore
  map: mapboxgl.Map;
  style = 'mapbox://styles/mapbox/streets-v11';
  lat = 48.137154;
  lng = 11.576124;
  zoom = 1.5;

  color = '#fffff';

  ngos: {[id: number]: NgoCoordinates} = {};

  mapMarkers = [];
  mapSources = [];
  mapLayers = [];

  constructor(private mapboxService: MapboxService) {
    this.color = getComputedStyle(document.body).getPropertyValue('--secondary-color');

    // @ts-ignore
    mapboxgl.accessToken = environment.mapbox.accessToken;

    this.mapboxService.getNgoCoordinates().subscribe(data => {
      data.forEach(
          (plot: any) => {
            const name = plot.name;
            const id = plot.id;
            const longitude = plot.coordinates[1];
            const latitude = plot.coordinates[0];

            this.ngos[id] = {
              id,
              name,
              longitude,
              latitude,
            };

            this.addMarker(longitude, latitude);
          });

      this.mapboxService.getNgoLinks().subscribe(linkData => {
        linkData.forEach((link: any) => {
          if (link.connected_ngo_id > link.reporter_id) {
            const connectedNgoId = link.connected_ngo_id;
            const reporterNgoId = link.reporter_id;

            const coordinatesNgo = this.ngos[connectedNgoId];
            const coordinatesReporter = this.ngos[reporterNgoId];

            this.addLink(coordinatesNgo.longitude, coordinatesNgo.latitude, coordinatesReporter.longitude, coordinatesReporter.latitude,
                coordinatesNgo.name, coordinatesReporter.name);
          }
        });

        this.buildMap();
        this.initialiseMap();
      });
    });
  }

  buildMap(): void {
    this.map = new mapboxgl.Map({container: 'map', style: this.style, zoom: this.zoom, center: [this.lng, this.lat]});
    this.map.addControl(new mapboxgl.NavigationControl());
  }

  addMarker(longitude: number, latitude: number): void {
    // @ts-ignore
    this.mapMarkers.push([longitude, latitude]);
  }

  addLink(lng1: number, lat1: number, lng2: number, lat2: number, name1: string, name2: string): void {
    const origin = turf.point([lng1, lat1]);
    const destination = turf.point([lng2, lat2]);

    const curvedLine = turf.greatCircle(origin, destination, {properties: {name: name1 + ' --- ' + name2}});

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

    const name = name1 + '-' + name2;

    // @ts-ignore
    this.mapSources.push({id: name, data: route});

    // @ts-ignore
    this.mapLayers.push({id: name, source: name});

  }

  private initialiseMap(): void {
    this.map.on('load', () => {
      this.mapSources.forEach((source: any) => {
        this.map.addSource(source.id, {
          type: 'geojson',
          // @ts-ignore
          data: source.data
        });
      });

      this.mapLayers.forEach((layer: any) => {
        this.map.addLayer({
          id: layer.id,
          source: layer.source,
          type: 'line',
          paint: {
            'line-width': 3,
            'line-color': this.color,
          }
        });
      });
    });

    this.mapMarkers.forEach(marker => {
      new mapboxgl.Marker({
        color: this.color
      }).setLngLat(marker).addTo(this.map);
    });
  }
}
