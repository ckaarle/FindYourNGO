import {Component, OnDestroy, OnInit} from '@angular/core';
import {FilterService} from '../../services/filter.service';
import {ApiService} from '../../services/api.service';
import {MatDialog} from '@angular/material/dialog';
import {NgoSortingSelection} from '../../models/ngo';
import {LoginDialogComponent} from '../login-dialog/login-dialog.component';

@Component({
  selector: 'app-user-screen',
  templateUrl: './user-screen.component.html',
  styleUrls: ['./user-screen.component.scss']
})
export class UserScreenComponent implements OnInit, OnDestroy {

  public photoUrl = '';

  constructor(private filter: FilterService, public apiService: ApiService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    const selectedSorting: NgoSortingSelection = {keyToSort: 'Name', orderToSort: 'asc'};
    this.filter.editSelectedFilters({}, selectedSorting);
    this.filter.applyFilter({}, selectedSorting).subscribe(data => {
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
