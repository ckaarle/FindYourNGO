import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {NgoRegistrationService} from '../../services/ngo-registration.service';
import {UserService} from '../../services/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {NewNgo, NgoFilterOptions, NgoOverviewItem} from '../../models/ngo';
import {BehaviorSubject} from 'rxjs';
import {ApiService} from '../../services/api.service';
import {LoginChoiceValidator, NgoNameValidator} from './CustomValidators';
import {SocialAuthService, SocialUser} from 'angularx-social-login';
import {LoginService} from '../../services/login.service';
import {MAT_CHECKBOX_DEFAULT_OPTIONS, MatCheckboxDefaultOptions} from '@angular/material/checkbox';
import {Utils} from '../../services/utils';


@Component({
  selector: 'app-ngo-sign-up',
  templateUrl: './ngo-sign-up.component.html',
  styleUrls: ['./ngo-sign-up.component.scss'],
  providers: [
    {provide: MAT_CHECKBOX_DEFAULT_OPTIONS, useValue: { clickAction: 'noop' } as MatCheckboxDefaultOptions}
  ]
})
export class NgoSignUpComponent implements OnInit {
  allNgoNames = new BehaviorSubject<string[]>([]);
  googleLogin = new BehaviorSubject(false);
  facebookLogin = new BehaviorSubject(false);

  group = new FormGroup({
    ngoNameControl: new FormControl('', [Validators.required, new NgoNameValidator(this.allNgoNames).validator()]),
    countryControl: new FormControl(null, Validators.required),

    firstNameControl: new FormControl('', Validators.required),
    lastNameControl: new FormControl('', Validators.required),
    emailRepresentativeControl: new FormControl('', [Validators.required, Validators.email]),

    userForm: new FormGroup({
      username: new FormControl(''),
      email: new FormControl(''),
      password: new FormControl(''),
    }, new LoginChoiceValidator(this.googleLogin, this.facebookLogin).validator())
  });

  $errorMessage = new BehaviorSubject<string>('');

  registrationSuccessful = false;

  user?: SocialUser;

  countries: string[] = [];

  constructor(
      private ngoRegistrationService: NgoRegistrationService,
      private userService: UserService,
      private snackBar: MatSnackBar,
      private apiService: ApiService,
      private authService: SocialAuthService,
      private loginService: LoginService
  ) {
    this.apiService.get('ngos/filteroptions/').subscribe((data: NgoFilterOptions) => {
      const filterOptions = Utils.mapDataToNgoFilterOptions(data);
      this.countries = filterOptions.countries.values;
    });
  }

  ngOnInit(): void {
    this.$errorMessage.subscribe(value => {
      if (value !== '') {
        this.showErrorMessage();
      }
    });
    this.userService.$lastErrorMessage.subscribe(error => this.$errorMessage.next(error.error));

    this.apiService.get('idNamesFull').subscribe((data: NgoOverviewItem[]) => {
      this.allNgoNames.next(data.map(ngo => ngo.name));
    });

    this.authService.authState.subscribe((user) => {
      this.user = user;

      if (user) {
        this.loginService.trySocialLogin(this.getQuery(), this.user?.authToken);
      }

    });

    this.userService.user.subscribe(user => this.user = user);
  }

  submit(): void {
    const newNgo = this.convertFormInputToNgo();

    this.$errorMessage.next('');

    this.ngoRegistrationService.registerNewNgo(newNgo).subscribe((result: any) => {
          this.registerUser();
          this.registrationSuccessful = true;
        },
        (error: any) => {
          const userMessage = error.error.error;
          this.$errorMessage.next(userMessage);
        });
  }

  private registerUser(): void {
    if (this.googleLogin.getValue()) {
      this.loginService.googleLogin();
    } else if (this.facebookLogin.getValue()) {
      this.loginService.facebookLogin();
    } else {
      const query = this.getQuery();
      this.userService.register(this.group.get('userForm')?.value, query, true);
    }
  }

  private getQuery(): any {
    return {ngo_name: this.group.get('ngoNameControl')?.value};
  }

  private showErrorMessage(): void {
    if (!this.$errorMessage.getValue() || this.$errorMessage.getValue().trim() === '') {
      return;
    }

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
    this.toggleStatus(this.googleLogin, this.facebookLogin, $event);
  }

  toggleFacebookLoginStatus($event: MouseEvent): void {
    this.toggleStatus(this.facebookLogin, this.googleLogin, $event);
  }

  private disableUserForm(): void {
    this.group.get('userForm')?.disable();
  }

  private enableUserForm(): void {
    this.group.get('userForm')?.enable();
  }

  private toggleStatus(active: BehaviorSubject<boolean>, other: BehaviorSubject<boolean>, $event: MouseEvent): void {
    if (other.getValue()) {
      $event.stopPropagation();
      return;
    }

    if (active.getValue()) {
      this.enableUserForm();
    } else {
      this.disableUserForm();
    }
    active.next(!active.getValue());
    this.group.get('userForm')?.updateValueAndValidity();
  }
}
