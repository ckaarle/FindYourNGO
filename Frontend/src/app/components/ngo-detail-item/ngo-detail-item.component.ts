import {Component, ElementRef} from '@angular/core';
import {NgoDetailItem, NgoFilterSelection, NgoSortingSelection} from 'src/app/models/ngo';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../../services/api.service';
import {Utils} from '../../services/utils';
import {BehaviorSubject} from 'rxjs';
import {AbstractControl, FormArray, FormControl, FormGroup} from '@angular/forms';
import {FavouriteService} from '../../services/favourite.service';
import {UserService} from '../../services/user.service';
import {Location} from '@angular/common';
import {MatTabChangeEvent} from '@angular/material/tabs';
import {MediaService} from '../../services/media.service';
import {FilteredNgosCount} from '../../screens/overview-screen/overview-screen.component';


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
  utils = Utils;
  ngoContentContainers: NgoContentContainer[] = [];
  public ngoDetailItem: any | NgoDetailItem;
  public $ngoId = new BehaviorSubject<number>(-1);
  public ngoForm: FormGroup = new FormGroup({});
  public $ngoRelation = new BehaviorSubject<string>('');
  public editMode = false;

  editModeEnabled = true;

  previousPageNumber: null | number = null;

  filter: boolean = false;
  filterSelection: NgoFilterSelection = {};
  totalAmount: FilteredNgosCount = {} as FilteredNgosCount;

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
      public userService: UserService,
      public media: MediaService) {
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
    const totalAmount = this.route.snapshot.paramMap.get('totalAmount');

    if (filterActive != null) {
      this.filter = filterActive.toLowerCase() === 'true';
    }
    if (filterSelection != null) {
      this.filterSelection = JSON.parse(filterSelection);
    }
    if (totalAmount != null) {
      this.totalAmount = JSON.parse(totalAmount);
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
            (Array.isArray(ngoContentContainerTitles[title].values) ?
                ngoContentContainerTitles[title].values.length > 0 :
                ngoContentContainerTitles[title].values !== '' &&
                Object.keys(ngoContentContainerTitles[title].values).length > 0);
      }
    }
    return hasValues;
  }

  titleRowHasValues(titleRow: any): boolean {
    return titleRow && (Array.isArray(titleRow) ? titleRow.length > 0 : titleRow !== '' && Object.keys(titleRow).length > 0);
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
        sortingSelection: JSON.stringify(this.sortingSelection),
        totalAmount: JSON.stringify(this.totalAmount)
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
      for (const ngoTitle of Object.values(ngoContentContainer.values) as any) {
        // @ts-ignore
        if (ngoTitle.displayName === 'Representative') {
            absControl['Edit Representative First Name'] = new FormControl(ngoTitle.values.representativeFirstName);
            absControl['Edit Representative Last Name'] = new FormControl(ngoTitle.values.representativeLastName);
            absControl['Edit Representative Email'] = new FormControl(ngoTitle.values.representativeEmail);
        } else if (ngoTitle.displayName === 'President') {
            absControl['Edit President First Name'] = new FormControl(ngoTitle.values.presidentFirstName);
            absControl['Edit President Last Name'] = new FormControl(ngoTitle.values.presidentLastName);
        } else if (ngoTitle.displayName === 'Address') {
            absControl['Edit Street'] = new FormControl(ngoTitle.values.street);
            absControl['Edit City'] = new FormControl(ngoTitle.values.city);
            absControl['Edit Postcode'] = new FormControl(ngoTitle.values.postcode);
            absControl['Edit Country'] = new FormControl(ngoTitle.values.country);
        } else {
            absControl[`Edit ${ngoTitle.displayName}`] = new FormControl(ngoTitle.values);
        }
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

  trackByFn(index: any, item: any): any {
    return index;
  }

  startEditMode(): void {
    this.editMode = true;
  }

  removeValue(value: any, formFieldKey: string): void {
    const index = this.ngoForm.value[formFieldKey].indexOf(value);
    if (index >= 0) {
      this.ngoForm.value[formFieldKey].splice(index, 1);
    }
  }

  setInputValue(value: string, formFieldKey: string): void {
    if (Array.isArray(this.ngoForm.value[formFieldKey])) {
      if (this.ngoForm.value[formFieldKey].length === 0) {
        this.ngoForm.value[formFieldKey] = [];
      }
      this.ngoForm.value[formFieldKey].push(value);
    }
    return;
  }

  submit(): void {
    this.editMode = false;
    const editedNgo = Utils.retrieveObjectKeyFromDetailItemDisplayName(this.ngoForm.value);
    this.apiService.put('ngoDetailItem/', editedNgo, {id: this.$ngoId.value}).subscribe(
        data => this.refreshNgoDetailItem(this.$ngoId.value.toString()));

  }

  showInformation(): void {
    this.router.navigate(['/about'], {fragment: 'tw-explanation'});
  }

  setEditMode($event: MatTabChangeEvent): void {
    if ($event.index > 0 && this.editMode) {
      this.editMode = false;
    }
    this.editModeEnabled = $event.index === 0;
  }
}
