import {Component, OnInit} from '@angular/core';
import * as $ from 'jquery';
import 'jquery-mapael';
import 'jquery-mapael/js/maps/world_countries.js';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'app-map-screen',
  templateUrl: './map-screen.component.html',
  styleUrls: ['./map-screen.component.scss']
})
export class MapScreenComponent implements OnInit {

  private plots = {fyn: {
    latitude: 48.13,
    longitude: 11.58,
    tooltip: {content: 'FIND YOUR NGO HQ'}
  }};

  private links = {};

  constructor(private apiService: ApiService) {
    this.apiService.get('map/plots').subscribe(data => {
      data.forEach((plot: any) => this.plots[plot.id] = {
        latitude: plot.coordinates[0],
        longitude: plot.coordinates[1],
        tooltip: {content: plot.name},
      });
      this.apiService.get('map/links').subscribe(linkData => {
        linkData.forEach((link: any) => {
          if (link.connected_ngo_id > link.reporter_id) {
            this.links[link.id] = {
              between: [String(link.connected_ngo_id), String(link.reporter_id)],
              tooltip: {content: link.id}
            };
          }
        });
        console.log(this.links);
        $('.container').trigger('update', [{
          newPlots: this.plots,
          newLinks: this.links,
          animDuration: 1000}]);
      });
    });
  }

  ngOnInit(): void {
    $('.container').mapael({
      map: {
        name: 'world_countries',
        defaultArea: {
          attrs: {
            fill: '#f4f4e8',
            stroke: '#ced8d0'
          }
        },
        defaultLink: {
          factor: -0.3,
          stroke: '#a4e100',
          'stroke-width': 2,
          opacity: 0.6,
          attrsHover: {
            stroke: '#a4e100'
          }
        },
        defaultPlot: {
          size: 3,
          text: {
            attrs: {
              fill: '#000'
            },
            attrsHover: {
              fill: '#000'
            }
          }
        }
      },
      plots: this.plots,
      links: this.links,
    });
  }
}
