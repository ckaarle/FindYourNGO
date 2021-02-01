import { Component, OnInit } from '@angular/core';
import {FilterService} from '../../services/filter.service';
import {MatDialog} from '@angular/material/dialog';
import {LoginDialogComponent} from '../../screens/login-dialog/login-dialog.component';
import {UserService} from '../../services/user.service';
import {ApiService} from '../../services/api.service';
import {Router} from '@angular/router';

@Component({
  selector: 'user-options',
  templateUrl: './user-options.component.html',
  styleUrls: ['./user-options.component.scss']
})
export class UserOptionsComponent implements OnInit {

  constructor(private filter: FilterService, public router: Router, public userService: UserService, public apiService: ApiService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(LoginDialogComponent);
  }

  showDetails(): void {
    this.router.navigate(['/detailView', this.userService.ngoid.value, {
      currentPage: 1,
      filter: this.filter.filterActive,
      filterSelection: JSON.stringify(this.filter.selectedFilters),
      sortingSelection: JSON.stringify(this.filter.selectedSorting),
    }]); // this navigates to detail page and automatically redirects to overview page.. why?
  }
}
