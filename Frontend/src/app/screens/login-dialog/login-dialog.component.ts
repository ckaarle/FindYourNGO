import { Component, OnDestroy, OnInit } from '@angular/core';
import { SocialAuthService, SocialUser } from 'angularx-social-login';
import { FacebookLoginProvider, GoogleLoginProvider } from 'angularx-social-login';
import { ApiService } from '../../services/api.service';
import { Names } from '../../models/ngo';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { Observable } from 'rxjs';
import { FormControl, FormGroup } from '@angular/forms';
import { map, startWith } from 'rxjs/operators';
import { MatDialogRef } from '@angular/material/dialog';
import {UserService} from '../../services/user.service';

@Component({
  selector: 'app-login-dialog',
  templateUrl: './login-dialog.component.html',
  styleUrls: ['./login-dialog.component.scss']
})
export class LoginDialogComponent implements OnInit, OnDestroy {

  user?: SocialUser;
  endpoint?: string;
  isNgo: boolean;
  query: any;
  names: string[] = [];
  $names: Observable<string[]> | undefined;
  ngoControl = new FormControl();
  status = '';
  userForm = new FormGroup({
    username: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(public dialogRef: MatDialogRef<LoginDialogComponent>, private authService: SocialAuthService,
              private apiService: ApiService, private userService: UserService) {
    this.isNgo = false;

    this.apiService.get('names').subscribe((data: Names) =>
      this.$names = this.ngoControl.valueChanges.pipe(startWith(''),
          map(value => data.names.filter(name => name.toLowerCase().includes(value.toLowerCase())))));

    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.updateQuery();
      if (this.endpoint) {
        this.userService.socialLogin({token: this.user?.authToken}, this.endpoint, this.query);
      }
    });

    this.userService.user.subscribe((user: SocialUser) => {
      this.user = user;
    });

    this.userService.userid.subscribe((id: number) => {
     if (id !== -1) {  // The dialog is automatically closed if a user is signed in
        this.dialogRef.close(this.user?.photoUrl);  // and it returns the photo url if there is one
      }
    });
  }

  ngOnInit(): void {
    this.authService.authState.subscribe((user) => {
      this.userService.user.next(user);
    });
  }

  signInWithGoogle(): void {
    this.endpoint = 'google/';
    this.authService.signIn(GoogleLoginProvider.PROVIDER_ID);
  }

  signInWithFB(): void {
    this.endpoint = 'facebook/';
    this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  signOut(): void {
    if (this.user) {
      this.authService.signOut();
    }
  }

  submit(): void {
    if (this.status === 'register') {
      this.updateQuery();
      this.userService.register(this.userForm.value, this.query);
    }
    if (this.status === 'login') {
      this.userService.login(this.userForm.value);
    }
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

  ngOnDestroy(): void {
    this.endpoint = '';
    // this.signOut(); // Why do we signOut every time the component is destroyed (which is the case when we sign in or up)?
  }
}
