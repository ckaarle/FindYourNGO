import {Component, Input, OnInit} from '@angular/core';
import {NgoFavourite, NgoOverviewItem} from '../../models/ngo';
import {FavouriteService} from '../../services/favourite.service';
import {UserService} from '../../services/user.service';

@Component({
  selector: 'ngo-overview-item',
  templateUrl: './ngo-overview-item.component.html',
  styleUrls: ['./ngo-overview-item.component.scss']
})
export class NgoOverviewItemComponent implements OnInit {
  @Input() ngoOverviewItem: NgoOverviewItem = {} as NgoOverviewItem;
  @Input() editableRating: boolean = false;

  @Input() userFavourite: boolean = true;

  constructor(private favouriteService: FavouriteService, public userService: UserService) {
  }

  ngOnInit(): void {
  }


  toggleFavouriteStatus(event: MouseEvent): void {
    event.stopPropagation();

    this.favouriteService.setUserFavourite(!this.userFavourite, this.ngoOverviewItem.id).subscribe(newStatus => {
      this.userFavourite = newStatus;

      const favourite: NgoFavourite = {
        ngoId: this.ngoOverviewItem.id,
        favourite: newStatus
      };
      this.favouriteService.emit(favourite);
    });
  }
}
