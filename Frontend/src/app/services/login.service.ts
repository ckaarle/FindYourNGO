import {Injectable, OnDestroy} from '@angular/core';
import {UserService} from './user.service';
import {FacebookLoginProvider, GoogleLoginProvider, SocialAuthService, SocialUser} from 'angularx-social-login';

@Injectable({
  providedIn: 'root'
})
export class LoginService implements OnDestroy {

  endpoint?: string;

  constructor(private userService: UserService, private authService: SocialAuthService) {
  }

  ngOnDestroy(): void {
    this.endpoint = '';
  }

  trySocialLogin(query: any, authToken: string | undefined): void {
    if (this.endpoint) {
      this.userService.socialLogin({token: authToken}, this.endpoint, query);
    }
  }

  googleLogin(): void {
    this.endpoint = 'google/';
    this.authService.signIn(GoogleLoginProvider.PROVIDER_ID);
  }

  facebookLogin(): void {
    this.endpoint = 'facebook/';
    this.authService.signIn(FacebookLoginProvider.PROVIDER_ID);
  }

  signOut(user: SocialUser | undefined): void {
    if (user) {
      this.authService.signOut();
    }
  }
}
