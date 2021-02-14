import {Component, OnInit} from '@angular/core';
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

  constructor(public filter: FilterService, public router: Router, public userService: UserService, public apiService: ApiService, public dialog: MatDialog) {
  }

  ngOnInit(): void {
  }

  openDialog(): void {
    this.dialog.open(LoginDialogComponent);
  }
}
