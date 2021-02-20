import {Component, OnDestroy, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {NgoRegistrationService} from '../../services/ngo-registration.service';
import {UserService} from '../../services/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {NewNgo, NgoOverviewItem} from '../../models/ngo';
import {BehaviorSubject} from 'rxjs';
import {ApiService} from '../../services/api.service';
import {NgoNameValidator} from './CustomValidators';
import {SocialAuthService, SocialUser} from 'angularx-social-login';
import {LoginService} from '../../services/login.service';


@Component({
  selector: 'app-ngo-sign-up',
  templateUrl: './ngo-sign-up.component.html',
  styleUrls: ['./ngo-sign-up.component.scss']
})
export class NgoSignUpComponent implements OnInit, OnDestroy {
  allNgoNames = new BehaviorSubject<string[]>([]);

  group = new FormGroup({
    ngoNameControl: new FormControl('', [Validators.required, new NgoNameValidator(this.allNgoNames).validator()]),
    countryControl: new FormControl('', Validators.required),

    firstNameControl: new FormControl('', Validators.required),
    lastNameControl: new FormControl('', Validators.required),
    emailRepresentativeControl: new FormControl('', [Validators.required, Validators.email]),

    userForm: new FormGroup({
      username: new FormControl('', Validators.required),
      email: new FormControl('', [Validators.required, Validators.email]),
      password: new FormControl('', Validators.required),
    })
  });

  $errorMessage = new BehaviorSubject<string>('');

  registrationSuccessful = false;

  user?: SocialUser;

  googleLogin = false;
  facebookLogin = false;

  constructor(
      private ngoRegistrationService: NgoRegistrationService,
      private userService: UserService,
      private snackBar: MatSnackBar,
      private apiService: ApiService,
      private authService: SocialAuthService,
      private loginService: LoginService
  ) {
  }

  ngOnInit(): void {
    this.$errorMessage.subscribe(value => {
      if (value !== '') {
        this.showErrorMessage();
      }
    });
    this.userService.$lastErrorMessage.subscribe(errorMessage => this.$errorMessage.next(errorMessage));

    this.apiService.get('idNames').subscribe((data: NgoOverviewItem[]) => {
      this.allNgoNames.next(data.map(ngo => ngo.name));
    });

    this.authService.authState.subscribe((user) => {
      this.user = user;
      this.loginService.trySocialLogin(this.getQuery(), this.user?.authToken);
    });

    this.userService.user.subscribe((user: SocialUser) => {
      this.user = user;
    });
  }

  ngOnDestroy(): void {
    this.loginService.fullSignOut(this.user); // validate account first
  }

  submit(): void {
    const newNgo = this.convertFormInputToNgo();

    this.$errorMessage.next('');

    this.ngoRegistrationService.registerNewNgo(newNgo).subscribe((result: any) => {
          this.registerUser();
        },
        (error: any) => {
          const userMessage = error.error.error;
          this.$errorMessage.next(userMessage);
        });
  }

  private registerUser(): void {
    if (this.googleLogin) {
      this.loginService.googleLogin();
    } else if (this.facebookLogin) {
      this.loginService.facebookLogin();
    } else {
      const query = this.getQuery();
      this.userService.register(this.group.get('userForm')?.value, query);
    }

    if (this.$errorMessage.getValue() === '') {
      this.registrationSuccessful = true;
    }
  }

  private getQuery(): any {
    return {ngo_name: this.group.get('ngoNameControl')?.value};
  }

  private showErrorMessage(): void {
    this.snackBar.open(this.$errorMessage.getValue(), '', {
      duration: 3000,
      panelClass: ['login-snackbar']
    });
  }

  private convertFormInputToNgo(): NewNgo {
    return {
      ngoName: this.group.get('ngoNameControl')?.value,
      ngoCountry: this.group.get('countryControl')?.value,

      representativeFirstName: this.group.get('firstNameControl')?.value,
      representativeLastName: this.group.get('lastNameControl')?.value,
      representativeEmail: this.group.get('emailRepresentativeControl')?.value
    };
  }

  toogleGoogleLoginStatus($event: MouseEvent): void {
    if (this.facebookLogin) {
      $event.stopPropagation();
      return;
    }

    if (this.googleLogin) {
      this.enableUserForm();
    } else {
      this.disableUserForm();
    }
    this.googleLogin = !this.googleLogin;
  }

  toggleFacebookLoginStatus($event: MouseEvent): void {
    if (this.googleLogin) {
      $event.stopPropagation();
      return;
    }

    if (this.facebookLogin) {
      this.enableUserForm();
    } else {
      this.disableUserForm();
    }
    this.facebookLogin = !this.facebookLogin;
  }

  private disableUserForm(): void {
    this.group.get('userForm')?.disable();
  }

  private enableUserForm(): void {
    this.group.get('userForm')?.enable();
  }
}

// TODO: validation of User Account thing: check for either of two boolean flags or valid form
