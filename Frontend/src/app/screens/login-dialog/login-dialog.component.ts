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
  $names: Observable<string[]>;
  ngoControl = new FormControl();
  status = '';
  userForm = new FormGroup({
    username: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(public dialogRef: MatDialogRef<LoginDialogComponent>,
              private authService: SocialAuthService,
              private apiService: ApiService) {
    this.isNgo = false;
    this.apiService.get('names').subscribe((data: Names) => {
      this.names = data.names;
    });
    this.$names = this.ngoControl.valueChanges.pipe(
        startWith(''), map(value => this._filter(value))
    );
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.updateQuery();
      if (this.endpoint) {
        this.apiService.socialLogin({token: this.user?.authToken}, this.endpoint, this.query);
      }
    });
    this.apiService.userid.subscribe((id: string) => {
      if (id !== '') {  // The dialog is automatically closed if a user is signed in
        this.dialogRef.close(this.user?.photoUrl);  // and it returns the photo url if there is one
      }
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

  ngOnInit(): void {
    this.authService.authState.subscribe((user) => {
      this.user = user;
    });
  }

  ngOnDestroy(): void {
    this.endpoint = '';
    this.signOut();
  }

  submit(): void {
    if (this.status === 'register') {
      this.updateQuery();
      this.apiService.register(this.userForm.value, this.query);
    }
    if (this.status === 'login') {
      this.apiService.login(this.userForm.value);
    }
  }

  checkNgo($event: MatCheckboxChange): void {
    this.isNgo = !this.isNgo;
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.names.filter(option => option.toLowerCase().includes(filterValue));
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
}