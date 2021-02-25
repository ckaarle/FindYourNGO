import {Injectable, OnDestroy} from '@angular/core';
import {AbstractControl, EmailValidator, FormControl, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import {BehaviorSubject, Subscription} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NgoNameValidator implements OnDestroy {
  allNgoNames: string[] = [];

  nameSubscription: undefined | Subscription;

  constructor(allNgoNames: BehaviorSubject<string[]>) {
    this.nameSubscription = allNgoNames.subscribe(value => this.allNgoNames = value.map(name => name.toLowerCase()));
  }

  validator(): ValidatorFn {

    return (control: AbstractControl): ValidationErrors | null => {
      if (this.allNgoNames.indexOf(control.value.toLowerCase()) >= 0) {
        return {
          ngoNameDuplicate: true
        };
      }
      return null;
    };
  }

  ngOnDestroy(): void {
    this.nameSubscription?.unsubscribe();
  }
}

@Injectable({
  providedIn: 'root',
})
export class LoginChoiceValidator {

  dummyEmail = new FormControl('', Validators.email);

  constructor(private loginChoice1: BehaviorSubject<boolean>, private loginChoice2: BehaviorSubject<boolean>) {
  }

  validator(): ValidatorFn {

    return (control: AbstractControl): ValidationErrors | null => {

      if (this.loginChoice1.getValue() || this.loginChoice2.getValue()) {
        return null;
      }

      const error = {
        loginChoiceMissing: true
      };

      const username = control.get('username');
      const email = control.get('email');
      const password = control.get('password');

      if (!username?.value || !email?.value || !password?.value) {
        return error;
      }

      this.dummyEmail.setValue(email.value);

      if (this.dummyEmail.valid) {
        return null;
      }

      return error;
    };
  }
}
