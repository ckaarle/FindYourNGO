import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {OverviewScreenComponent} from './screens/overview-screen/overview-screen.component';
import {SearchScreenComponent} from './screens/search-screen/search-screen.component';
import {MapScreenComponent} from './screens/map-screen/map-screen.component';
import {FavouritesScreenComponent} from './screens/favourites-screen/favourites-screen.component';
import {LoginDialogComponent} from './screens/login-dialog/login-dialog.component';
import {NgoOverviewItemComponent} from './components/ngo-overview-item/ngo-overview-item.component';
import {NgoDetailItemComponent} from './components/ngo-detail-item/ngo-detail-item.component';
import {NgoFilterComponent} from './components/ngo-filter/ngo-filter.component';
import {NgoFilterSelectionComponent} from './components/ngo-filter-selection/ngo-filter-selection.component';
import {NgoConnectionComponent} from './components/ngo-connection/ngo-connection.component';
import {NgoEventComponent} from './components/ngo-event/ngo-event.component';
import {MediaService} from './services/media.service';

import {MatButtonModule} from '@angular/material/button';
import {MatSidenavModule} from '@angular/material/sidenav';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatListModule} from '@angular/material/list';
import {MatTabsModule} from '@angular/material/tabs';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatIconModule} from '@angular/material/icon';
import {MatCardModule} from '@angular/material/card';
import {MatDialogModule} from '@angular/material/dialog';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatMenuModule} from '@angular/material/menu';

import {MatChipsModule} from '@angular/material/chips';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatSelectModule} from '@angular/material/select';
import {MatCheckboxModule} from '@angular/material/checkbox';
import {MatInputModule} from '@angular/material/input';
import {MatProgressBarModule} from '@angular/material/progress-bar';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {FlexLayoutModule} from '@angular/flex-layout';

import {FullCalendarModule} from '@fullcalendar/angular'; // the main connector. must go first
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';

import {StarRatingComponent} from './components/star-rating/star-rating.component';
import {ValueTransformerPipe} from './pipes/value-transformer.pipe';
import {TypeEvaluatorPipe} from './pipes/type-evaluator.pipe';
import {OverlayService} from './services/overlay.service';
import {FilterService} from './services/filter.service';
import {PaginationComponent} from './components/pagination/pagination.component';
import {NgoRatingComponent} from './components/ngo-rating/ngo-rating.component';
import {NgoTwRatingComponent} from './components/ngo-tw-rating/ngo-tw-rating.component';
import {NgoRatingTableComponent} from './components/ngo-rating-table/ngo-rating-table.component';
import {NgoReviewComponent} from './components/ngo-review/ngo-review.component';
import {NgoReviewsComponent} from './components/ngo-reviews/ngo-reviews.component';
import {NgoNewReviewComponent} from './components/ngo-new-review/ngo-new-review.component';
import {AppRoutingModule} from './app-routing.module';
import {CalendarComponent} from './components/calendar/calendar.component';
import {NgoEventOverviewComponent} from './components/ngo-event-overview/ngo-event-overview.component';
import {UserOptionsComponent} from './components/user-options/user-options.component';

FullCalendarModule.registerPlugins([ // register FullCalendar plugins
  dayGridPlugin,
  interactionPlugin,
  timeGridPlugin,
  listPlugin
]);

@NgModule({
  imports: [
    CommonModule,
    MatTabsModule,
    MatSidenavModule,
    MatToolbarModule,
    MatMenuModule,
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
    MatProgressBarModule,
    FormsModule,
    ReactiveFormsModule,
    FlexLayoutModule,
    AppRoutingModule,
    MatAutocompleteModule,
    FullCalendarModule
  ],
  declarations: [
    OverviewScreenComponent,
    PaginationComponent,
    SearchScreenComponent,
    MapScreenComponent,
    LoginDialogComponent,
    FavouritesScreenComponent,
    NgoOverviewItemComponent,
    StarRatingComponent,
    NgoFilterComponent,
    NgoFilterSelectionComponent,
    NgoDetailItemComponent,
    NgoConnectionComponent,
    NgoEventComponent,
    ValueTransformerPipe,
    TypeEvaluatorPipe,
    NgoRatingComponent,
    NgoTwRatingComponent,
    NgoRatingTableComponent,
    NgoReviewComponent,
    NgoReviewsComponent,
    NgoNewReviewComponent,
    CalendarComponent,
    NgoEventOverviewComponent,
    UserOptionsComponent,
  ],
  exports: [
    MatTabsModule,
    MatSidenavModule,
    MatToolbarModule,
    MatMenuModule,
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
    MatProgressBarModule,
    FormsModule,
    ReactiveFormsModule,
    UserOptionsComponent
  ],
  providers: [
    MediaService,
    OverlayService,
    FilterService,
    ValueTransformerPipe,
    TypeEvaluatorPipe
  ]
})
export class SharedModule {
}
