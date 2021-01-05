import { Component, Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { LoginDialogComponent } from '../login-dialog/login-dialog.component';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-favourites-screen',
  templateUrl: './favourites-screen.component.html',
  styleUrls: ['./favourites-screen.component.scss']
})
export class FavouritesScreenComponent {

  public photoUrl = '';

  constructor(public apiService: ApiService, public dialog: MatDialog) { }

  openDialog(): void {
    const dialogRef = this.dialog.open(LoginDialogComponent);
    dialogRef.afterClosed().subscribe(result => {
      console.log(result);
      this.photoUrl = result;
    });
  }

  postAllowed(): void {
    this.apiService.post(`test/`, {user_id: this.apiService.userid.value}).subscribe(data => console.log(data));
  }

  postNotAllowed(): void {
    this.apiService.post(`test/`, {user_id: this.apiService.userid.value + '0'}).subscribe(data => console.log(data));
  }
}
