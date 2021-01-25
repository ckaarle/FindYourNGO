import {Component, OnInit} from '@angular/core';
import {NgoDetailItem, NgoFilterSelection} from 'src/app/models/ngo';
import {ActivatedRoute, Router} from '@angular/router';
import {ApiService} from '../../services/api.service';
import {Utils} from '../../services/utils';
import {FavouriteService} from '../../services/favourite.service';

export interface NgoContentContainer {
  icon: string;
  values: any;
}

@Component({
  selector: 'ngo-detail-item',
  templateUrl: './ngo-detail-item.component.html',
  styleUrls: ['./ngo-detail-item.component.scss']
})
export class NgoDetailItemComponent implements OnInit {
  ngoContentContainers: NgoContentContainer[] = [];
  public ngoDetailItem: any | NgoDetailItem;

  previousPageNumber: null | number = null;

  filter: boolean = false;
  filterSelection: NgoFilterSelection = {};

  userFavourite: boolean = true;

  constructor(private route: ActivatedRoute, public apiService: ApiService, private router: Router, private favouriteService: FavouriteService) {
    let id = this.route.snapshot.paramMap.get('id');
    this.apiService.get('ngoDetailItem', {id: id}).subscribe(data => {
      this.ngoDetailItem = data;
      this.ngoDetailItem = Utils.mapDataToNgoDetailItem(this.ngoDetailItem);
      this.generateContentContainers();
    });

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

    // @ts-ignore
    this.favouriteService.isUserFavourite(id).subscribe(result => {
      this.userFavourite = result;
    });
  }

  ngOnInit(): void {
  }

  containerHasValues(ngoContentContainer: NgoContentContainer): boolean {
    let hasValues = false;
    const ngoContentContainerTitles = ngoContentContainer.values;
    for (const title of Object.keys(ngoContentContainerTitles)) {
      if (hasValues) {
        break;
      } else {
        hasValues = ngoContentContainerTitles[title].values &&
            (ngoContentContainerTitles[title].values != '' || ngoContentContainerTitles[title].values.length > 0);
      }
    }
    return hasValues;
  }

  titleRowHasValues(titleRow: any): boolean {
    return titleRow && (titleRow != '' || titleRow.length > 0);
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
    this.router.navigate(['/overview', {
      startPage: this.previousPageNumber,
      filter: this.filter,
      filterSelection: JSON.stringify(this.filterSelection)
    }]);
  }

  toggleFavouriteStatus(): void {
    this.favouriteService.setUserFavourite(!this.userFavourite, this.ngoDetailItem.id).subscribe(newStatus => {
      this.userFavourite = newStatus;
    });
  }
}
