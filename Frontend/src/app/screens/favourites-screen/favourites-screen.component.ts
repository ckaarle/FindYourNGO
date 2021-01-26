import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {MatDialog} from '@angular/material/dialog';
import {LoginDialogComponent} from '../login-dialog/login-dialog.component';
import {FavouriteService} from '../../services/favourite.service';
import {NgoFavourite, NgoOverviewItem} from '../../models/ngo';
import {Router} from '@angular/router';

@Component({
  selector: 'app-favourites-screen',
  templateUrl: './favourites-screen.component.html',
  styleUrls: ['./favourites-screen.component.scss']
})
export class FavouritesScreenComponent implements OnInit {

  overviewItems: NgoOverviewItem[] = [];
  userFavourites: number[] = [];

  userLoggedIn: boolean = false;

  constructor(
      private apiService: ApiService,
      private dialog: MatDialog,
      private favouriteService: FavouriteService,
      private router: Router,
      ) {
  }

  ngOnInit(): void {
    this.userLoggedIn = this.apiService.userid.getValue() >= 0;
    this.apiService.userid.subscribe((id: number) => {
      this.userLoggedIn = id >= 0;

      if (this.userLoggedIn) {
        this.load_favourite_ngos();
      }
    });

    if (!this.userLoggedIn) {
      this.dialog.open(LoginDialogComponent);
    } else {
      this.load_favourite_ngos();
    }

    this.favouriteService.favouriteChanged.subscribe((ngoFavourite: NgoFavourite) => {
      let index = -1;

      for (let i = 0; i < this.overviewItems.length; i++) {
        const ngo = this.overviewItems[i];
        if (ngo.id === ngoFavourite.ngoId && !ngoFavourite.favourite) {
          index = i;
          break;
        }
      }

      if (index >= 0) {
        this.overviewItems.splice(index, 1);
      }
    });
  }

  private load_favourite_ngos(): void {
    this.favouriteService.getUserFavourites().subscribe(ngos => {
      this.favouriteService.getUserFavourites().subscribe(
          result => {
            this.userFavourites = [];

            for (const ngoOverViewItem of result){
              this.userFavourites.push(ngoOverViewItem.id);
            }
          });
      this.overviewItems = ngos;
    });
  }

  showDetail(overviewItem: NgoOverviewItem): void {
    this.router.navigate(['/detailView', overviewItem.id, {
      pageBeforePaginated: false,
    }]);
  }
}
