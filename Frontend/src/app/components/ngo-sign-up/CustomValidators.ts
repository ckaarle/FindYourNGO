import {Injectable, OnDestroy} from '@angular/core';
import {AbstractControl, EmailValidator, ValidationErrors, ValidatorFn} from '@angular/forms';
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
      console.log(control.value);
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

  constructor(private loginChoice1: BehaviorSubject<boolean>, private loginChoice2: BehaviorSubject<boolean>) {
  }

  validator(): ValidatorFn {

    return (control: AbstractControl): ValidationErrors | null => {

      // console.log(this.loginChoice1.getValue())
      // console.log(this.loginChoice2.getValue())
      // console.log('----')
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

      const emailValidator = new EmailValidator();

      const emailValidation = emailValidator.validate(email);
      // console.log(emailValidation)

      if (emailValidation === null) {
        return null;
      }

      return error;
    };
  }
}
