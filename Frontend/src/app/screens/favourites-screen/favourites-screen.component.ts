import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {MatDialog} from '@angular/material/dialog';
import {LoginDialogComponent} from '../login-dialog/login-dialog.component';

@Component({
  selector: 'app-favourites-screen',
  templateUrl: './favourites-screen.component.html',
  styleUrls: ['./favourites-screen.component.scss']
})
export class FavouritesScreenComponent implements OnInit {

  userLoggedIn: boolean = false;

  constructor(private apiService: ApiService, private dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.userLoggedIn = this.apiService.userid.getValue();
    this.apiService.userid.subscribe((id: string) => {
      this.userLoggedIn = id !== '';
    });

    if (!this.userLoggedIn) {
      this.dialog.open(LoginDialogComponent);
    }
  }

}
