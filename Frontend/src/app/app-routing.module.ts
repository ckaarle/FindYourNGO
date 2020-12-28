import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CommonModule} from '@angular/common';

import {FavouritesScreenComponent} from './screens/favourites-screen/favourites-screen.component';
import {MapScreenComponent} from './screens/map-screen/map-screen.component';
import {OverviewScreenComponent} from './screens/overview-screen/overview-screen.component';
import {SearchScreenComponent} from './screens/search-screen/search-screen.component';
import {LoginScreenComponent} from './screens/login-screen/login-screen.component';

const routes: Routes = [
  {path: '', redirectTo: '/overview', pathMatch: 'full'},
  {path: 'overview', component: OverviewScreenComponent, data: {title: 'Overview'}},
  {path: 'search', component: SearchScreenComponent, data: {title: 'Search'}},
  {path: 'favourites', component: FavouritesScreenComponent, data: {title: 'Favourites'}},
  {path: 'map', component: MapScreenComponent, data: {title: 'Map'}},
  {path: 'login', component: LoginScreenComponent, data: {title: 'Login'}},
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

export class AppRoutingModule {
}
