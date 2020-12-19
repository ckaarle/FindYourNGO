import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OverviewScreenComponent } from './screens/overview-screen/overview-screen.component';
import { SearchScreenComponent } from './screens/search-screen/search-screen.component';
import { MapScreenComponent } from './screens/map-screen/map-screen.component';
import { FavouritesScreenComponent } from './screens/favourites-screen/favourites-screen.component';
import { NgoOverviewItemComponent } from './components/ngo-overview-item/ngo-overview-item.component';
import { NgoDetailItemComponent } from './components/ngo-detail-item/ngo-detail-item.component';
import { MediaService } from './services/media.service';

import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatTabsModule } from '@angular/material/tabs';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from "@angular/material/dialog";

import { FlexLayoutModule } from '@angular/flex-layout';
import { StarRatingComponent } from './components/star-rating/star-rating.component';
import { ValueTransformerPipe } from './pipes/value-transformer.pipe';
import { ReactiveFormsModule } from '@angular/forms';
import { MatSelectModule } from "@angular/material/select";
import { MatInputModule } from "@angular/material/input";
import { OverlayService } from './services/overlay.service';

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
        FlexLayoutModule,
        ReactiveFormsModule,
        MatSelectModule,
        MatInputModule,
        MatDialogModule
    ],
  declarations: [
    OverviewScreenComponent,
    SearchScreenComponent,
    MapScreenComponent,
    FavouritesScreenComponent,
    NgoOverviewItemComponent,
    StarRatingComponent,
    NgoDetailItemComponent,
    ValueTransformerPipe
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
    MatDialogModule
  ],
  providers: [
    MediaService,
    OverlayService,
    ValueTransformerPipe
  ]
})
export class SharedModule { }
