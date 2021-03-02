import { Component, OnInit, OnDestroy } from '@angular/core';
import { SocialAuthService, SocialUser } from 'angularx-social-login';
import { ApiService } from '../../services/api.service';
import { Names } from '../../models/ngo';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { Observable } from 'rxjs';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { map, startWith } from 'rxjs/operators';
import { MatDialogRef } from '@angular/material/dialog';
import {UserService} from '../../services/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {Router} from '@angular/router';
import {LoginService} from '../../services/login.service';

@Component({
  selector: 'app-login-dialog',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.scss']
})
export class LoginDialogComponent implements OnInit, OnDestroy {

  user?: SocialUser;
  isNgo: boolean;
  query: any;
  names: string[] = [];
  // @ts-ignore
  $names: Observable<string[]> | undefined;
  ngoControl = new FormControl();
  status = '';
  userForm = new FormGroup({
    username: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(public dialogRef: MatDialogRef<LoginDialogComponent>, private authService: SocialAuthService,
              private apiService: ApiService, private userService: UserService, private snackBar: MatSnackBar,
              private router: Router, private loginService: LoginService) {
    this.isNgo = false;

    this.apiService.get('names').subscribe((data: Names) =>
      this.$names = this.ngoControl.valueChanges.pipe(startWith(''),
          map(value => data.names.filter(name => name.toLowerCase().includes(value.toLowerCase())))));

    this.authService.authState.subscribe((user) => {
      this.updateQuery();
      this.user = user;
      this.loginService.trySocialLogin(this.query, this.user?.authToken);
    });

    this.userService.user.subscribe((user: SocialUser) => {
      this.user = user;
    });

    this.userService.userid.subscribe((id: number) => {
     if (id !== -1) {  // The dialog is automatically closed if a user is signed in
        this.dialogRef.close();
      }
    });
  }

  ngOnInit(): void {
    this.authService.authState.subscribe((user) => {
      this.userService.user.next(user);
    });

    this.userService.$lastErrorMessage.subscribe(error => this.showUserLoginFeedback(error));
  }

  signInWithGoogle(): void {
    this.loginService.googleLogin();
  }

  signInWithFB(): void {
    this.loginService.facebookLogin();
  }

  signOut(): void {
    this.loginService.signOut(this.user);
    this.user = undefined;
  }

  submit(): void {
    if (this.status === 'register') {
      this.updateQuery();
      this.userService.register(this.userForm.value, this.query);
    }
    if (this.status === 'login') {
      this.userService.login(this.userForm.value);
    }
    this.signOut();
  }

  checkNgo($event: MatCheckboxChange): void {
    this.isNgo = !this.isNgo;
  }

  updateQuery(): void {
    if (!this.isNgo) {
      this.query = null;
    }
    else {
      this.query = {ngo_name: this.ngoControl.value};
    }
  }

  updateForm(status: string): void {
    if (status === this.status) {
      this.status = '';
    }
    else {
      this.status = status;
    }
  }

  private showUserLoginFeedback(error: any): void {
    if (!error || error.error === '') {
      return;
    }

    let userMessage = 'Error: ' + error.error;

    if (error.ngo_account_confirmed) {
      userMessage += ' The representative of your NGO should have received an email with further instructions.';
    }

    this.snackBar.open(userMessage, '', {
      duration: 3000,
      panelClass: ['login-snackbar']
    });
  }

  registerNewNgo($event: MouseEvent): void {
    $event.stopPropagation();
    this.dialogRef.close();
    this.router.navigate(['registerNgo']);
  }

  ngOnDestroy(): void {
    this.signOut();
  }
}
