import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OverviewScreenComponent } from './screens/overview-screen/overview-screen.component';
import { SearchScreenComponent } from './screens/search-screen/search-screen.component';
import { MapScreenComponent } from './screens/map-screen/map-screen.component';
import { FavouritesScreenComponent } from './screens/favourites-screen/favourites-screen.component';
import { NgoOverviewItemComponent } from './components/ngo-overview-item/ngo-overview-item.component';
import { MediaService } from './services/media.service';

import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatTabsModule } from '@angular/material/tabs';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';
import { OverviewService } from './services/overview.service';
import { StarRatingComponent } from './components/star-rating/star-rating.component';


@NgModule({
  imports: [
    CommonModule,
    MatTabsModule,
    MatSidenavModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatExpansionModule,
    MatCardModule,
    FlexLayoutModule
  ],
  declarations: [
    OverviewScreenComponent,
    SearchScreenComponent,
    MapScreenComponent,
    FavouritesScreenComponent,
    NgoOverviewItemComponent,
    StarRatingComponent,
  ],
  exports: [
    MatTabsModule,
    MatSidenavModule,
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatExpansionModule,
    MatCardModule,
  ],
  providers: [
    MediaService,
    OverviewService
  ]
})
export class SharedModule { }
