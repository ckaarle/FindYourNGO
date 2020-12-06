import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common'

import { FavouritesScreenComponent } from './screens/favourites-screen/favourites-screen.component';
import { MapScreenComponent } from './screens/map-screen/map-screen.component';
import { OverviewScreenComponent } from './screens/overview-screen/overview-screen.component';
import { SearchScreenComponent } from './screens/search-screen/search-screen.component';

const routes: Routes = [
  { path: '', redirectTo: '/overview', pathMatch: 'full'},
  { path: 'overview', component: OverviewScreenComponent, data: {title: 'Overview'} },
  { path: 'search', component: SearchScreenComponent, data: {title: 'Search'} },
  { path: 'favourites', component: FavouritesScreenComponent, data: {title: 'Favourites'} },
  { path: 'map', component: MapScreenComponent, data: {title: 'Map'} }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
    CommonModule
  ],
  exports: [
    RouterModule
  ],
  declarations: []
})

export class AppRoutingModule { }
