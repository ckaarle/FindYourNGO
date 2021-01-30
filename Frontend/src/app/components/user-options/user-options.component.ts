import { Component, OnInit, OnDestroy } from '@angular/core';
import {FilterService} from '../../services/filter.service';
import {MatDialog} from '@angular/material/dialog';
import {NgoSortingSelection} from '../../models/ngo';
import {LoginDialogComponent} from '../../screens/login-dialog/login-dialog.component';
import {UserService} from '../../services/user.service';
import {ApiService} from '../../services/api.service';
import {Router} from '@angular/router';

@Component({
  selector: 'user-options',
  templateUrl: './user-options.component.html',
  styleUrls: ['./user-options.component.scss']
})
export class UserOptionsComponent implements OnInit, OnDestroy {

  constructor(private filter: FilterService, public router: Router, public userService: UserService, public apiService: ApiService, public dialog: MatDialog) {
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
  }

  showDetails(): void {
    this.router.navigate(['/detailView', this.userService.ngoid.value]);
  }
}
