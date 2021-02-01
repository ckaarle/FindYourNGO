import {Component} from '@angular/core';
import {Title} from '@angular/platform-browser';
import {ActivatedRoute, NavigationEnd, Router} from '@angular/router';
import {filter, map} from 'rxjs/operators';
import {MediaService} from './services/media.service';
import {UserService} from "./services/user.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  screens = ['Overview', 'Favourites', 'User'];
  activeScreen = this.screens[0];
  currentTitle: string = 'Find your NGO';

  constructor(private router: Router, private activatedRoute: ActivatedRoute, public media: MediaService, private titleService: Title, public userService: UserService) {
    this.init();
  }

  init(): void {
    this.setTitle();
    this.media.init();
  }

  setTitle(): void {
    this.router.events.pipe(
        filter((event) => event instanceof NavigationEnd),
        map(() => {
          let child = this.activatedRoute.firstChild;
          while (child) {
            if (child.firstChild) {
              child = child.firstChild;
            } else if (child.snapshot.data && child.snapshot.data['title']) {
              return child.snapshot.data['title'];
            } else {
              return null;
            }
          }
          return null;
        })
    ).subscribe((data: any) => {
      if (data) {
        this.titleService.setTitle(data);
        this.currentTitle = data;
      }
    });
  }

  getScreenIcon(screen: string): string {
    switch (screen) {
      case 'Map':
        return 'map';
      case 'Overview':
        return 'list';
      case 'Favourites':
        return 'star';
      case 'User':
        return 'star';
    }
    return '';
  }

  getRouterLink(screen: string): string {
    switch (screen) {
      case 'Map':
        return 'map';
      case 'Overview':
        return 'overview';
      case 'Favourites':
        return 'favourites';
      case 'Search':
        return 'search';
      case 'User':
        return 'user';
    }
    return '';
  }

  getCurrentRoute(): string {
    return this.router.url;
  }
}
