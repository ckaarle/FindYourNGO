import { Injectable } from '@angular/core';
import { MediaObserver } from '@angular/flex-layout'
import { EventManager } from '@angular/platform-browser';
import { Observable, Subject } from 'rxjs';

declare global {
  interface Window {

  }
}

export enum DeviceType {
  DESKTOP,
  MOBILE
}

@Injectable({
  providedIn: 'root'
})
export class MediaService {
  currentDevice: DeviceType = DeviceType.DESKTOP;
  private _mediachanged$: Subject<DeviceType> = new Subject();
  public mediachanged$: Observable<DeviceType> = this._mediachanged$.asObservable()

  constructor(private media: MediaObserver, private eventManager: EventManager) {
    this.updateDeviceType();

    this.media.media$.subscribe(() => {
      this.updateDeviceType();
    });

    this.eventManager.addGlobalEventListener('window', 'resize', this.updateDeviceType.bind(this));
  }

  public init(): void { }

  updateDeviceType() {
    let oldDevice = this.currentDevice;

    this.currentDevice = (window.matchMedia('screen and (max-width: 1000px').matches) ? DeviceType.MOBILE : DeviceType.DESKTOP;

    if (this.currentDevice != oldDevice) {
      this._mediachanged$.next(this.currentDevice);
    }
  }

  isMobile(): boolean {
    return this.currentDevice === DeviceType.MOBILE;
  }

  isDesktop(): boolean {
    return this.currentDevice === DeviceType.DESKTOP;
  }
}
