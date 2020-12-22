import { Overlay, OverlayConfig, OverlayRef } from '@angular/cdk/overlay';
import { ComponentPortal, PortalInjector } from '@angular/cdk/portal';
import { Injectable, Injector, InjectionToken, ComponentRef, Inject } from '@angular/core';
import { NgoDetailItemComponent } from '../components/ngo-detail-item/ngo-detail-item.component';
import { NgoDetailItem } from '../models/ngo';

interface CustomOverlayConfig {
  panelClass?: string;
  hasBackdrop?: boolean;
  backdropClass?: string;
  height?: string;
  ngoDetailItem?: NgoDetailItem;
}

const DEFAULT_CONFIG: CustomOverlayConfig = {
  hasBackdrop: true,
  backdropClass: 'dark-backdrop',
  panelClass: 'ngo-custom-overlay',
};

export const NGO_DETAIL_ITEM_DIALOG_DATA = new InjectionToken<NgoDetailItem>('NGO_DETAIL_ITEM_DIALOG_DATA');

@Injectable({
  providedIn: 'root'
})
export class OverlayService {

  constructor(
    private overlay: Overlay,
    private injector: Injector
  ) { }

  open(config: CustomOverlayConfig = {}) {
    const dialogConfig = {...DEFAULT_CONFIG, ...config};
    const overlayRef = this.createOverlay(dialogConfig);

    const dialogRef = new CustomOverlayRef(overlayRef);

    const customPortal = this.attachDialogContainer(overlayRef, dialogConfig, dialogRef);
    overlayRef.backdropClick().subscribe(_ => dialogRef.close());

    return dialogRef;
  }

  private attachDialogContainer(overlayRef: OverlayRef, config: CustomOverlayConfig, dialogRef: CustomOverlayRef) {
    const injector = this.createInjector(config, dialogRef);

    const containerPortal = new ComponentPortal(NgoDetailItemComponent, null, injector);
    const containerRef: ComponentRef<NgoDetailItemComponent> = overlayRef.attach(containerPortal);

    return containerRef.instance;
  }

  private createInjector(config: CustomOverlayConfig, dialogRef: CustomOverlayRef): PortalInjector {
    const injectionTokens = new WeakMap();

    injectionTokens.set(CustomOverlayRef, dialogRef);
    injectionTokens.set(NGO_DETAIL_ITEM_DIALOG_DATA, config.ngoDetailItem);

    return new PortalInjector(this.injector, injectionTokens);
  }

  private createOverlay(config: CustomOverlayConfig) {
    const overlayConfig = this.getOverlayConfig(config);
    return this.overlay.create(overlayConfig)
  }

  private getOverlayConfig(config: CustomOverlayConfig): OverlayConfig {
    const positionStrategy = this.overlay.position()
      .global()
      .centerHorizontally()
      .centerVertically();

    const overlayConfig = new OverlayConfig({
      hasBackdrop: config.hasBackdrop,
      backdropClass: config.backdropClass,
      panelClass: config.panelClass,
      scrollStrategy: this.overlay.scrollStrategies.reposition(),
      positionStrategy
    });

    return overlayConfig;
  }
}


export class CustomOverlayRef {
  
  constructor(private overlayRef: OverlayRef) { }

  close(): void {
    this.overlayRef.dispose();
  }
}