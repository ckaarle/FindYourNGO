import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {NgoRegistrationService} from '../../services/ngo-registration.service';
import {UserService} from '../../services/user.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import {NewNgo} from '../../models/ngo';
import {BehaviorSubject} from 'rxjs';

@Component({
  selector: 'app-ngo-sign-up',
  templateUrl: './ngo-sign-up.component.html',
  styleUrls: ['./ngo-sign-up.component.scss']
})
export class NgoSignUpComponent implements OnInit {

  group = new FormGroup({
    ngoNameControl: new FormControl('', Validators.required),
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

  constructor(
      private ngoRegistrationService: NgoRegistrationService,
      private userService: UserService,
      private snackBar: MatSnackBar,
  ) {
  }

  ngOnInit(): void {
    this.$errorMessage.subscribe(value => {
      if (value !== '') {
        this.showErrorMessage();
      }
    });
    this.userService.$lastErrorMessage.subscribe(errorMessage => this.$errorMessage.next(errorMessage));

    // TODO fetch all ngo names and throw error if one of them is used via a validator (plus message!)
    // TODO country autocomplete
  }

  submit(): void {
    const newNgo = this.convertFormInputToNgo();

    this.$errorMessage.next('');

    this.ngoRegistrationService.registerNewNgo(newNgo).subscribe((result: any) => {
          const query = {ngo_name: this.group.get('ngoNameControl')?.value};
          this.userService.register(this.group.get('userForm')?.value, query);
          this.userService.signOut(); // validate account first

          if (this.$errorMessage.getValue() === '') {
            this.registrationSuccessful = true;
          }
        },
        (error: any) => {
          const userMessage = error.error.error;
          this.$errorMessage.next(userMessage);
        });
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
}
