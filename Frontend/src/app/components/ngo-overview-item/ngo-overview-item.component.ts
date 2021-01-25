import {Component, Input, OnInit} from '@angular/core';
import {NgoOverviewItem} from '../../models/ngo';
import {ApiService} from '../../services/api.service';
import {FavouriteService} from '../../services/favourite.service';

@Component({
  selector: 'ngo-overview-item',
  templateUrl: './ngo-overview-item.component.html',
  styleUrls: ['./ngo-overview-item.component.scss']
})
export class NgoOverviewItemComponent implements OnInit {
  @Input() ngoOverviewItem: NgoOverviewItem = {} as NgoOverviewItem;
  @Input() editableRating: boolean = false;

  @Input() userFavourite: boolean = true;

  constructor(public apiService: ApiService, private favouriteService: FavouriteService) {
  }

  ngOnInit(): void {
  }

  toggleFavouriteStatus(event: MouseEvent): void {
    event.stopPropagation();
    this.favouriteService.setUserFavourite(!this.userFavourite, this.ngoOverviewItem.id).subscribe(newStatus => {
      this.userFavourite = newStatus;
    });
  }
}
