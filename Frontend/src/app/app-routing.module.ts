import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {CommonModule} from '@angular/common';

import {FavouritesScreenComponent} from './screens/favourites-screen/favourites-screen.component';
import {MapScreenComponent} from './screens/map-screen/map-screen.component';
import {OverviewScreenComponent} from './screens/overview-screen/overview-screen.component';
import {SearchScreenComponent} from './screens/search-screen/search-screen.component';
import {NgoNewReviewComponent} from './components/ngo-new-review/ngo-new-review.component';
import {NgoDetailItemComponent} from './components/ngo-detail-item/ngo-detail-item.component';
import {AboutComponent} from './screens/about/about.component';

const routes: Routes = [
  {path: '', redirectTo: '/overview', pathMatch: 'full'},
  {path: 'overview', component: OverviewScreenComponent, data: {title: 'Overview'}},
  {path: 'search', component: SearchScreenComponent, data: {title: 'Search'}},
  {path: 'favourites', component: FavouritesScreenComponent, data: {title: 'Favourites'}},
  {path: 'map', component: MapScreenComponent, data: {title: 'Map'}},
  {path: 'newReview/:ngoId', component: NgoNewReviewComponent},
  {path: 'detailView/:id', component: NgoDetailItemComponent},
  {path: 'about', component: AboutComponent, data: {title: 'About'}}
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {onSameUrlNavigation: 'reload'}),
    CommonModule
  ],
  exports: [
    RouterModule
  ],
  declarations: []
})

export class AppRoutingModule {
}
