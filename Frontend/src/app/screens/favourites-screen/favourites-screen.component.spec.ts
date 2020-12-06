import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FavouritesScreenComponent } from './favourites-screen.component';

describe('FavouritesScreenComponent', () => {
  let component: FavouritesScreenComponent;
  let fixture: ComponentFixture<FavouritesScreenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FavouritesScreenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FavouritesScreenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
