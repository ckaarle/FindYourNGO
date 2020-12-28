import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {OverviewScreenComponent} from './screens/overview-screen/overview-screen.component';
import {SearchScreenComponent} from './screens/search-screen/search-screen.component';
import {MapScreenComponent} from './screens/map-screen/map-screen.component';
import {FavouritesScreenComponent} from './screens/favourites-screen/favourites-screen.component';
import {LoginScreenComponent} from './screens/login-screen/login-screen.component';
import {NgoOverviewItemComponent} from './components/ngo-overview-item/ngo-overview-item.component';
import { NgoDetailItemComponent } from './components/ngo-detail-item/ngo-detail-item.component';
import {NgoFilterComponent} from './components/ngo-filter/ngo-filter.component';
import {NgoFilterSelectionComponent} from './components/ngo-filter-selection/ngo-filter-selection.component';
import { MediaService } from './services/media.service';

import {MatButtonModule} from '@angular/material/button';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatListModule} from '@angular/material/list';
import {MatTabsModule} from '@angular/material/tabs';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatCardModule} from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';

import {MatChipsModule} from '@angular/material/chips';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatInputModule} from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { FlexLayoutModule } from '@angular/flex-layout';

import {StarRatingComponent} from './components/star-rating/star-rating.component';
import {ValueTransformerPipe} from './pipes/value-transformer.pipe';
import {TypeEvaluatorPipe} from './pipes/type-evaluator.pipe';
import { OverlayService } from './services/overlay.service';
import {OverviewService} from './services/overview.service';
import {FilterService} from './services/filter.service';
import {PaginationComponent} from './components/pagination/pagination.component';

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
    MatChipsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatCheckboxModule,
    MatInputModule,
    MatDialogModule,
    MatProgressSpinnerModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule
  ],
  declarations: [
    OverviewScreenComponent,
    PaginationComponent,
    SearchScreenComponent,
    MapScreenComponent,
    LoginScreenComponent,
    FavouritesScreenComponent,
    NgoOverviewItemComponent,
    StarRatingComponent,
    NgoFilterComponent,
    NgoFilterSelectionComponent,
    NgoDetailItemComponent,
    ValueTransformerPipe,
    TypeEvaluatorPipe
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
    MatChipsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatSelectModule,
    MatCheckboxModule,
    MatInputModule,
    MatProgressSpinnerModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    MediaService,
    OverviewService,
    OverlayService,
    FilterService,
    ValueTransformerPipe,
    TypeEvaluatorPipe
  ]
})
export class SharedModule {
}
