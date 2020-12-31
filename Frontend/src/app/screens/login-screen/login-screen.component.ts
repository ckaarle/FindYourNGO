import { Component, OnInit } from '@angular/core';
import { SocialAuthService, SocialUser } from 'angularx-social-login';
import { FacebookLoginProvider, GoogleLoginProvider } from 'angularx-social-login';
import { ApiService } from '../../services/api.service';
import { Names } from '../../models/ngo';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { Observable, of } from 'rxjs';
import {FormControl, FormGroup} from '@angular/forms';
import { map, startWith } from 'rxjs/operators';

@Component({
  selector: 'app-login-screen',
  templateUrl: './login-screen.component.html',
  styleUrls: ['./login-screen.component.scss']
})
export class LoginScreenComponent implements OnInit {

  user?: SocialUser;
  loggedIn?: boolean;
  endpoint?: string;
  isNgo: boolean;
  query: any;
  names: string[] = [];
  $names: Observable<string[]>;
  ngoControl = new FormControl();
  ngoName = '';
  status = '';
  userForm = new FormGroup({
    username: new FormControl(''),
    email: new FormControl(''),
    password: new FormControl(''),
  });

  constructor(private authService: SocialAuthService, private apiService: ApiService) {
    this.isNgo = false;
    this.apiService.get('names').subscribe((data: Names) => {
      this.names = data.names;
    });
    this.$names = this.ngoControl.valueChanges.pipe(
        startWith(''), map(value => this._filter(value))
    );
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.loggedIn = (user != null);
      this.updateQuery();
      if (this.endpoint) {
        this.apiService.post(this.endpoint, {token: this.user?.authToken}, this.query).subscribe(
            data => console.log(data));
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
    this.authService.signOut();
  }

  ngOnInit(): void {
    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.loggedIn = (user != null);
    });
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
