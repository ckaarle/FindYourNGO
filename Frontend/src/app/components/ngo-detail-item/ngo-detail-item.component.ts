import {Component} from '@angular/core';
import {NgoDetailItem, NgoFilterSelection, NgoSortingSelection} from 'src/app/models/ngo';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../../services/api.service';
import {Utils} from '../../services/utils';
import {BehaviorSubject} from 'rxjs';
import {AbstractControl, FormControl, FormGroup} from '@angular/forms';
import {FavouriteService} from '../../services/favourite.service';
import {UserService} from '../../services/user.service';
import {Location} from '@angular/common';

export interface NgoContentContainer {
  icon: string;
  values: any;
}

@Component({
  selector: 'ngo-detail-item',
  templateUrl: './ngo-detail-item.component.html',
  styleUrls: ['./ngo-detail-item.component.scss']
})
export class NgoDetailItemComponent {
  ngoContentContainers: NgoContentContainer[] = [];
  public ngoDetailItem: any | NgoDetailItem;
  public $ngoId = new BehaviorSubject<number>(-1);
  public ngoForm: FormGroup = new FormGroup({});
  public $ngoRelation = new BehaviorSubject<string>('');
  public editMode = false;

  previousPageNumber: null | number = null;

  filter: boolean = false;
  filterSelection: NgoFilterSelection = {};

  // @ts-ignore
  sortingSelection: NgoSortingSelection = {};

  userFavourite: boolean = true;

  pageBeforePaginated: boolean = true;

  constructor(
      private route: ActivatedRoute,
      public apiService: ApiService,
      private router: Router,
      private favouriteService: FavouriteService,
      private location: Location,
      public userService: UserService
      ) {
    const id = this.route.snapshot.paramMap.get('id');
    this.$ngoId.next(Number(id));
    this.apiService.get(`connections/${id}`).subscribe(data => this.$ngoRelation.next(data.type));
    // @ts-ignore
    this.refreshNgoDetailItem(id);

    const pageBefore = this.route.snapshot.paramMap.get('currentPage');
    if (pageBefore != null) {
      this.previousPageNumber = +pageBefore;
    }

    const filterActive = this.route.snapshot.paramMap.get('filter');
    const filterSelection = this.route.snapshot.paramMap.get('filterSelection');

    if (filterActive != null) {
      this.filter = filterActive.toLowerCase() === 'true';
    }
    if (filterSelection != null) {
      this.filterSelection = JSON.parse(filterSelection);
    }

    const sortingSelection = this.route.snapshot.paramMap.get('sortingSelection');

    if (sortingSelection != null) {
      this.sortingSelection = JSON.parse(sortingSelection);
    }

    const pageBeforePaginated = this.route.snapshot.paramMap.get('pageBeforePaginated');
    if (pageBeforePaginated != null) {
      this.pageBeforePaginated = pageBeforePaginated.toLowerCase() === 'true';
    }

    // @ts-ignore
    this.favouriteService.isUserFavourite(id).subscribe(result => {
      this.userFavourite = result;
    });
  }

  refreshNgoDetailItem(id: string): void {
    this.apiService.get('ngoDetailItem', {id}).subscribe(data => {
      this.ngoDetailItem = data;
      this.ngoDetailItem = Utils.mapDataToNgoDetailItem(this.ngoDetailItem);
      this.generateContentContainers();
      this.ngoForm = new FormGroup(this.generateFormControls());
    });
  }

  containerHasValues(ngoContentContainer: NgoContentContainer): boolean {
    let hasValues = false;
    const ngoContentContainerTitles = ngoContentContainer.values;
    for (const title of Object.keys(ngoContentContainerTitles)) {
      if (hasValues) {
        break;
      } else {
        hasValues = ngoContentContainerTitles[title].values &&
            (ngoContentContainerTitles[title].values !== '' || ngoContentContainerTitles[title].values.length > 0);
      }
    }
    return hasValues;
  }

  titleRowHasValues(titleRow: any): boolean {
    return titleRow && (titleRow !== '' || titleRow.length > 0);
  }

  generateContentContainers(): void {
    this.ngoContentContainers = [
      {icon: 'info', values: this.ngoDetailItem.description},
      {icon: 'group_work', values: this.ngoDetailItem.fieldOfActivity},
      {icon: 'query_stats', values: this.ngoDetailItem.stats},
      {icon: 'person', values: this.ngoDetailItem.contact}
    ];
  }

  back(): void {
    if (this.pageBeforePaginated) {
      this.router.navigate(['/overview', {
        startPage: this.previousPageNumber,
        filter: this.filter,
        filterSelection: JSON.stringify(this.filterSelection),
        sortingSelection: JSON.stringify(this.sortingSelection)
      }]);
    }
    else {
      this.location.back();
    }
  }

  toggleFavouriteStatus(): void {
    this.favouriteService.setUserFavourite(!this.userFavourite, this.ngoDetailItem.id).subscribe(newStatus => {
      this.userFavourite = newStatus;
    });
  }

  generateFormControls(): { [key: string]: AbstractControl; } {
    const absControl: { [key: string]: AbstractControl; } = {};
    for (const ngoContentContainer of this.ngoContentContainers) {
      for (const ngoTitle of Object.values(ngoContentContainer.values)) {
        // @ts-ignore
        absControl[ngoTitle.displayName] = new FormControl(ngoTitle.values);
      }
    }
    return absControl;
  }

  updateRelation(): void {
    this.apiService.get(`connections/${this.$ngoId.value}`).subscribe(data => this.$ngoRelation.next(data.type));
  }

  addConnection(): void {
    this.apiService.post('connections/add/', {}, {ngo_id: this.$ngoId.value}).subscribe(
        x => this.updateRelation());
  }

  removeConnection(): void {
    this.apiService.post('connections/remove/', {}, {ngo_id: this.$ngoId.value}).subscribe(
        x => this.updateRelation());
  }

  startEditMode(): void {
    this.editMode = true;
  }

  submit(): void {
    this.editMode = false;
    console.log(this.ngoForm.value);
    this.apiService.put('ngoDetailItem', this.ngoForm.value).subscribe(
        data => this.refreshNgoDetailItem(this.$ngoId.value.toString()));
  }

}
