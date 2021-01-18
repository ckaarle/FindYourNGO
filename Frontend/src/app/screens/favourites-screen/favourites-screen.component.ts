import { Component, OnDestroy, OnInit, Inject } from '@angular/core';
import { FilterService } from '../../services/filter.service';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { LoginDialogComponent } from '../login-dialog/login-dialog.component';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-favourites-screen',
  templateUrl: './favourites-screen.component.html',
  styleUrls: ['./favourites-screen.component.scss']
})
export class FavouritesScreenComponent implements OnInit, OnDestroy {

  public photoUrl = '';

  constructor(private filter: FilterService, public apiService: ApiService, public dialog: MatDialog) { }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    this.filter.editSelectedFilters({});
    this.filter.applyFilter({}).subscribe(data => {
        this.filter.displayFilteredNgoItems(data);
    });
  }

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
